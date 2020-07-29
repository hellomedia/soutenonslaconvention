from slc import queries
from dataclasses import dataclass
from datetime import datetime
from typing import List
from typing import Optional
from typing import Tuple

from embrace.exceptions import NoResultFound

from slc import queries
from slc.templating import piglet

from fresco import context

@dataclass
class Organisation:
    id: int
    created_at: datetime
    name: Optional[str]
    logo: Optional[str]
    website: Optional[str]
    state: Optional[str]
    contact_name: Optional[str]
    contact_email: bool
    contact_phone: Optional[str]
    contact_role: Optional[str]
    size: Optional[str]
    org_type: Optional[str]
    sector: Optional[str]
    scope: Optional[str]
    theme: Optional[List[str]]

    def uploaded_image_url(self):
        return context.app.urlfor("media", path=self.image_path)

    def logo_url(self):
        return context.app.urlfor("media", path=self.logo)


def organisation_count(conn) -> int:
    return queries.organisation_count(conn)

def create_organisation(conn, **data) -> int:
    return queries.create_organisation(
        conn,
        **data
    )

def get_organisation_by_id(conn, id: int) -> Optional[Organisation]:
    try:
        data = queries.organisation_info(conn, id=id)
    except NoResultFound:
        return None
    return Organisation(**data._asdict())

def get_organisation_list(
    conn, limit=100, offset=0
) -> Tuple[List[Organisation], bool]:
    result = [
        Organisation(**row._asdict())
        for row in queries.organisation_list(
            conn, limit=limit + 1, offset=offset
        )
    ]
    has_more_results = len(result) == limit + 1
    if has_more_results:
        result.pop()
    return result, has_more_results
