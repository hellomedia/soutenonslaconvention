import json

from morf import fields
import morf


class SupporterForm(morf.HTMLForm):

    display_name = fields.Str(default=None)
    reason = fields.Str(default=None)
    occupation_id = fields.Int(default=None)
    year_of_birth = fields.Str(default=None)
    photo_option = fields.Choice(choices=["upload", "existing", "none"], default=None)
    image_path = fields.Str(default=None)
    signed_mesopinions_petition = fields.Bool(default=False)

    @morf.cleans(year_of_birth)
    def clean_year_of_birth(self, yob):
        try:
            json.loads(yob)
        except (TypeError, ValueError):
            return None
