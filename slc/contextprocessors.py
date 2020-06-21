from fresco_i18n.i18nformat import Formatter
from fresco_flash import flash

from slc import assets
from slc.templating import piglet

formatter = Formatter("fr")


@piglet.contextprocessor
def default_context(request):
    return {
        "static": lambda path: f"/static/{path}",
        "assets": assets.assetbuilder,
        "format": formatter,
        "flash_messages": flash.messages(),
    }
