from fresco.options import Options
import logging
from pathlib import Path
import toml

logger = logging.getLogger(__name__)
_options_loaded = []


def options_loaded(fn=None):
    _options_loaded.append(fn)


def _call_options_loaded(options):
    for func in _options_loaded:
        func(options)


def load_options(options=Options()):

    projectroot = Path(__file__).parent.parent
    sources = ["settings.py", ".env*"]
    sources = sorted(path for s in sources for path in projectroot.glob(s))

    for path in sources:
        logger.warning(f"Loading config from {path}")
        if path.suffix == ".py":
            options.update_from_file(str(path))
        elif path.suffix == ".toml":
            with path.open("r") as f:
                options.update(toml.load(f))
        else:
            with path.open("r") as f:
                options.update(load_key_value_pairs(f))

    return options


def configure_app(app):

    load_options(app.options)
    _call_options_loaded(app.options)
    return app


def load_key_value_pairs(f):
    lines = f
    lines = (line.split("#", 1)[0] for line in lines)
    pairs = (line.split("=", 1) for line in lines if "=" in line)
    return {k.strip(): v.strip() for k, v in pairs}
