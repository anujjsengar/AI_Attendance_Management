from flask import Flask, render_template, request, redirect, send_file, url_for, flash
import pymongo
from pymongo import DESCENDING
import gridfs
from bson.binary import Binary
from io import BytesIO
from urllib.parse import quote_plus
from bson import ObjectId
database_username = "anujjsengar"
database_password = "Anuj@082004"
encoded_username_database = quote_plus(database_username)
encoded_password_database = quote_plus(database_password)

connection_string = (
    f"mongodb+srv://{encoded_username_database}:{encoded_password_database}"
    "@anujjsengar.2ordy.mongodb.net/demo?retryWrites=true&w=majority"
)
client = pymongo.MongoClient(connection_string)

db = client["Project"]
admin_collection = db["admin"]
student_collection = db["student_table"]
room_collection=db["Room_data"]
mapped_class_collection=db["Mapped_Class"]
fs = gridfs.GridFS(db)
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('admin_login.html')

@app.route('/validate_admin', methods=['GET', 'POST'])
def validate_admin():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get("password")

        if check_user_credentials(username, password):
            print("Login Successfully!")
            return render_template('dashboard.html')

        else:
            print("Invalid!")
            return render_template('unsuccess.html')

def check_user_credentials(input_username, input_password):
    user = admin_collection.find_one({"username": input_username, "password": input_password})
    return user is not None

@app.route('/new_student', methods=['GET', 'POST'])
def new_student():
    if request.method == "POST":
        max_roll_no = student_collection.find_one(sort=[("Roll_no", DESCENDING)])
        Roll_no = max_roll_no["Roll_no"] + 1 if max_roll_no else 1
        Student_Name = request.form.get('Name')
        Password = request.form.get("password")
        section = request.form.get("section")
        Profile_Pic = request.files["photo"]
        image_data=Binary(Profile_Pic.read())

        image_id = fs.put(Profile_Pic.read(), filename=Profile_Pic.filename)
        print("Stored image with ID:", image_id)
        new_student_data = {
            "Roll_no": Roll_no,
            "Student_Name": Student_Name,
            "Password": Password,
            "Section": section,
            "Image": image_data
        }
        student_collection.insert_one(new_student_data)

        print("Successfully Registered")
        return render_template("display_student.html", student={
            "Roll_no": Roll_no,
            "Student_Name": Student_Name,
            "Password": Password,
            "Section": section,
            "Image": image_id
        })

    return render_template("unsuccess.html")
@app.route('/get_image/<image_id>')
def get_image(image_id):
    try:
        if(db.fs.files.find({ "_id": ObjectId(image_id) })):
            print("available")
        image = fs.get(ObjectId(image_id))
        return app.response_class(image.read(), mimetype='image/jpeg') 
    except gridfs.errors.NoFile:
        return "Image not found", 404

@app.route('/add_room', methods=['GET', 'POST'])
def add_room():
    if(request.method=="POST"):
        room_no=request.form.get("room_no")
        block_no=request.form.get("block_no")
        lat=request.form.get("lat")
        long=request.form.get("long")
        new_room_record={
            "room_no":room_no,
            "block_no":block_no,
            "lat":lat,
            "long":long
        }
        print(new_room_record)
        room_collection.insert_one(new_room_record)
        return render_template('unsuccess.html')
        



@app.route('/show_students')
def show_students():
    students = list(student_collection.find())
    return render_template('students_table.html', students=students)
@app.route('/add_student')
def add_student():
    return render_template('new_student.html')

@app.route('/show_student')
def show_student():
    return redirect(url_for('show_students'))
@app.route('/room_add')
def room_add():
    return render_template('Add_Room.html')
@app.route('/start_dashboard')
def start_dashboard():
    return render_template('dashboard_start.html')
@app.route('/show_rooms')
def show_rooms():
    rooms = list(room_collection.find())
    print(rooms)
    return render_template('room_table.html', rooms=rooms)

@app.route('/show_room')
def show_room():
    return redirect(url_for('show_rooms'))
@app.route('/class_map')
def class_map():
    return render_template("new_class.html")
@app.route('/mapped_class',methods=['GET','POST'])
def mapped_class():
    if(request.method=='POST'):
        max_class_id= mapped_class_collection.find_one(sort=[("Class_ID", DESCENDING)])
        class_id = max_class_id["Class_ID"] + 1 if max_class_id else 1
        Section=request.form.get('section')
        Room=request.form.get('room_no')
        date=request.form.get('date')
        time=request.form.get('time')
        map_class={
            "Class_ID":class_id,
            "Section":Section,
            "Room":Room,
            "Date":date,
            "Time":time
        }
        mapped_class_collection.insert_one(map_class)
        print(map_class)
        return render_template("display_room.html",data=map_class)
if __name__ == '__main__':
    app.run(debug=True)
