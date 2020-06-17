from datetime import datetime

from fresco import context
from fresco import Request as FrescoRequest
from fresco.exceptions import BadRequest
from fresco_i18n.i18nformat import Formatter
from pytz import UTC


AUTH_USERNAME_SEPARATOR = "\n"
_marker = object()


class Request(FrescoRequest):

    UNDEFINED = object()
    SESSION_ENV_KEY = "ob.session"
    _now = None
    _conn = None

    format = Formatter("fr")

    def getint(self, key, default=_marker):
        v = self.get(key, _marker)
        if v is _marker:
            if default is _marker:
                raise BadRequest()
            else:
                return default
        try:
            return int(v)
        except Exception:
            if default is _marker:
                raise BadRequest()
            else:
                return default

    @property
    def now(self, utcnow=datetime.utcnow, utc=UTC):  # type: ignore
        if self._now:
            return self._now
        self._now = utcnow().replace(tzinfo=utc)
        return self._now

    def getconn(self):
        if self._conn:
            return self._conn

        self._conn = context.app.options.connection_pool.getconn()
        return self._conn
