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
        "/politique-confidentialite",
        GET=templated_page,
        name="privacy",
        template="default/privacy.html",
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
    Route(
        "/support",
        GET="slc.views.support_us",
        POST="slc.views.support_us_email",
        name="support-us",
    ),
    Route(
        "/support-step",
        GET="slc.views.support_step",
        POST="slc.views.support_step_submit",
        name="support-step",
    ),
    Route(
        "/oauth/<provider:str>", GET="slc.views.oauth_login", name="oauth-login"
    ),
    Route(
        "/oauth/<provider:str>/callback",
        GET="slc.views.oauth_callback",
        name="oauth-callback",
    ),
    Route("/v/<token:str>", GET="slc.views.verify_email", name="verify-email"),
    Route(
        "/filepond/", POST="slc.views.filepond_upload", name="filepond-upload"
    ),
]
