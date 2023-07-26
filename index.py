from flask import Flask, request, render_template 
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
    return render_template('/paginajurados.html', programa="Hola", genero="DEPORTIVO") 

if __name__ == '__main__':
    app.run('127.0.0.1', 5000, debug=True) 

