#!/usr/bin/env python3
""" Store data file """
import redis
import uuid
from functools import wraps
from typing import Union, Optional, Callable


def count_calls(method: Callable) -> Callable:
    """ Decorator to count a function """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """ wrapper function """
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """ Call history function """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """ Wrapper function """
        nput = method.__qualname__ + ':inputs'
        output = method.__qualname__ + ':outputs'
        self._redis.rpush(nput, str(args))
        returned_value = method(self, *args, **kwargs)
        self._redis.rpush(output, returned_value)
        return returned_value
    return wrapper


def replay(method: Callable):
    """ Replay function to display function history """
    cache = redis.Redis()
    name = method.__qualname__
    nput = name + ':inputs'
    output = name + ':outputs'
    nput_list = cache.lrange(nput, 0, -1)
    output_list = cache.lrange(output, 0, -1)
    combined_list = list(zip(nput_list, output_list))
    print(f'{name} was called {len(combined_list)} times:')
    for key, value in combined_list:
        print(f"{name}(*{key.decode('utf-8')}) -> \
{value.decode('utf-8')}")


class Cache:
    """ Class to cache """
    def __init__(self):
        """ Instantiate a class """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
            stores date
            Args:
                data: passed data to be stored
            Return - random key used to store data
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> Union[str,
                                                                    bytes,
                                                                    int,
                                                                    float]:
        """
            Get stored value
            Args:
                Key: key for value stored to retrieve
                Fn: callable of a function
            Return - data stored
        """
        value = self._redis.get(key)
        if fn:
            value = fn(value)
        return value

    def get_str(self, key: str) -> str:
        """ Parametrize Cache.get with string conversion """
        return self.get(key, lambda val: val.decode('utf-8'))

    def get_int(self, key: str) -> int:
        """ Parametrize Cache.get with int conversion """
        return self.get(key, lambda val: int(val.decode('utf-8')))
