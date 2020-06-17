from slc import queries
from typing import Any
from typing import Dict


def add_supporter_from_social_profile(
    conn, provider: str, profile: Dict[str, Any]
) -> int:
    return queries.upsert_supporter(
        conn,
        provider=provider,
        social_id=id,
        first_name=profile.get("first_name"),
        last_name=profile.get("last_name"),
        picture_url=(
            profile["picture"]["data"]["url"]
            if profile.get("picture")
            else None
        ),
        account_confirmed=True,
    )
