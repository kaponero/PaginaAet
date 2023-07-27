from flask import Flask, request, render_template
import form 
app = Flask(__name__) 

@app.route('/') 
def inicio(): 
    return render_template('/index.html') 

@app.route('/formulario', methods = ['GET','POST']) 
def formulario():
    if request.method == 'POST':
        pass
    else:
        return render_template('/formulario google.html')

@app.route('/inscripcion', methods = ['GET','POST'])   
def inscripcion(): 
    if request.method == 'POST':
        nom = request.form['programa']
        #cat = request.form['categoria']
        fecha = request.form['fecha']
        dura  = request.form['duracion']
        vid = request.form['video']
        print(nom)
        print(vid)
        print(fecha)
        print(dura)
    else:
        return render_template('/inscripcion.html')
    return render_template('/inscripcion.html')

@app.route('/paginajurados') 
def jurados(): 
    return render_template('/paginajurados.html', 
                           programa="programa_largo", 
                           genero="genero",
                           categoria="categoria",
                           vivo="vivo",
                           localidad="localidad",
                           emision="emision",
                           duracion="duracion",
                           productor="productor",
                           coproductor="coproductor", 
                           autor="autor", 
                           director="director", 
                           camara="camara", 
                           sonido="sonido", 
                           conductor="conductor", 
                           protagonista="protagonista", 
                           cronistas="cronistas", 
                           otros="otros",
                           nombre="nombre",
                           direccion="direccion",
                           localidad_canal="localidad canal",
                           contacto="contacto",
                           telefono="telefono",
                           email="email",
                           socio="socio"
                           ) 

@app.route('/login') 
def loguin(): 
    return render_template('/login2.html') 

if __name__ == '__main__':
    app.run('127.0.0.1', 5000, debug=True) 

