import os
from pkg_resources import resource_filename

from fresco_template import Piglet
from piglet.loader import TemplateLoader

from slc import app

__all__ = ["piglet"]

piglet_loader = TemplateLoader(
    [os.path.normpath(resource_filename(__name__, "../templates"))],
    auto_reload=app.options.PIGLET_AUTO_RELOAD,
    cache_dir=app.options.PIGLET_CACHE_DIR,
)
piglet = Piglet(piglet_loader)
