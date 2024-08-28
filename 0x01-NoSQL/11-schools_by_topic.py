#!/usr/bin/env python3
"""
Module containing a function that finds schools by topic
"""

def schools_by_topic(mongo_collection, topic):
    """
    Returns the list of schools having a specific topic.

    Args:
        mongo_collection: pymongo collection object
        topic (str): The topic to search for

    Returns:
        List of dictionaries representing the schools with the specific topic
    """
    return list(mongo_collection.find({"topics": topic}))
