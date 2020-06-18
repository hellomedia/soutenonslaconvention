from mailsend import Mail
from slc import options

mailer = Mail(sendmail="sendmail", **options.MAILER_OPTIONS)
