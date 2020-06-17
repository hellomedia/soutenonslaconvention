from fresco import Route
from functools import partial

from slc.templating import piglet

__routes__ = [
    Route(
        "/", name="index", GET=partial(piglet.render, "default/index.html", {})
    ),
    Route(
        "/qui-sommes-nous",
        name="about",
        GET=partial(piglet.render, "default/about.html", {}),
    ),
    Route("/soutiens", GET=partial(piglet.render, "default/soutiens.html", {})),
    Route("/test", GET=partial(piglet.render, "default/test.html", {})),
]
