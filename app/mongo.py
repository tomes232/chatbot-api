from pymongo import MongoClient
import gridfs
import base64

from app.load import FileJson

import os




def get_client(username:str = "tomes232", password:str = "password"):
    #connect to MongoDB
    client = MongoClient(f"mongodb+srv://{username}:{password}@chat-bot.nuh0hux.mongodb.net/?retryWrites=true&w=majority")

    return client

def get_database(client, database_name:str = "chat-bot"):
    #create/connect to database
    db = client[database_name]

    return db

def get_collection(db, collection_name:str = "files"):
    #create/connect to collection
    collection = db[collection_name]

    return collection

def get_document(collection):
    #get file from collection
    return collection.find_one()

def insert_document(collection, document):
    #insert document into collection
    collection.insert_one(document)

def write_file(database, path, filename):
    #insert file into collection with gridfs
    fs = gridfs.GridFS(database)
    with open(os.path.join(path,filename), "rb") as f:
        encoded_string = base64.b64encode(f.read())
    with fs.new_file(
        chunkSize=800000,
        filename=filename) as fp:
        fp.write(encoded_string)

def read_file(database, filename, path="./pdfs/"):
    # Usual setup
    fs = gridfs.GridFS(database)
    # Standard query to Mongo
    data = fs.find_one(filter=dict(filename=filename))
    with open(os.path.join(path, filename), "wb") as f:

        f.write(base64.b64decode(data.read()))
        





def main():
    # print("getting client...")
    # client = get_client("********", "********")
    # db = get_database(client)
    # collection = get_collection(db, "reume12_23")
    # insert_document(collection, {"name": "test"})
    # print("writing file...")
    # write_file(db, "pdfs/", "Thomas Pickup Resume 12_23.pdf")
    # print("reading file...")
    # read_file(db, "Thomas Pickup Resume 12_23.pdf")
    
    # loading resume from json file into database
    # print("loading resume into json...")
    # resume = FileJson('resume.json', load=True)
    # print("writing resume...")
    # insert_document(collection, resume.get_dict())
    pass


if __name__ == "__main__":
    main()