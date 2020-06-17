from fresco import context
from fresco import object_or_404
from requests_oauthlib import OAuth2Session


OAUTH_PROVIDERS = {
    "facebook": {
        "authorization_base_url": "https://graph.facebook.com/oauth/authorize",
        "token_url": "https://graph.facebook.com/oauth/access_token",
        "profile_url": "https://graph.facebook.com/me?fields=email,picture,gender,first_name,name",
        "base_url": "https://graph.facebook.com/",
        "scope": ["public_profile", "email"],
    },
    "google": {
        "scope": [
            "https://www.googleapis.com/auth/userinfo.email",
            "https://www.googleapis.com/auth/userinfo.profile",
        ]
    },
}


def get_oauth2session(
    provider: str, client_id: str, state=None
) -> OAuth2Session:
    app = context.app
    provider_info = app.options.OAUTH_CREDENTIALS.get(provider)
    if provider_info is None:
        return None
    redirect_uri = app.urlfor("oauth-callback", provider=provider)
    return OAuth2Session(
        client_id,
        redirect_uri=redirect_uri,
        state=state,
        scope=provider_info["scope"],
    )


def user_id_from_profile(provider, profile):
    return f"{provider}{profile['id']}"


def fetch_profile(provider: str, state, code: str, current_url: str):
    urls = object_or_404(OAUTH_PROVIDERS.get(provider))
    credentials = object_or_404(
        context.app.options.OAUTH_CREDENTIALS.get(provider)
    )
    oauth = get_oauth2session(provider, credentials["id"], state=state)
    token = oauth.fetch_token(
        urls["token_url"],
        code=code,
        client_secret=credentials["secret"],
        authorization_response=current_url,
    )

    oauth = OAuth2Session(client_id=credentials["id"], token=token)
    return oauth.get(OAUTH_PROVIDERS[provider]["profile_url"]).json()
