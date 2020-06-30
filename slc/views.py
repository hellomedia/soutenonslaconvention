import json

from email_validator import validate_email
from email_validator import EmailNotValidError
from fresco import Response
from fresco import context
from fresco import object_or_404
from fresco import urlfor
from fresco.exceptions import Forbidden
from fresco_flash import flash

from slc import fileuploads
from slc import options
from slc import suggestions
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
    ).add_headers(cache_control="must-revalidate, max-age=30", vary="cookie")


def templated_page(request, template):
    return piglet.render(template, {})


def support_us(request):
    return piglet.render("default/support-us.html", {})


def support_us_email(request):

    email = request.get("email", "").strip().lower()
    try:
        validate_email(email)
    except EmailNotValidError:
        flash.info("veuillez vérifier votre adresse e-mail")
        return support_us(request)

    conn = request.getconn()
    with queries.transaction(conn):
        user_id = supporters.add_supporter_from_email(conn, email)

    supporters.send_confirmation_email(
        supporter_id=user_id,
        email=email,
        get_confirmation_url=lambda token: urlfor("confirm-email", token=token),
    )
    return Response.redirect(email_needs_confirmation, email=email)


def email_needs_confirmation(request, email):
    return piglet.render(
        "default/email-needs-confirmation.html", {"email": email}
    )


def confirm_email(request, token):
    conn = request.getconn()
    with queries.transaction(conn):
        supporter_id = supporters.confirm_email(conn, token)
        if supporter_id is None:
            return piglet.render("default/invalid-confirmation-token.html", {})
    request.remember_user_id(supporter_id)
    return Response.redirect(support_step, _query={"step": 2})


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
        supporters.download_social_image(conn, user_id)
    request.remember_user_id(user_id)
    return Response.redirect(support_step, _query={"step": 2})


def support_step(request):
    if not request.is_authenticated():
        return Response.redirect(support_us)
    try:
        step = int(request.get("step"))
    except (TypeError, ValueError):
        return Response.redirect(support_us)

    conn = request.getconn()
    supporter = supporters.get_supporter_by_id(
        request.getconn(), request.get_user_id()
    )
    if supporter is None:
        return Response.redirect(support_us)

    occupation_options = supporters.occupation_options(conn)
    year_of_birth_range_options = supporters.year_of_birth_range_options(
        supporter
    )
    template = f"default/support-us-step-{step}.html"
    return piglet.render(
        template,
        {
            "step": step,
            "supporter": supporter,
            "occupation_options": occupation_options,
            "year_of_birth_range_options": year_of_birth_range_options,
        },
    )


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
        photo_option = data.pop("photo-option", "existing")
        display_image = {
            "upload": data.get("image_path"),
            "existing": None,
            "none": None,
        }[photo_option]
        try:
            data["year_of_birth"] = json.loads(data.get("year_of_birth"))
        except ValueError:
            data["year_of_birth"] = None
        try:
            data["occupation_id"] = int(data.get("occupation_id"))
        except (TypeError, ValueError):
            data["occupation_id"] = None
        with queries.transaction(conn):
            supporters.update_profile(
                conn,
                id=request.get_user_id(),
                display_image=display_image,
                **data,
            )
    return Response.redirect(support_step, _query={"step": step + 1})


def submit_suggestion(request):
    conn = request.getconn()
    supporter_id = request.get_user_id()
    if supporter_id:
        supporter = supporters.get_supporter_by_id(conn, supporter_id)
    else:
        supporter = None
    suggestion = request.get("suggestion")
    suggestions.send_suggestion(conn, supporter, suggestion)

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
