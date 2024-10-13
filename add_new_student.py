import pymongo
import gridfs
from urllib.parse import quote_plus

database_username = "anujjsengar"
database_password = "Anuj@082004"

encoded_username_database = quote_plus(database_username)
encoded_password_database = quote_plus(database_password)

connection_string = f"mongodb+srv://{encoded_username_database}:{encoded_password_database}@anujjsengar.2ordy.mongodb.net/demo?retryWrites=true&w=majority"

client = pymongo.MongoClient(connection_string)

new_db = client["Project"]
new_collection = new_db["student"]

fs = gridfs.GridFS(new_db)

"""roll_no = input("Enter Student ID: ")
name = input("Enter Student Name: ")
father_name = input("Enter Father's Name: ")
contact = input("Enter Phone Number: ")
image_path = "profile.jpg"

with open(image_path, "rb") as image_file:
    image_id = fs.put(image_file, filename="profile.jpg")

sample_document = {
    "Student_ID": roll_no,
    "Student_Name": name,
    "Father_Name": father_name,
    "Phone": contact,
    "Image": image_id
}

new_collection.insert_one(sample_document)
print("Student record with image inserted successfully!")

def retrieve_image(image_id):
    image_data = fs.get(image_id)
    with open("retrieved_profile.jpg", "wb") as output_file:
        output_file.write(image_data.read())
    print("Image retrieved and saved as 'retrieved_profile.jpg'.")

doc = new_collection.find_one({"Student_ID": roll_no})
if doc and "Image" in doc:
    retrieve_image(doc["Image"])
else:
    print("No image found for this student.")"""
documents = new_collection.find()
print("\nAll users in the collection:")
for doc in documents:
    print(doc)
