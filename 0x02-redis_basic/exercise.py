#!/usr/bin/env python3
"""
This defines a Cache class for storing data in Redis with random keys.
"""

import redis
import uuid
from typing import Union


class Cache:
    """
    Cache class to handle data storage in Redis.
    """

    def __init__(self):
        """
        Init. Cache class, setting up the Redis client & database.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store the given data in Redis using a randomly generated key.

        Args:
            data (Union[str, bytes, int, float]): The data to be stored.

        Returns:
            str: The key under which the data was stored.
        """
        key = str(uuid.uuid4())  # Gen a random UUID key
        self._redis.set(key, data)  # Store data in Redis form.
        return key


#!/usr/bin/env python3
"""
This module defines a Cache class for storing and retrieving data from Redis with type recovery.
"""

import redis
import uuid
from typing import Union, Callable, Optional


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

#!/usr/bin/env python3
"""
This module defines a Cache class for storing and retrieving data from Redis with type recovery.
It includes a decorator to count method calls.
"""

import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps


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
        """
        Wrapper function that increments the call count in Redis and calls the original method.
        """
        # Increment the count of method calls in Redis using the method's qualified name as the key
        self._redis.incr(method.__qualname__)
        # Call the original method and return its result
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
