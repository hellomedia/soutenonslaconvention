import json

from morf import fields
import morf
from slc import queries

class OrganisationForm(morf.HTMLForm):

    contact_email = fields.Str(default=None)
    contact_name = fields.Str(default=None)
    contact_phone = fields.Str(default=None)
    name = fields.Str(default=None)
    website = fields.Str(default=None)
    image_path = fields.Str(default=None)
    size = fields.Choice(
        choices=[
            ("S", "< 10 staff / personnel"),
            ("M", "10 - 100 staff / personnel"),
            ("L", "> 100 staff / personnel")
        ], default=None
    )
    state = fields.Choice(
        choices='get_state_choices', default="PENDING"
    )
    org_type = fields.Choice(
        choices='get_type_choices', default=None
    )
    sector = fields.Choice(
        choices='get_sector_choices', default=None
    )

    def __init__(self, conn):
        super().__init__()
        self.conn = conn

    def get_state_choices(self):
        return queries.column(self.conn, 'SELECT unnest(enum_range(null,null::organisation_state));')

    def get_type_choices(self):
        return queries.column(self.conn, 'SELECT unnest(enum_range(null,null::organisation_type));')

    def get_sector_choices(self):
        return queries.column(self.conn, 'SELECT unnest(enum_range(null,null::organisation_sector));')
