from flask import Flask,render_template,request,redirect,url_for,flash
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
fs=fs = gridfs.GridFS(new_db)
student= new_db["student"]
app=Flask(__name__)
@app.route('/')
def index():
    return render_template('new_student.html')
@app.route('/new_student',methods=['GET','POST'])
def new_student():
    if(request.method=="POST"):
        Student_ID = "22155000228"
        Student_Name = request.form.get('Name')
        Father_Name = request.form.get("Father")
        Phone=request.form.get("Mobile")
        Profile_Pic=request.files["photo"]
        image_id = fs.put(Profile_Pic, filename=Profile_Pic.filename)
        new_collection={
            "Student_ID": Student_ID,
            "Student_Name": Student_Name,
            "Father_Name": Father_Name,
            "Phone": Phone,
            "Image": image_id
        }
        student.insert_one(new_collection)
        print("SuccessFully Register")
    return render_template("success.html")
if __name__ == '__main__':
    app.run(debug=True)
