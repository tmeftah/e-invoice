from flask import request

from app.main.resources import cache


def clear_cache(key_prefix):

    keys = [key for key in cache.cache._cache.keys() if key.startswith(key_prefix)]

    cache.delete_many(*keys)


def cache_json_keys():
    json_data = tuple(sorted(request.get_json().items()))
    return json_data
