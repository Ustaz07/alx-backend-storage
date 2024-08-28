#!/usr/bin/env python3
"""
Provide stats about Nginx logs stored in MongoDB.
Database: logs, Collection: nginx.

Displays:
- Total number of logs
- Number of logs for each HTTP method
- Number of logs with method GET and path /status
- Top 10 most present IPs in the collection
"""

from pymongo import MongoClient

METHODS = ["GET", "POST", "PUT", "PATCH", "DELETE"]

# Aggregation pipeline to find the top 10 most present IPs
TOP_IPS_PIPELINE = [
    {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
    {"$sort": {"count": -1}},
    {"$limit": 10}
]

def log_stats(mongo_collection):
    """
    Provides stats about Nginx logs stored in the MongoDB collection.

    Args:
        mongo_collection: The pymongo collection object.
    """
    # Count total number of logs
    total_logs = mongo_collection.count_documents({})
    print(f"{total_logs} logs")

    # Count logs by HTTP method
    print("Methods:")
    for method in METHODS:
        count = mongo_collection.count_documents({"method": method})
        print(f"\tmethod {method}: {count}")

    # Count logs with method GET and path /status
    status_check = mongo_collection.count_documents({"method": "GET", "path": "/status"})
    print(f"{status_check} status check")

    # Display the top 10 most present IPs
    print("IPs:")
    for ip in mongo_collection.aggregate(TOP_IPS_PIPELINE):
        print(f"\t{ip.get('_id')}: {ip.get('count')}")

if __name__ == "__main__":
    # Connect to the MongoDB server and access the 'nginx' collection in the 'logs' database
    client = MongoClient('mongodb://127.0.0.1:27017')
    nginx_collection = client.logs.nginx

    # Call the log_stats function with the collection
    log_stats(nginx_collection)
