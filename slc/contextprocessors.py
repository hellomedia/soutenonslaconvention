import functools
import json
from textwrap import dedent

from fresco_i18n.i18nformat import Formatter
from fresco_flash import flash
from markupsafe import Markup

from slc import assets
from slc import options
from slc.templating import piglet

formatter = Formatter("fr")


@functools.lru_cache()
def render_markdown(s):
    from markdown import Markdown

    return Markup(Markdown().convert(dedent(s)))


@piglet.contextprocessor
def default_context(request):
    return {
        "options": options,
        "static": lambda path: f"/static/{path}",
        "assets": assets.assetbuilder,
        "format": formatter,
        "markdown": render_markdown,
        "flash_messages": flash.messages(),
        "json": json.dumps,
    }
