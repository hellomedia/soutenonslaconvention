from mailsend import Mail
from random import choices
from slc import options

mailers = []
mailer_weights = []
for item in options.SMTP_SERVERS:
    if item["enabled"]:
        mailers.append(Mail(item["url"], **options.MAILER_OPTIONS))
        mailer_weights.append(item["monthly_quota"])


def get_mailer():
    return choices(mailers, weights=mailer_weights, k=1)[0]
