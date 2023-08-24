from flask import render_template, redirect, request, url_for, flash, session, send_file

from app import tryton
from app.base import blueprint
from app.base.forms import Formulario
from app.auth.routes import login_required

from trytond.transaction import Transaction

from functools import wraps
from datetime import datetime

from io import BytesIO

WebUser = tryton.pool.get('web.user')
Session = tryton.pool.get('web.user.session')
Inscription = tryton.pool.get('aet_web.inscription')
CityCategory = tryton.pool.get('aet_web.city.category')
Category = tryton.pool.get('aet_web.category')

#### objetos para testing
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

data=[]

data1 = daata("casados con hijos","canal1", "la paz", "atp", "comedia" ,1 ,1 ,0)
data2 = daata("casados ","canal1", "la paz", "atp", "comedia" ,0 ,0,1)
data3 = daata(" hijos","canal1", "la paz", "atp", "comedia" ,1,0,1)
data4 = daata("asd","canal1", "la paz", "atp", "comedia" ,0,1,0)

data.append(data1)
data.append(data2)
data.append(data3)
data.append(data4)

#####

@blueprint.route('/formulario', methods = ['GET','POST'])
def formulario():
    if request.method == 'POST':
        return "all ok"
    else:
        return "mal"

@blueprint.route('/inscripcion', methods = ['GET','POST'])
@tryton.transaction(readonly=False, user=1)
def inscripcion():
    genres = []
    categories = []
    cat_asociados = CityCategory.search([('category.type', '=', 'associated')])
    cat_abiertos = CityCategory.search([('category.type', '=', 'open')])
    cat_prod_indep = CityCategory.search([('category.type', '=', 'independent')])
    cat_unica = CityCategory.search([('category.type', '=', 'unique')])
    cat_turf = CityCategory.search([('category.type', '=', 'turf')])

    with Transaction().set_context(language='es'):
        categories = Category.fields_get(['type'])['type']['selection']
        genres = Inscription.fields_get('genre')['genre']['selection']

    if request.method == 'POST':
        print(20*'*', request.form)
        inscription, = Inscription.create([{
            'name': request.form['programa'] or None,
            'category': request.form['categoria'],
            'genre': request.form['genero'],
            'live': request.form['vivo'],
            'city_of_emission': request.form['localidad'] or None,
            'date_of_emission': request.form['fecha'] \
                and datetime.strptime(request.form['fecha'], '%Y-%m-%d').date() or None,
            'duration': request.form['duracion'] or None,
            'description': request.form['otros'] or None,
            'video_long1': request.form['video1'] or None,
            'video_long2': request.form['video2'] or None,
            'video_long3': request.form['video3'] or None,
            'video_short': request.form['cover'] or None,
            'producer': request.form['productor'] or None,
            'co_producer': request.form['coproduccion'] or None,
            'author': request.form['autor'] or None,
            'editor': request.form['editor'] or None,
            'director': request.form['director'] or None,
            'cameraman': request.form['camara'] or None,
            'musician': request.form['sonido'] or None,
            'host': request.form['conductor'] or None,
            'protagonist': request.form['protagonista'] or None,
            'chroniclers': request.form['cronistas'] or None,
            'channel_name': request.form['canal'] or None,
            'address_channel': request.form['direccion'] or None,
            'channel_town': request.form['localidad_canal'] or None,
            'channel_contact': request.form['contacto'] or None,
            'channel_phone': request.form['telefono'] or None,
            'channel_email': request.form['email'] or None,
            'aet_partner': request.form['socio'],
            'business_name': request.form['razonsocial'] or None,
            'cuit': request.form['cuit'] and int(request.form['cuit']) or None,
            'inscription_date': datetime.now(),
            }])
        return render_template('/page-1.html')
    else:
        return render_template('/inscripcion.html',
                categories=categories,
                    cat_asociados=cat_asociados,
                    cat_abiertos=cat_abiertos,
                    cat_prod_indep=cat_prod_indep,
                    cat_unica=cat_unica,
                    cat_turf=cat_turf,
                genres=genres)

@blueprint.route('/download_instructivo')
@tryton.transaction()
def render_instructivo():
    Instruction = tryton.pool.get('aet_web.instruction.report', type='report')
    ext, content, _, name = Instruction.execute([], {})
    print(ext, content, _, name)
    return send_file(
        BytesIO(content),
        attachment_filename='instructivo.pdf')


@blueprint.route('/paginajurados/<id_>')
@tryton.transaction()
@login_required
def jurados(id_=None):
    inscription, = Inscription.search([('id', '=', int(id_))],
                                      limit=1)
    inscriptions = Inscription.search([('id', '>', 0)])
    print(inscription)
    return render_template('/paginajurados.html',
                           usuarios=len(inscriptions),
                           programa=inscription.name,
                           genero=inscription.genre_string,
                           categoria=inscription.category.rec_name,
                           vivo=inscription.live,
                           localidad=inscription.channel_town,
                           emision=inscription.city_of_emission,
                           duracion=inscription.duration,
                           productor=inscription.producer,
                           coproductor=inscription.co_producer,
                           autor=inscription.author,
                           director=inscription.director,
                           camara=inscription.cameraman,
                           sonido=inscription.musician,
                           conductor=inscription.host,
                           protagonista=inscription.protagonist,
                           cronistas=inscription.chroniclers,
                           otros="no se encuentra este campo",
                           nombre=inscription.channel_name,
                           direccion=inscription.address_channel,
                           localidad_canal=inscription.channel_town,
                           contacto=inscription.channel_contact,
                           telefono=inscription.channel_phone,
                           email=inscription.channel_email,
                           socio=inscription.aet_partner,
                           razonsocial=inscription.business_name,
                           cuit=inscription.cuit,
                           observacion=inscription.description,
                           estado="estado ok" if inscription.enrolled else "faltan revisar campos por el administrador",
                           cover=inscription.video_short,
                           programa1=inscription.video_long1,
                           programa2=inscription.video_long2,
                           programa3=inscription.video_long3,
                           )

@blueprint.route('/paginajurados')
@blueprint.route("/listado")
@blueprint.route("/listado/<categoria>")
@tryton.transaction()
@login_required
def show_category(categoria=None):
    inscriptos = []
    if categoria == "a":
        inscriptos = Inscription.search([('category.category.name','=', "CATEGORÍA A")])
    elif categoria == "b":
        inscriptos = Inscription.search([('category.category.name','=', "CATEGORÍA B")])
    elif categoria == "c":
        inscriptos = Inscription.search([('category.category.name','=', "CATEGORÍA C")])
    elif categoria == "d":
        inscriptos = Inscription.search([('category.category.name','=', "CATEGORÍA D")])
    elif categoria == "e":
        inscriptos = Inscription.search([('category.category.name','=', "CATEGORÍA E")])
    elif categoria == "f":
        inscriptos = Inscription.search([('category.category.name','=', "CATEGORÍA F")])
    elif categoria == "vivo":
        inscriptos = Inscription.search([('category.category.name','=', "TRANSMISIONES EN VIVO")])
    elif categoria == "turf":
        inscriptos = Inscription.search([('category.category.name','=', "TURF")])
    else:
        inscriptos = Inscription.search([('id','>',0)])
        return render_template("listado.html", inscriptos=inscriptos, usuarios=len(inscriptos))
    return render_template("listado.html", inscriptos=inscriptos, usuarios=len(inscriptos))
