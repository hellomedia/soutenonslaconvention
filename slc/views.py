import uuid

from email_validator import validate_email
from email_validator import EmailNotValidError
from fresco import Response
from fresco import Route
from fresco import context
from fresco import object_or_404
from fresco import urlfor
from fresco.exceptions import Forbidden

from slc import caching
from slc import fileuploads
from slc import options
from slc import supporters
from slc import queries
from slc.queuing import queue_send_mail
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


def support_us_email(request):

    email = request.get("email", "").strip().lower()
    try:
        validate_email(email)
    except EmailNotValidError:
        raise

    conn = request.getconn()
    with queries.transaction(conn):
        user_id = supporters.add_supporter_from_email(conn, email)

    request.remember_user_id(user_id)
    token = str(uuid.uuid4())
    url = urlfor("verify-email", token=token)
    caching.cache.set(f"verify-email:{token}", (email, request.now))
    queue_send_mail(
        options.MAIL_FROM,
        "Please confirm your email address",
        recipients=[email],
        body=url,
    )
    return Response.redirect(support_step, _query={"step": 2})


def verify_email(request, token):
    try:
        user_id, email, when = caching.cache.get(f"verify-email:{token}")
    except TypeError:
        return piglet.render("default/token-expired.html")
    return Response("ok")


def oauth_login(request, provider, already_logged_in_redirect="index"):
    app = context.app
    session = request.session
    credentials = object_or_404(app.options.OAUTH_CREDENTIALS.get(provider))
    provider_info = object_or_404(OAUTH_PROVIDERS.get(provider))

    # if request.is_authenticated():
    #    return Response.redirect(already_logged_in_redirect)
    oauth = get_oauth2session(provider, credentials["id"])
    url, session["oauth_state"] = oauth.authorization_url(
        provider_info["authorization_base_url"]
    )
    return Response.redirect(url)


def oauth_callback(request, provider):
    session = request.session

    state = object_or_404(session.get("oauth_state"), Forbidden)
    code = object_or_404(request.get("code"))
    profile = fetch_profile(provider, state, code, request.url)

    conn = request.getconn()
    with queries.transaction(conn):
        user_id = supporters.add_supporter_from_social_profile(
            conn, provider, profile
        )

    request.remember_user_id(user_id)
    return Response.redirect(support_step, _query={"step": 2})


def support_step(request):
    if not request.is_authenticated():
        return Response.redirect(support_us)
    try:
        step = int(request.get("step"))
    except (TypeError, ValueError):
        return Response.redirect(support_us)

    supporter = supporters.get_supporter_by_id(
        request.getconn(), request.get_user_id()
    )
    if supporter is None:
        return Response.redirect(support_us)

    template = f"default/support-us-step-{step}.html"
    return piglet.render(template, {"step": step, "supporter": supporter})


def support_step_submit(request):
    if not request.is_authenticated():
        return Response.redirect(support_us)
    try:
        step = int(request.get("step"))
    except (TypeError, ValueError):
        return Response.redirect(support_us)

    conn = request.getconn()
    if "skip" not in request:
        data = dict(request.form)
        data.pop("step")
        # TODO: image uploading
        data.pop("image", None)
        with queries.transaction(conn):
            supporters.update_profile(conn, id=request.get_user_id(), **data)
    return Response.redirect(support_step, _query={"step": step + 1})


def submit_suggestion(request):
    conn = request.getconn()
    supporter_id = request.get_user_id()
    suggestion = request.get("suggestion")
    if suggestion and supporter_id:
        with queries.transaction(conn):
            supporters.register_suggestion(conn, supporter_id, suggestion)

    return Response(headers=[("X-HX-Trigger", "suggestionSubmitted")])


def filepond_upload(request, media_dir="media/"):
    """
    See https://pqina.nl/filepond/docs/patterns/api/server/

    Expects a single field with two values: metadata, then upload
    """
    form = request.form
    key = next(form.keys())
    metadata, upload = form.getlist(key)
    filename = fileuploads.upload(media_dir, upload)
    return Response([filename], content_type="text/plain")
