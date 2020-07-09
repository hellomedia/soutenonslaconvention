import json

from morf import fields
import morf


class SupporterForm(morf.HTMLForm):

    display_name = fields.Str(default=None)
    reason = fields.Str(default=None)
    occupation_id = fields.Int(default=None)
    year_of_birth = fields.Str(default=None)
    photo_option = fields.Choice(choices=["upload", "existing", "none"])
    image_path = fields.Str(default=None)
    display_image = fields.Str(default=None)

    @morf.cleans(year_of_birth)
    def clean_year_of_birth(self, yob):
        try:
            json.loads(yob)
        except (TypeError, ValueError):
            return None

    @morf.cleans(display_image)
    def clean_display_image(self, display_image):
        photo_option = self.data.photo_option
        if photo_option == "upload":
            return self.data.image_path
        elif photo_option == "existing":
            return display_image
        return None

    def data_for_update(self):
        d = self.data.copy()
        d.pop("photo_option")
        return d
