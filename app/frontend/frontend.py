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

@app.route('/menu', methods=['GET','POST'])
def menu():
    if request.method == 'POST':
        language = request.form.get('nm')
        framework = request.form.get('framework')
        
    jsons = api.API()
    jsons = jsons.get_all_tasks()
    print("perro",request.environ.get('HTTP_X_REAL_IP', request.remote_addr))

    libros_array = []
    titulos_array = []
    images_array =[]
    print
    for i in range(len(jsons)):
        libros_array.append(jsons[i]['Libro'])
        titulos_array.append(jsons[i]['Titulo'])
        images_array.append(jsons[i]['Imagen'])
    
    
    browser = request.form.get("nm")
    print("browser",browser)
    #print(images_array)
   
    return render_template('index.html',libros=libros_array,titulos=titulos_array,imagenes=images_array)



if __name__ == "__main__":
    app.run(debug=True)
