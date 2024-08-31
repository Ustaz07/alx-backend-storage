#!/usr/bin/env python3
"""
Module for implementing an expiring web cache and tracker using Redis.
"""

import redis
import requests
from typing import Callable
from functools import wraps


# Initialize Redis client
redis_client = redis.Redis()


def cache_page(method: Callable) -> Callable:
    """
    A decorator that caches the result of a function with an expiration time and tracks access counts.

    Args:
        method (Callable): The function to be decorated.

    Returns:
        Callable: The wrapped function with caching and counting functionality.
    """
    @wraps(method)
    def wrapper(url: str) -> str:
        # Define the Redis keys for counting and caching
        count_key = f"count:{url}"
        cache_key = f"cache:{url}"

        # Increment the count of URL accesses
        redis_client.incr(count_key)

        # Check if the page content is cached
        cached_content = redis_client.get(cache_key)
        if cached_content:
            return cached_content.decode('utf-8')

        # Fetch the page content using the original method
        content = method(url)

        # Cache the content with an expiration time of 10 seconds
        redis_client.setex(cache_key, 10, content)

        return content

    return wrapper


@cache_page
def get_page(url: str) -> str:
    """
    Fetch the HTML content of the specified URL.

    Args:
        url (str): The URL to fetch the HTML content from.

    Returns:
        str: The HTML content of the URL.
    """
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.text
