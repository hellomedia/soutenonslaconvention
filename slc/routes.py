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
        "/soutien-existant",
        GET="slc.views.existing_support",
        name="existing-support",
    ),
    Route(
        "/petition-count",
        GET="slc.views.petition_count",
        name="petition-count",
    ),
    Route("/soutiens", GET="slc.views.soutiens", name="soutiens",),
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
        "/suggestion",
        POST="slc.views.submit_suggestion",
        name="submit-suggestion",
    ),
    Route(
        "/oauth/<provider:str>", GET="slc.views.oauth_login", name="oauth-login"
    ),
    Route(
        "/oauth/<provider:str>/callback",
        GET="slc.views.oauth_callback",
        name="oauth-callback",
    ),
    Route(
        "/support/en-attente-de-validation/<email:str>",
        GET="slc.views.email_needs_confirmation",
        name="email-needs-validation",
    ),
    Route(
        "/v/<token:str>", GET="slc.views.confirm_email", name="confirm-email"
    ),
    Route(
        "/filepond/", POST="slc.views.filepond_upload", name="filepond-upload"
    ),
    Route("/admin/", GET="slc.views.supporter_list", name="admin-home"),
    Route(
        "/organisations/", GET="slc.views.organisation_form", name="organisation"
    ),
    Route(
        "/organisations/", POST="slc.views.organisation_form_submit", name="organisation-form-submit"
    ),
]
