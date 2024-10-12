from flask import Flask,render_template,request,redirect,url_for,flash
import pymongo
from urllib.parse import quote_plus
database_username = "anujjsengar"
database_password = "Anuj@082004"

encoded_username_database = quote_plus(database_username)
encoded_password_database = quote_plus(database_password)

connection_string = f"mongodb+srv://{encoded_username_database}:{encoded_password_database}@anujjsengar.2ordy.mongodb.net/demo?retryWrites=true&w=majority"

client = pymongo.MongoClient(connection_string)

new_db = client["Project"]
new_collection = new_db["admin"]
app=Flask(__name__)
@app.route('/')
def index():
    return render_template('admin_login.html')
@app.route('/validate_admin',methods=['GET','POST'])
def validate_admin():
    def check_user_credentials(input_username,input_password):
        user=new_collection.find_one({"username":input_username,"password":input_password})
        return user is not None

    if(request.method=="POST"):
        username = request.form.get('username')
        password = request.form.get("password")
        if(check_user_credentials(username,password)):
            print("Login Successfully!")
            return render_template('success.html')
        else:
            print("Invalid!")
            return render_template('unsuccess.html')
    
if __name__ == '__main__':
    app.run(debug=True)
