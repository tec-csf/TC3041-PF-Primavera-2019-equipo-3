from pymongo import MongoClient
from bson import ObjectId
from flask import request, url_for, jsonify
from backend import config

class Libros(object):

    def __init__(self):
        client = MongoClient(config.MONGO_URI)
        db = client.libros
        self.collection = db.libros


    def find(self):
        """
        Obtener todas las notas
        """
        cursor = self.collection.find()

        libros = []

        for libro in cursor:
            # Se adicionó para poder manejar ObjectID
            libro['_id'] = str(libro['_id']) 
            libros.append(libro)

        return libros

    def findOne(self, id):
        """
        Obtener la nota con id
        """
        libro = self.collection.find_one({'_id': ObjectId(id)})

        # Se adicionó para poder manejar ObjectID
        if libro is not None:
            libro['_id'] = str(libro['_id'])

        return libro


    def create(self, libro):
        """
        Insertar una nota nueva
        """
        result = self.collection.insert_one(libro)

        return result

    def delete(self, id):
        """
        Eliminar una nota
        """
        result = self.collection.delete_one({'_id': ObjectId(id)})

        return result

    def update(self, id, libro):
        """
        Actualizar una nota
        """
        result = self.collection.replace_one({'_id': ObjectId(id)}, libro )

        return result

    def findByGenre(self):
        cursor = self.collection.find()
        cursor = cursor.sort(("Genero"))
        libros = []

        for libro in cursor:
            # Se adicionó para poder manejar ObjectID
            libro['_id'] = str(libro['_id']) 
            libros.append(libro)

        return libros

    def findByAuthor(self):
        cursor = self.collection.find()
        cursor = cursor.sort(("Autor"))
        libros = []

        for libro in cursor:
            # Se adicionó para poder manejar ObjectID
            libro['_id'] = str(libro['_id']) 
            libros.append(libro)

        return libros
