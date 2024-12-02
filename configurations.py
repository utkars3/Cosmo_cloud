import ssl
import certifi
from pymongo.mongo_client import MongoClient

uri = "mongodb+srv://utkarshkesharwani3:d8N5Xqob50qhDB3o@cluster0.hmyse.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri, tlsCAFile=certifi.where())

try:
    client.admin.command('ping')
    print("MongoDB connection successful")
except Exception as e:
    print(f"Connection failed: {e}")

db=client.student_db
collection=db["student_data"]