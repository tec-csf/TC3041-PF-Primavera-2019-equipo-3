from flask import Flask,jsonify,request,make_response,redirect,url_for,render_template
from flask_api import FlaskAPI, status, exceptions
from bson.objectid import ObjectId
from flask_wtf import Form
from wtforms import StringField,PasswordField
from wtforms.validators import InputRequired, Email,Length,AnyOf
from .models import sessions
from datetime import datetime
from .models import libros, usuarios




class LoginForm(Form):
    username = StringField('username', validators=[InputRequired(),Email(message='Invalid email.')])
    password = PasswordField('password', validators=[InputRequired(),Length(min=5,max=15)])    

class API(object):

    def update_user(self,user,password):
        red = sessions.Sessions()
        red.set_user(user,password)



    def verify_password(self,user,password):
        red = sessions.Sessions()

        hashedPassword = red.hashed_pass(password)

        redisPassword = red.get_user_password(user)
        
        if(redisPassword != None):
            print("Romel")
            

            if redisPassword.decode() == hashedPassword:
              print(redisPassword.decode(),hashedPassword)
              return True
            return False  
        return False

    def insert_user(self,user,password,nombre,apellido,email):
         red = sessions.Sessions()
         mongodb = usuarios.Usuarios()

         #red.set_user(user,password)
         #mongodb.insert_user(user,nombre,apellido,email)   

    def get_user_books(self,user):
        mongodb = libros.Libros()


    def get_all_tasks(self):
        mongodb = libros.Libros()
        libs = mongodb.find()  

        return libs

    def get_all_tasks_by_genre(self):
        mongodb = libros.Libros()
        libs = mongodb.findByGenre()  

        return libs

    def get_all_tasks_by_author(self):
        mongodb = libros.Libros()
        libs = mongodb.findByAuthor()  

        return libs

    def get_all_users(self):
        mongodb = usuarios.Usuarios()
        users = mongodb.find()  

        return users

