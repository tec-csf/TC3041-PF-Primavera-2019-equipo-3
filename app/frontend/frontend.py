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

@app.route('/login', methods=['GET','POST'])
def login():

    a = api.API()
    if request.method == 'POST':
        user = request.form.get('username')
        print("agap",user)
        password = request.form.get('password')
        print("agap",password)

        if(a.verify_password(user,password)):
             print("correcto")
        else:
            print("incorrecto")


    
    return render_template('login.html')

@app.route('/registro', methods=['POST','GET'])
def registro():

    a = api.API()
    if request.method == 'POST':

        user = request.form.get('username')
        print("agap",user)
        password = request.form.get('password')
        print("agap",password)
        name = request.form.get('Name')
        print("agap",name)
        lastName = request.form.get('Lastname')
        print("agap",lastName)
        email = request.form.get('Email')
        print("agap",email)

        if(len(user)>0 and len(password)>0 and len(name)>0 and len(lastName)>0 and len(email)>0):
           a.insert_user(user,password,name,lastName,email)
           print("lleno")
        else:
           print("no lleno") 
    
     
    return render_template('registro.html')



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

    jsons = api.API()
    usuarios_array = jsons.get_all_users()

    
    if request.form.get("filt"):
        filtro = request.form.get("filt")
        bandera = 1
    elif request.form.get("aut"):
        filtro = request.form.get("aut")
        bandera = 2
    else:
        bandera = 0
        filtro = 'None'
    bandera = str(bandera)
    print("browser",filtro,bandera)

    
    jsons = jsons.get_all_tasks()
    #print(type(jsons))
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
    
    generos_limpios = []
    autores_limpios = []
    for genero in genero_array:
        if genero not in generos_limpios:
            generos_limpios.append(genero)
    for autor in autor_array:
        if autor not in autores_limpios:
            autores_limpios.append(autor)
    print(autores_limpios)
    
    #print(images_array)
   
    return render_template('index.html',autores= autor_array, libros=libros_array,titulos=titulos_array,
                            imagenes=imagenes_array, generos=genero_array,
                            fechas=fecha_de_publicacion_array,descripciones=descripcion_array,
                            num_paginas=num_paginas_array,editoriales = editorial_array,
                            paises=pais_array,filtro = filtro,usuarios=usuarios_array,
                            generoslimpios=generos_limpios,autoreslimpios=autores_limpios,bandera=bandera)



if __name__ == "__main__":
    app.run(debug=True)
