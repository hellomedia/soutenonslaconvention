import json

from morf import fields, widgets
import morf
from slc import queries

class OrganisationForm(morf.HTMLForm):

    contact_email = fields.Str(default=None, displayname="Email")
    contact_name = fields.Str(default=None, displayname="Nom")
    contact_phone = fields.Str(default=None, displayname="Téléphone")
    contact_role = fields.Str(default=None, displayname="Rôle")
    name = fields.Str(default=None, displayname="Dénomination")
    website = fields.Str(default=None, displayname="Site web")
    image_path = fields.Str(default=None, displayname="Logo")
    size = fields.Choice(
        choices=[
            ("S", "équipe < 10 personnes"),
            ("M", "équipe 10 - 100 personnes"),
            ("L", "équipe > 100 personnes")
        ], default=None, displayname="Taille"
    ),
    theme = fields.Choice(
        choices='get_theme_choices',
        widget=widgets.CheckboxGroup(),
        default=None,
        displayname="Thématique"
    ),
    scope = fields.Choice(
        choices='get_scope_choices', default=None, displayname="Echelle d'activité"
    )
    org_type = fields.Choice(
        choices='get_type_choices', default=None, displayname="Type"
    )
    sector = fields.Choice(
        choices='get_sector_choices', default=None, displayname="Secteur"
    )

    def __init__(self, conn):
        super().__init__()
        self.conn = conn

    def get_scope_choices(self):
        return queries.column(self.conn, 'SELECT unnest(enum_range(null,null::organisation_scope));')

    def get_type_choices(self):
        return queries.column(self.conn, 'SELECT unnest(enum_range(null,null::organisation_type));')

    def get_sector_choices(self):
        return queries.column(self.conn, 'SELECT unnest(enum_range(null,null::organisation_sector));')

    def get_theme_choices(self):
        return queries.column(self.conn, 'SELECT unnest(enum_range(null,null::organisation_theme));')
