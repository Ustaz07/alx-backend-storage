#!/usr/bin/env python3
"""
This module defines a Cache class with methods for storing and retrieving data using Redis.
It includes decorators for counting method calls and tracking input-output history.
"""

import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps


def call_history(method: Callable) -> Callable:
    """
    A decorator that stores the history of inputs and outputs for a method in Redis.

    Args:
        method (Callable): The method to decorate.

    Returns:
        Callable: The wrapped method with input-output tracking functionality.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        # Define Redis keys for inputs and outputs
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"

        # Store input arguments as a string in Redis
        self._redis.rpush(input_key, str(args))

        # Call the original method and store the result
        result = method(self, *args, **kwargs)

        # Store the result of the method call in Redis
        self._redis.rpush(output_key, str(result))

        return result

    return wrapper


def count_calls(method: Callable) -> Callable:
    """
    A decorator that counts the number of times a method is called.

    Args:
        method (Callable): The method to decorate.

    Returns:
        Callable: The wrapped method with counting functionality.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        # Increment the call count in Redis
        self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)

    return wrapper


class Cache:
    """
    Cache class to handle data storage and retrieval in Redis.
    """

    def __init__(self):
        """
        Initialize the Cache class, setting up the Redis client and flushing the database.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store the given data in Redis using a randomly generated key.

        Args:
            data (Union[str, bytes, int, float]): The data to be stored.

        Returns:
            str: The key under which the data was stored.
        """
        key = str(uuid.uuid4())  # Generate a random UUID key
        self._redis.set(key, data)  # Store the data in Redis using the random key
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> Union[str, bytes, int, float, None]:
        """
        Retrieve data from Redis and optionally apply a conversion function.

        Args:
            key (str): The key of the data to retrieve.
            fn (Optional[Callable]): A callable function to apply to the retrieved data.

        Returns:
            Union[str, bytes, int, float, None]: The retrieved data, optionally converted by `fn`.
        """
        value = self._redis.get(key)
        if value is None:
            return None
        return fn(value) if fn else value

    def get_str(self, key: str) -> Optional[str]:
        """
        Retrieve a string value from Redis.

        Args:
            key (str): The key of the data to retrieve.

        Returns:
            Optional[str]: The retrieved string data, or None if the key does not exist.
        """
        return self.get(key, lambda d: d.decode('utf-8'))

    def get_int(self, key: str) -> Optional[int]:
        """
        Retrieve an integer value from Redis.

        Args:
            key (str): The key of the data to retrieve.

        Returns:
            Optional[int]: The retrieved integer data, or None if the key does not exist.
        """
        return self.get(key, int)
