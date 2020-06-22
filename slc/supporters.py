import logging
from dataclasses import dataclass
from embrace.exceptions import NoResultFound
from typing import Any
from typing import Callable
from typing import Dict
from typing import Optional

from htmltextconvert import html_to_text
from fresco_utils.security import generate_random_string
from fresco import context
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
):
    return queries.update_supporter_profile(
        conn,
        id=id,
        display_name=display_name,
        reason=reason,
        suggestion=suggestion,
        image_path=image_path,
        display_image=display_image,
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
        "Please confirm your email address",
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
