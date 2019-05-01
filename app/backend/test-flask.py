from flask import Flask,jsonify,request,make_response,redirect,url_for
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
from models import libros
import json
import dns
import os
import jinja2
env = jinja2.Environment()
env.globals.update(zip=zip)
SECRET_KEY = os.urandom(32)


app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
Bootstrap(app)
app.jinja_env.filters['zip'] = zip

class LoginForm(Form):
    username = StringField('username', validators=[InputRequired(),Email(message='Invalid email.')])
    password = PasswordField('password', validators=[InputRequired(),Length(min=5,max=10)])


@app.route("/login",methods=['GET','POST'])
def index():
    form =LoginForm()
    if form.validate_on_submit():
        return 'Form Successfully!'
    return render_template('hello.html',form=form)



@app.route("/redis", methods=['GET', 'POST'])
def listas():
    redis = sessions.Sessions()
    print("debugeo",datetime.now())
    redis.add(str(datetime.now()))

    mongodb = libros.Libros()


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



@app.route('/menu', methods=['GET','POST'])
def menu():
    if request.method == 'POST':
        language = request.form.get('nm')
        framework = request.form.get('framework')
        
    mongodb = libros.Libros()
    libs = mongodb.find()
    
    libros_array = []
    titulos_array = []
    images_array =[]
    for i in range(len(libs)):
        libros_array.append(libs[i]['Libro'])
        titulos_array.append(libs[i]['Titulo'])
        images_array.append(libs[i]['Imagen'])
    
    #print(libros_array)
    browser = request.form.get("nm")
    print("browser",browser)
    #print(images_array)
   
    return render_template('index.html',libros=libros_array,titulos=titulos_array,imagenes=images_array)



if __name__ == "__main__":
    app.run(debug=True)
