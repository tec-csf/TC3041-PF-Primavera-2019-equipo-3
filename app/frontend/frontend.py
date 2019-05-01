from flask import Flask,jsonify,request,make_response,redirect,url_for,render_template
from flask_bootstrap import Bootstrap
import jinja2
from backend import api
import os
env = jinja2.Environment()
env.globals.update(zip=zip)
SECRET_KEY = os.urandom(32)


app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
Bootstrap(app)
app.jinja_env.filters['zip'] = zip


@app.route('/', methods=['GET','POST'])
def root():
    jsons = api.API()
    jsons = jsons.get_all_tasks_by_genre()
    result=[]
    print(jsons)
    for libro in jsons:
        libro['Genero'] = str(libro['Genero']) 
        result.append(libro)

    return jsonify(result)

@app.route('/menu', methods=['GET','POST'])
def menu():
    libros_array = []
    titulos_array = []
    imagenes_array =[]
    autor_array =[]
    genero_array=[]
    fecha_de_publicacion_array=[]
    descripcion_array=[]
    num_paginas_array=[]
    editorial_array=[]
    pais_array=[]
    if request.method == 'POST':
        language = request.form.get('nm')
        framework = request.form.get('framework')
        
    jsons = api.API()
    filtro = request.form.get("nm")
    print("browser",filtro)
    if filtro == 'Género':
        jsons = jsons.get_all_tasks_by_genre()
    elif filtro == 'Autor':
        jsons = jsons.get_all_tasks_by_author()
    else:
        jsons = jsons.get_all_tasks()
   
  
    for i in range(len(jsons)):
        autor_array.append(jsons[i]['Autor'])
        libros_array.append(jsons[i]['Libro'])
        titulos_array.append(jsons[i]['Titulo'])
        imagenes_array.append(jsons[i]['Imagen'])
        genero_array.append(jsons[i]['Genero'])
        fecha_de_publicacion_array.append(jsons[i]['Fecha_de_Publicacion'])
        descripcion_array.append(jsons[i]['Descripcion'])
        num_paginas_array.append(int(jsons[i]['numPaginas']))
        editorial_array.append(jsons[i]['Editorial'])
        pais_array.append(jsons[i]['Pais'])
    
    
    
    #print(images_array)
   
    return render_template('index.html',autores= autor_array, libros=libros_array,titulos=titulos_array,
                            imagenes=imagenes_array, generos=genero_array,
                            fechas=fecha_de_publicacion_array,descripciones=descripcion_array,
                            num_paginas=num_paginas_array,editoriales = editorial_array,
                            paises=pais_array,filtro = filtro)



if __name__ == "__main__":
    app.run(debug=True)