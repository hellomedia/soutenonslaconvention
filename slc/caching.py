from functools import partial
from math import log
from typing import Any
from typing import Callable
import logging
import shlex
import os
import random
import time
import psutil

from diskcache import Cache
from slc import options

logger = logging.getLogger(__name__)

cache = Cache(options.CACHE_DIR, **options.CACHE_SETTINGS)


def _get_or_create(
    cache: Cache,
    key: Any,
    creator: Callable,
    seconds: int = 0,
    minutes: int = 0,
    hours: int = 0,
    days: int = 0,
    use_stale_on_error: bool = False,
    _time=time.time,
    _random=random.random,
    retry_limit=8,
    UPDATING="cache-updating-marker",
) -> Any:
    """
    Gets a value from a cache, refreshing it if it doesn't exist.
    Avoids the dogpile effect.
    """

    def set_value():
        # Acquire a lock on the cache for that key
        pid = os.getpid()
        if cache.add((key, UPDATING), pid):
            logger.info(f"Got lock for cache key {key!r}")
            try:
                soft_expire = (
                    seconds + minutes * 60 + hours * 120 + days * 86400
                )
                now = _time()
                try:
                    value = creator()
                except Exception:
                    if use_stale_on_error:
                        logger.exception(
                            f"Could not regenerate cache value for {key}"
                        )
                        cached = cache.get(key, default=None)
                        if cached:
                            _, cost, value = cached
                        else:
                            raise
                    else:
                        raise
                else:
                    cost = _time() - now
                cache.set(key, (_time() + soft_expire, cost, value))
                logger.info(f"Releasing lock after {cost:.2f}s")
                return value, True
            finally:
                cache.delete((key, UPDATING))
        else:
            lock_held_by_pid = cache.get((key, UPDATING))
            if not lock_held_by_pid or not psutil.pid_exists(lock_held_by_pid):
                cache.delete((key, UPDATING))
                logger.warning(
                    f"Deleting stale lock for cache key {key!r} (pid={lock_held_by_pid}."
                )
            else:
                proc = None
                for proc in psutil.process_iter():
                    if proc.pid == lock_held_by_pid:
                        break
                logger.info(
                    f"Failed to acquire lock for cache key {key!r}. "
                    f"Lock is held by process {lock_held_by_pid} "
                    f"({shlex.join(proc.cmdline()) if proc else 'unknown process'})"
                )

        return None, False

    cached = cache.get(key, default=None)
    if cached:
        soft_expire, cost, value = cached
        ttl = soft_expire - _time()
        if (cost * -log(_random())) < ttl:
            return value
        else:
            logger.info(f"TTL based refresh for key {key!r}")
            updated, success = set_value()
            if success:
                return updated
            return value
    else:
        for ix in range(retry_limit):
            logger.info(
                f"Cache miss for {key!r} (attempt {ix + 1}/{retry_limit})"
            )
            # Acquire a lock on the cache for that key
            updated, success = set_value()
            if success:
                return updated
            else:
                # Another process has the lock?
                time.sleep(0.1 * 1.65 ** ix)
                cached = cache.get(key, default=None)
                if cached:
                    return cached[-1]
        raise Exception(
            f"Could not acquire lock to regenerate cache value for {key!r}"
        )


get_or_create = partial(_get_or_create, cache, hours=1)
