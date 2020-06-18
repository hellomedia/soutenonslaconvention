import logging

from diskcache import Cache
from slc import options

logger = logging.getLogger(__name__)

cache = Cache(options.CACHE_DIR, **options.CACHE_SETTINGS)
