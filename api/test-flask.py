from flask import Flask,jsonify,request
from flask_api import FlaskAPI, status, exceptions
from pymongo import MongoClient
from bson.objectid import ObjectId
from flask_wtf import Form
from wtforms import StringField,PasswordField
from wtforms.validators import InputRequired, Email,Length,AnyOf
from flask_cors import CORS
from flask import render_template
from flask_bootstrap import Bootstrap
from models import sessions
from datetime import datetime
from models import notes
import json
import dns
import os
SECRET_KEY = os.urandom(32)


app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
Bootstrap(app)

class LoginForm(Form):
    username = StringField('username', validators=[InputRequired(),Email(message='Invalid email.')])
    password = PasswordField('password', validators=[InputRequired(),Length(min=5,max=10)])


@app.route("/login",methods=['GET','POST'])
def index():
    form =LoginForm()
    if form.validate_on_submit():
        return 'Form Successfully!'
    return render_template('hello.html',form=form)

@app.route("/",methods=['GET'])
def get_all_tasks():
    print("hola")
    uri = "mongodb+srv://maupeon:admin@cluster0-1q1k1.mongodb.net/test?retryWrites=true"

    client = MongoClient(uri)
    db = client.tasks
    collection = db.tasks

    result = []

    for field in collection.find():
        result.append({'_id':str(field['_id']),'titulo':field['titulo'],'libro':field['libro']})

    return jsonify(result)

@app.route("/frontend",methods=['GET','POST'])
def show_front():
    return render_template('hello.html')

@app.route("/redis", methods=['GET', 'POST'])
def listas():
    redis = sessions.Sessions()
    print("debugeo",datetime.now())
    redis.add(str(datetime.now()))

    mongodb = notes.Notes()


    #if request.method == 'GET':
    note = request.data

    result = mongodb.create(note)

    # Se adicionó para poder manejar ObjectID
    note['_id'] = str(note['_id'])

    return note, status.HTTP_201_CREATED

    #return mongodb.find()
@app.route('/active_sessions', methods=['GET'])
def active_sessions():
    redis = sessions.Sessions()
    dbsize = redis.get_active_sessions()

    return jsonify({"Sesiones activas: ": dbsize})

@app.route('/libros', methods=['GET','POST'])
def show_libros():
    mongodb = notes.Notes()
    libros = mongodb.find()
    #print(type(libros))
    
    #print(libros[0]['libro'])
    libros_array = []
    for i in range(len(libros)):
        libros_array.append(libros[i]['libro'])
    
    print(libros_array)

    return render_template('libros.html',libro=libros_array)




if __name__ == "__main__":
    app.run(debug=True)
