import logging
from typing import Any
from typing import Dict

from slc import queries

logger = logging.getLogger(__name__)


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
