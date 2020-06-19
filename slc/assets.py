from pkg_resources import resource_filename
from assetbuilder import AssetBuilder

from slc import app

GUPFILES = ["../gup/**/*.gup"]
CSSFILES = ["public/css/**"]
JSFILES = ["public/js/**"]

CSSDEPS = CSSFILES + GUPFILES
JSDEPS = JSFILES + GUPFILES

assetbuilder = AssetBuilder(
    "/assets",
    resource_filename(__name__, "../_build"),
    depdirs=[resource_filename(__name__, "static")],
    autobuild=app.options.ASSETS_AUTO_BUILD,
)
assetbuilder.set_default_build_command("gup -u {path}")

assetbuilder.add_paths("forms-css", ["css/forms.css"], CSSDEPS)
assetbuilder.add_paths(
    "default-css",
    ["css/main.css", "css/index.css", "css/soutiens.css", "css/util.css"],
    CSSDEPS,
)
