from pymongo import MongoClient
from bson import ObjectId
from flask import request, url_for, jsonify
from backend import config

class Usuarios(object):

    def __init__(self):
        client = MongoClient(config.MONGO_URI)
        db = client.libros
        self.collection = db.usuarios


    def find(self):
        """
        Obtener todas las notas
        """
        cursor = self.collection.find()

        usuarios = []

        for usuario in cursor:
            # Se adicionó para poder manejar ObjectID
            usuario['_id'] = str(usuario['_id']) 
            usuarios.append(usuario)

        return usuarios

    def findOne(self, id):
        """
        Obtener la nota con id
        """
        usuario = self.collection.find_one({'_id': ObjectId(id)})

        # Se adicionó para poder manejar ObjectID
        if usuario is not None:
            usuario['_id'] = str(usuario['_id'])

        return usuario


    def create(self, usuario):
        """
        Insertar una nota nueva
        """
        result = self.collection.insert_one(usuario)

        return result

    def delete(self, id):
        """
        Eliminar una nota
        """
        result = self.collection.delete_one({'_id': ObjectId(id)})

        return result

    def update(self, id, usuario):
        """
        Actualizar una nota
        """
        result = self.collection.replace_one({'_id': ObjectId(id)}, usuario )

        return result

    