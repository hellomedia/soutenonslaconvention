import logging
from dataclasses import dataclass
from embrace.exceptions import NoResultFound
from typing import Any
from typing import Optional
from typing import Dict

from slc import queries

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
        from fresco import context

        if not self.display_image:
            return None
        if "://" in self.display_image:
            return self.display_image
        return context.app.urlfor("media", path=self.display_image)


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
