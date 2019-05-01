from flask import Flask,jsonify,request,make_response,redirect,url_for,render_template
from flask_api import FlaskAPI, status, exceptions
from bson.objectid import ObjectId
from flask_wtf import Form
from wtforms import StringField,PasswordField
from wtforms.validators import InputRequired, Email,Length,AnyOf
from .models import sessions
from datetime import datetime
from .models import libros




class LoginForm(Form):
    username = StringField('username', validators=[InputRequired(),Email(message='Invalid email.')])
    password = PasswordField('password', validators=[InputRequired(),Length(min=5,max=15)])

class API(object):
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

