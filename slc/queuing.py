import logging

from huey import SqliteHuey

from slc.appbootstrap import options
from slc.mailer import get_mailer

logger = logging.getLogger(__name__)
huey = SqliteHuey(filename=options.HUEY_DB)


@huey.task(retries=10, retry_delay=60)
def queue_send_mail(*args, **kwargs):
    mailer = get_mailer()
    logger.warning(f"Sending via {mailer.username} @ {mailer.hostname}")
    mailer.send(*args, **kwargs)
