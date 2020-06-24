import functools
from textwrap import dedent

from fresco_i18n.i18nformat import Formatter
from fresco_flash import flash
from markupsafe import Markup
from lazy_object_proxy import Proxy

from slc import assets
from slc import options
from slc import supporters
from slc import petition
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
        "supporter_count": Proxy(
            lambda: (
                supporters.supporter_count(request.getconn())
                + petition.get_cached_count()
            )
        ),
    }
