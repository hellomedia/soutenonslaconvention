from slc import options
from slc import queuing


def send_suggestion(conn, supporter, suggestion):
    if supporter:
        subject = (
            f"Soutenons la Convention: "
            f"une suggestion de "
            f"{supporter.full_name or supporter.display_name or supporter.email} "
            f"(#{supporter.id})"
        )

        reply_to = supporter.email
    else:
        subject = f"Soutenons la Convention: une suggestion"
        reply_to = None
    if suggestion:
        queuing.queue_send_mail(
            options.MAIL_FROM,
            subject=subject,
            recipients=[options.CONTACT_EMAIL],
            reply_to=reply_to,
            body=suggestion,
        )
