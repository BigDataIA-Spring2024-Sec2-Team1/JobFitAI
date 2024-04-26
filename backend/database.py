from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError

def connect_to_mongodb():
    username = 'sudarshandudhemasters'
    password = 'NRGu4wKCkJDvG9ih'
    cluster_url = 'clustersd.2b003uq.mongodb.net'
    database_name = 'jobfit'
    connection_string = f"mongodb+srv://{username}:{password}@{cluster_url}/{database_name}?retryWrites=true&w=majority&appName=clusterSD"
    try:
        client = MongoClient(connection_string)
        client.admin.command('ping')
        print("Connection established to MongoDB")
        db = client[database_name]
        return db
    except ServerSelectionTimeoutError:
        print("Server selection timeout. Could not connect to MongoDB.")
        return None
    except ConnectionFailure:
        print("Failed to connect to MongoDB. Check your connection settings.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
