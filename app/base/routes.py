from flask import render_template, redirect, request, url_for, flash, session

from app import tryton
from app.base import blueprint
from app.base.forms import LoginForm, Formulario

from trytond.transaction import Transaction
from functools import wraps


WebUser = tryton.pool.get('web.user')
Session = tryton.pool.get('web.user.session')
Inscription = tryton.pool.get('aet_web.inscription')

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
        return "all ok"
    else:
        return "mal"


@blueprint.route('/inscripcion', methods = ['GET','POST'])
@tryton.transaction(readonly=False, user=1)
def inscripcion():
    categories = []
    genres = []
    cat_asociados = ['CATEGORÍA A', 'CATEGORÍA B', 'CATEGORÍA C', 'CATEGORÍA D']
    cat_abiertos = ['CATEGORÍA E']
    cat_prod_indep = ['CATEGORÍA E']
    cat_unica = ['TRANSMISIONES EN VIVO']
    cat_turf = ['TURF']

    with Transaction().set_context(language='es'):
        categories = Inscription.fields_get(['category'])['category']['selection']
        genres = Inscription.fields_get('genre')['genre']['selection']
    
    if request.method == 'POST':
        print(request.form)
        inscription, = Inscription.create([{
            'name': request.form['programa'],
            'category': request.form['categoria'],
            'genre': request.form['genero'],
            'live': request.form['vivo'],
            'city_of_emission': request.form['localidad'],
            'date_of_emission': request.form['fecha'],
            'duration': request.form['duracion'],
            'description': request.form['otros'],
            'video_long1': request.form['video1'],
            'video_long2': request.form['video2'],
            'video_long3': request.form['video3'],
            'video_short': request.form['cover'],
            'producer': request.form['productor'],
            'co_producer': request.form['coproduccion'],
            'author': request.form['autor'],
            'editor': request.form['editor'],
            'director': request.form['director'],
            'cameraman': request.form['camara'],
            'musician': request.form['sonido'],
            'host': request.form['conductor'],
            'protagonist': request.form['protagonista'],
            'chroniclers': request.form['cronistas'],
            'channel_name': request.form['canal'],
            'address_channel': request.form['direccion'],
            'channel_town': request.form['localidad_canal'],
            'channel_contact': request.form['contacto'],
            'channel_phone': request.form['telefono'],
            'channel_email': request.form['email'],
            'aet_partner': request.form['socio'],
            'business_name': request.form['negocio'],
            'cuit': request.form['cuit'],
            'enrolled': request.form['razonsocial'],
            }])
    else:
        return render_template('/inscripcion.html',
                categories=categories,
                    cat_asociados=cat_asociados,
                    cat_abiertos=cat_abiertos,
                    cat_prod_indep=cat_prod_indep,
                    cat_unica=cat_unica,
                    cat_turf=cat_turf,
                genres=genres)
    
    return render_template('/inscripcion.html',
                categories=categories,
                    cat_asociados=cat_asociados,
                    cat_abiertos=cat_abiertos,
                    cat_prod_indep=cat_prod_indep,
                    cat_unica=cat_unica,
                    cat_turf=cat_turf,
                genres=genres)

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
    def __init__(self, programa, canal, localidad, categoria, genero, estado, revisado, pago): 
        self.programa = programa
        self.canal = canal
        self.localidad = localidad
        self.categoria = categoria
        self.genero = genero
        self.estado = estado
        self.revisado = revisado
        self.pago = pago


data1 = daata("casados con hijos","canal1", "la paz", "atp", "comedia" ,1 ,1 ,0)
data2 = daata("casados ","canal1", "la paz", "atp", "comedia" ,0 ,0,1)
data3 = daata(" hijos","canal1", "la paz", "atp", "comedia" ,1,0,1)
data4 = daata("asd","canal1", "la paz", "atp", "comedia" ,0,1,0)

data.append(data1)
data.append(data2)
data.append(data3)
data.append(data4)


@blueprint.route("/listado")
def hello_world():
    return render_template("listado.html", dataRegistros=data, usuarios=100)


