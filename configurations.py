import certifi
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

# Hardcoded MongoDB URI
uri = "mongodb+srv://utkarshkesharwani3:d8N5Xqob50qhDB3o@cluster0.hmyse.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri, tlsCAFile=certifi.where())

try:
    # Test the connection
    client.admin.command("ping")
    print("MongoDB connection successful")
except ConnectionFailure as e:
    print(f"MongoDB connection failed: {e}")
    raise

# Access the database and collection
db = client["student_db"]
collection = db["student_data"]
