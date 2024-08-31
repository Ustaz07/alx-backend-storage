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
