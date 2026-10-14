"""Tiny fixed-window rate limiter on top of Django's cache."""

from django.core.cache import cache

WINDOW_SECONDS = 3600


def allow(key, limit, window=WINDOW_SECONDS):
    """Record a hit against `key`. True while the count within `window` stays at or under `limit`."""
    cache_key = f'throttle:{key}'
    if cache.add(cache_key, 1, window):
        return True
    try:
        count = cache.incr(cache_key)
    except ValueError:  # expired between add and incr
        return True
    return count <= limit
