from fresco import Response
from fresco import Route
from fresco import context
from fresco import object_or_404
from fresco import urlfor
from fresco import GetArg
from fresco.exceptions import Forbidden
from requests_oauthlib import OAuth2Session

from slc import options
from slc import supporters
from slc import queries
from slc.oauthlogin import OAUTH_PROVIDERS
from slc.oauthlogin import fetch_profile
from slc.oauthlogin import get_oauth2session
from slc.templating import piglet


def homepage(request):
    return piglet.render(
        "default/index.html",
        {"days_left": (options.CONVENTION_DATE - request.now.date()).days - 1},
    )


def templated_page(request, template):
    return piglet.render(template, {})


def support_us(request):
    return piglet.render("default/support-us.html", {})


@Route.filter(Response.redirect)
def oauth_login(request, provider, already_logged_in_redirect="index"):
    app = context.app
    session = request.session
    credentials = object_or_404(app.options.OAUTH_CREDENTIALS.get(provider))
    urls = object_or_404(OAUTH_PROVIDERS.get(provider))

    if request.is_authenticated():
        return already_logged_in_redirect
    oauth = get_oauth2session(provider, credentials["id"])
    url, session["oauth_state"] = oauth.authorization_url(
        urls["authorization_base_url"]
    )
    return url


@Route.filter(Response.redirect)
def oauth_callback(provider, success_redirect="index"):
    request = context.request
    session = request.session

    state = object_or_404(session.get("oauth_state"), Forbidden)
    code = object_or_404(request.get("code"))
    profile = fetch_profile(provider, state, code, request.url)

    conn = request.getconn()
    with queries.transaction(conn):
        supporters.add_supporter_from_social_profile(provider, profile)

    request.remember_user_id(
        oauth_login.user_id_from_profile(provider, profile)
    )

    return urlfor(success_redirect)


__routes__ = [
    Route("/<provider:str>/", GET=oauth_login, name="oauth-login"),
    Route(
        "/<provider:str>/callback", GET=oauth_callback, name="oauth-callback",
    ),
]
