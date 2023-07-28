from flask import render_template, redirect, request, url_for, flash, session

from app import tryton
from app.base import blueprint
from app.base.forms import LoginForm, Formulario

from functools import wraps

WebUser = tryton.pool.get('web.user')
Session = tryton.pool.get('web.user.session')

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        session_key = None
        if 'session_key' in session:
            session_key = session['session_key']
        user = Session.get_user(session_key)
        if not user:
            return redirect(url_for('login', next=request.path))
        return func(*args, **kwargs)
    return wrapper


@blueprint.route('/formulario', methods = ['GET','POST'])
def formulario():
    if request.method == 'POST':
        pass
    else:
        return render_template('/formulario_google.html')

@blueprint.route('/inscripcion', methods = ['GET','POST'])
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

@blueprint.route('/paginajurados')
def jurados():
    return render_template('/paginajurados.html',
                           usuarios=100,
                           programa="Hello World",
                           genero="comedia fantastica",
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
                           otros="otros locos",
                           nombre="nombre",
                           direccion="direccion",
                           localidad_canal="localidad canal",
                           contacto="contacto",
                           telefono="telefono",
                           email="email",
                           socio="socio",
                           razonsocial="razon social",
                           cuit="cuit",
                           observacion="observacion 1",
                           estado="estado ok",
                           cover="https://drive.google.com/file/d/1XBPO992XLspRVgePVEV5_dIN9JiXHbfj/preview",
                           programa1="https://drive.google.com/file/d/1XBPO992XLspRVgePVEV5_dIN9JiXHbfj/preview",
                           programa2="https://drive.google.com/file/d/1XBPO992XLspRVgePVEV5_dIN9JiXHbfj/preview",
                           programa3="https://drive.google.com/file/d/1XBPO992XLspRVgePVEV5_dIN9JiXHbfj/preview"
                           )

@blueprint.route('/login')
def loguin():
    return render_template('/login2.html')

data=[]

class daata():
    def __init__(self, programa, canal, localidad, categoria, genero, estado, pago): 
        self.programa = programa
        self.canal = canal
        self.localidad = localidad
        self.categoria = categoria
        self.genero = genero
        self.estado = estado
        self.pago = pago


data1 = daata("casados con hijos","canal1", "la paz", "atp", "comedia" ,1 ,0)
data2 = daata("casados ","canal1", "la paz", "atp", "comedia" ,0 ,1)
data3 = daata(" hijos","canal1", "la paz", "atp", "comedia" ,1,1)
data4 = daata("asd","canal1", "la paz", "atp", "comedia" ,0,0)

data.append(data1)
data.append(data2)
data.append(data3)
data.append(data4)


@blueprint.route("/listado")
def hello_world():
    return render_template("listado.html", dataRegistros=data, usuarios=100)


