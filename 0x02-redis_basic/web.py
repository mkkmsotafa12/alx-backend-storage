#!/usr/bin/env python3
""" Implementing an expiring web cache and tracker """
import requests
from functools import wraps
from redis import Redis
from typing import Callable
db = Redis()


def cache_countVisited(method: Callable) -> Callable:
    """ Function that caches the number of requests """
    @wraps(method)
    def wrapper(url):
        """ Wrapper for the function """
        key = f'count:{url}'
        db.incr(key)
        if db.get(f'result:{url}'):
            return db.get(f'result:{url}').decode('utf-8')
        result = method(url)
        db.setex(f'result:{url}', 10, result)
        return result
    return wrapper


@cache_countVisited
def get_page(url: str) -> str:
    """ Return response of request """
    req = requests.get(url)
    return req.text
