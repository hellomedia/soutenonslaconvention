import re

from returns.io import IOResultE
from returns.io import impure_safe
from returns.result import safe
from returns.unsafe import unsafe_perform_io
import html5lib
import requests


@impure_safe
def fetch_petition_page() -> requests.Response:
    r = requests.get(
        "https://www.mesopinions.com/"
        "petition/politique/"
        "sortie-crise-soutenons-convention-citoyenne-climat/86134"
    )
    r.raise_for_status
    return r


@safe
def parse_count(r: requests.Response) -> int:
    doc = html5lib.parse(r.text)
    text = doc.find(".//*[@class='mo-counter hide-sm']/{*}strong").text
    return int(re.sub(r"[^\d]", "", text))


def fetch_count() -> IOResultE:
    return fetch_petition_page().bind(parse_count)


def get_cached_count() -> int:
    from slc.caching import get_or_create

    def get_value():
        value = unsafe_perform_io(fetch_count())
        if isinstance(value, Exception):
            raise value
        return value

    return get_or_create(
        "petition-count", get_value, hours=1, use_stale_on_error=True
    )
