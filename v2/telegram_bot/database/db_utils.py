from pymongo import MongoClient
from config.config import mongo_uri, database_name, collection_name

# MongoDB connection
client = MongoClient(mongo_uri)
db = client[database_name]
collection = db[collection_name]


def is_existing_entry(url, username, password):
    """
    Checks if an entry with the given URL, username, and password already exists in the database.
    """
    query = {"url": url, "username": username, "password": password}
    return collection.find_one(query) is not None


def add_to_database(url, username, password):
    """
    Adds a new entry to the database if it does not already exist.
    """
    if not is_existing_entry(url, username, password):
        try:
            # Adding a new entry
            collection.insert_one({"url": url, "username": username, "password": password})
            print(f"Added to MongoDB: {url}:{username}:{password}")

        except Exception as e:
            print(f"Error adding to MongoDB: {e}")
    else:
        # If the entry already exists, do not add it again
        print(f"Entry already exists in MongoDB: {url}:{username}:{password}")


def get_channel_data_from_db():
    """
    Retrieves channel data (URLs and passwords) from MongoDB.
    """
    try:
        channels = collection.find({}, {'_id': 0, 'url': 1, 'password': 1})
        channel_data_list = [{'url': channel['url'], 'password': channel.get('password', None)} for channel in channels
                             if 'url' in channel]

        print("Fetched channel data from DB:", channel_data_list)
        return channel_data_list

    except Exception as e:
        print(f"Error fetching channel data from MongoDB: {e}")
        return []
