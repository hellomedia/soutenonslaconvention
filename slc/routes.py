from fresco import Route
from fresco import routeargs
from functools import partial

templated_page = "slc.views.templated_page"
Route = partial(Route, request=routeargs.RequestObject)

__routes__ = [
    Route("/", name="index", GET="slc.views.homepage"),
    Route(
        "/qui-sommes-nous",
        GET=templated_page,
        name="about",
        template="default/about.html",
    ),
    Route(
        "/soutiens",
        GET=templated_page,
        template="default/soutiens.html",
        name="soutiens",
    ),
    Route(
        "/test", GET=templated_page, template="default/test.html", name="test",
    ),
]
