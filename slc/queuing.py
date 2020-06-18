from huey import SqliteHuey
from slc.appbootstrap import options
from slc.mailer import mailer

huey = SqliteHuey(filename=options.HUEY_DB)


@huey.task(retries=10, retry_delay=60)
def queue_send_mail(*args, **kwargs):
    mailer.send(*args, **kwargs)
