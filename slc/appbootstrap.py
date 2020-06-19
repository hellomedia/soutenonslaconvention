from functools import partial

from fresco.middleware import XForwarded
from fresco_static import StaticFiles
from pkg_resources import resource_filename
import yoyo
import embrace
import embrace.pool
import obsession
import psycopg2
import psycopg2.extras

import slc
from slc import app
from slc import loadoptions

loadoptions.configure_app(app)
options = app.options


def apply_migrations():
    backend = yoyo.get_backend(options.DATABASE)
    migrations = yoyo.read_migrations(
        resource_filename(__name__, "../migrations")
    )
    with backend.lock():
        backend.apply_migrations(backend.to_apply(migrations))


from slc import routes  # noqa
from slc import contextprocessors  # noqa
from slc import assets  # noqa

app.include("/", routes)
app.route_wsgi("/assets", assets.assetbuilder)

slc.queries = embrace.module(
    resource_filename(__name__, "queries"),
    auto_reload=app.options.EMBRACE_AUTO_RELOAD,
)

apply_migrations()

connection_pool = options.connection_pool = embrace.pool.ConnectionPool(
    partial(
        psycopg2.connect,
        options.DATABASE,
        cursor_factory=psycopg2.extras.NamedTupleCursor,
    ),
    limit=options.DATABASE_POOL_CONNECTION_LIMIT,
)

app.add_middleware(XForwarded, trusted=options.UPSTREAM_PROXIES)
app.add_middleware(
    obsession.SessionMiddleware,
    backend=obsession.FileBackend(directory=options.SESSION_DIR),
    id_persister=obsession.CookieIdPersistence(
        cookie_name="s", max_age=86400, path="/"
    ),
)

app.static = StaticFiles(app)
app.static.add_package("slc", "../_build", cache_max_age=120)
app.media = StaticFiles(app, prefix="/media", route_name="media")
app.media.add_directory("media-files", "media", cache_max_age=3600)


@app.process_teardown
def release_conn(request):
    if request._conn:
        connection_pool.release(request._conn)
