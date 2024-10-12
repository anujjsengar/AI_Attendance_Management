import pymongo
from urllib.parse import quote_plus

username = "anujjsengar"
password = "Anuj@082004"

encoded_username = quote_plus(username)
encoded_password = quote_plus(password)

connection_string = f"mongodb+srv://{encoded_username}:{encoded_password}@anujjsengar.2ordy.mongodb.net/demo?retryWrites=true&w=majority"

client = pymongo.MongoClient(connection_string)

new_db = client["Project"]
new_collection = new_db["admin"]

user_input_username = input("Enter a unique username: ")
user_input_password = input("Enter your password: ")

if new_collection.find_one({"username": user_input_username}):
    print("Error: Username already exists. Please choose a different username.")
else:
    sample_document = {
        "username": user_input_username,
        "password": user_input_password,
    }
    new_collection.insert_one(sample_document)
    print("New database and collection created successfully!")
    print("Inserted document:", sample_document)

documents = new_collection.find()
print("\nAll users in the collection:")
for doc in documents:
    print(doc)
