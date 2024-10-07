import hashlib

from django.core.cache import cache
from functools import wraps
from typing import Optional


def cache_decorator(cache_name: Optional[str] = None, timeout: int = 60):
    def wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            nonlocal cache_name
            if not cache_name:
                imprint = hashlib.md5(f"{func.__name__}:{args}:{kwargs}".encode())
                cache_name = f"{func.__name__}:{imprint.hexdigest()}"

            if (cached := cache.get(cache_name)) is not None:
                return cached

            result = func(*args, **kwargs)
            cache.set(cache_name, result, timeout)
            return result

        return inner

    return wrapper
