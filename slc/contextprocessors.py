from fresco_i18n.i18nformat import Formatter

from slc import assets
from slc.templating import piglet

formatter = Formatter("fr")


@piglet.contextprocessor
def default_context(request):
    return {
        "static": lambda path: f"/static/{path}",
        "assets": assets.assetbuilder,
        "format": formatter,
    }
