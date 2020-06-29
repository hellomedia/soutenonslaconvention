import logging
from dataclasses import dataclass
from datetime import date
from embrace.exceptions import NoResultFound
from typing import Any
from typing import Callable
from typing import Dict
from typing import Iterable
from typing import List
from typing import Optional
from typing import Tuple

from htmltextconvert import html_to_text
from fresco_utils.security import generate_random_string
from fresco import context
from psycopg2.extras import NumericRange
import requests

from slc import fileuploads
from slc import options
from slc import queries
from slc import caching
from slc import queuing
from slc.templating import piglet

logger = logging.getLogger(__name__)


@dataclass
class Supporter:
    id: int
    display_name: Optional[str]
    full_name: Optional[str]
    email: Optional[str]
    reason: Optional[str]
    suggestion: Optional[str]
    image_path: Optional[str]
    picture_url: Optional[str]
    display_image: Optional[str]
    year_of_birth: Optional[NumericRange]
    occupation_id: Optional[int]

    def display_image_url(self):

        if not self.display_image:
            return None
        if "://" in self.display_image:
            return self.display_image
        return context.app.urlfor("media", path=self.display_image)

    def uploaded_image_url(self):
        return context.app.urlfor("media", path=self.image_path)


def add_supporter_from_social_profile(
    conn, provider: str, profile: Dict[str, Any]
) -> int:
    logger.info(f"Got {provider} profile: {profile}")
    picture_data = profile.get("picture")
    if isinstance(picture_data, str):
        picture_url = picture_data
    elif isinstance(picture_data, dict):
        try:
            picture_url = picture_data["data"]["url"]
        except (KeyError, TypeError):
            picture_url = None
    else:
        picture_url = None

    return queries.upsert_supporter(
        conn,
        provider=provider,
        social_id=profile["id"],
        email=profile.get("email"),
        full_name=profile.get("name"),
        first_name=profile.get("given_name"),
        last_name=profile.get("family_name"),
        locale=profile.get("locale"),
        picture_url=picture_url,
        account_confirmed=True,
    )


def add_supporter_from_email(conn, email: str) -> int:

    return queries.upsert_supporter(
        conn,
        provider=None,
        social_id=None,
        email=email,
        full_name=None,
        first_name=None,
        last_name=None,
        locale=None,
        picture_url=None,
        account_confirmed=False,
    )


def get_supporter_by_id(conn, id: int) -> Supporter:
    try:
        data = queries.get_supporter_info(conn, id=id)
    except NoResultFound:
        return None
    return Supporter(**data._asdict())


def update_profile(
    conn,
    id: int,
    display_name=None,
    reason=None,
    suggestion=None,
    image_path=None,
    display_image=None,
    year_of_birth=None,
    occupation_id=None,
):
    if year_of_birth is None:
        year_of_birth_val = None
    else:
        year_of_birth_val = NumericRange(year_of_birth[0], year_of_birth[1])

    return queries.update_supporter_profile(
        conn,
        id=id,
        display_name=display_name,
        reason=reason,
        suggestion=suggestion,
        image_path=image_path,
        display_image=display_image,
        occupation_id=occupation_id,
        year_of_birth=year_of_birth_val,
    )


def register_suggestion(conn, supporter_id, suggestion):
    if not suggestion.strip():
        return
    update_profile(conn, id=supporter_id, suggestion=suggestion)
    supporter = get_supporter_by_id(conn, supporter_id)

    if suggestion:
        queuing.queue_send_mail(
            options.MAIL_FROM,
            f"Soutenons la Convention: une suggestions de {supporter.full_name}",
            recipients=[options.CONTACT_EMAIL],
            reply_to=supporter.email,
            body=suggestion,
        )


def download_social_image(conn, supporter_id):
    supporter = get_supporter_by_id(conn, supporter_id)
    r = requests.get(supporter.picture_url, stream=True)

    with fileuploads.content_addressed_file(options.MEDIA_DIR) as (
        f,
        get_filename,
    ):
        for chunk in r.iter_content(chunk_size=1024):
            f.write(chunk)
    update_profile(conn, supporter_id, image_path=get_filename())


def send_confirmation_email(
    email: str,
    supporter_id: int,
    get_confirmation_url: Callable[[str], str],
    expire: int = 86400,
):
    token = generate_random_string(16)
    url = get_confirmation_url(token)
    caching.cache.set(f"confirm-email:{token}", (supporter_id, email))
    html = piglet.as_string(
        "email/confirm-email.html", {"url": url, "email": email}
    )
    queuing.queue_send_mail(
        options.MAIL_FROM,
        "Validation de votre soutien à la Convention Citoyenne",
        recipients=[email],
        html=html,
        body=html_to_text(html),
    )


def confirm_email(conn, token) -> int:
    try:
        supporter_id, email = caching.cache.get(f"confirm-email:{token}")
    except TypeError:
        return None
    queries.confirm_email(conn, id=supporter_id, email=email)
    return supporter_id


def supporter_count(conn) -> int:
    return queries.supporter_count(conn)


def year_of_birth_range_options(
    supporter: Supporter,
) -> Iterable[Tuple[Optional[int], Optional[int]]]:
    """
    Return a list of (start year, end year) pairs for birth year ranges.
    None indicates an open-ended range.
    """

    def standard_options():
        year = date.today().year
        boundaries = [
            year - 65,
            year - 50,
            year - 35,
            year - 25,
            year - 18,
            year - 16,
        ]
        yield None, boundaries[0]
        yield from ((y1, y2) for y1, y2 in zip(boundaries, boundaries[1:]))
        yield boundaries[-1], None

    existing = None
    if supporter and supporter.year_of_birth:
        existing = supporter.year_of_birth.lower, supporter.year_of_birth.upper

    options = list(standard_options())
    print(options, existing)
    if existing in options:
        yield from ((option, option == existing) for option in options)
    else:
        if existing:
            yield existing, True
        yield from ((option, False) for option in options)


def occupation_options(conn) -> List[Tuple[int, str]]:
    return list(queries.occupations(conn))
