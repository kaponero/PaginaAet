from flask import (render_template, redirect, request, url_for,
            flash, session, send_file, jsonify)

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
Calification = tryton.pool.get('aet_web.calification')
Partner = tryton.pool.get('aet_web.partner')

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

@blueprint.route('/tarjetas', methods = ['GET','POST'])
def formulario():
    if request.method == 'POST':
        return "all ok"
    else:
        return render_template('/tarjetas.html')

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
        inscription, = Inscription.create([{
            'inscription_number': '',
            'aet_partner': request.form['socio'] or None,
            'aet_number': request.form['num_socio'] or None,
            'name': request.form['programa'] or None,
            'category': request.form['categoria'] ,
            'genre': request.form['genero'],
            'live': request.form['vivo'],
            'city_of_emission': request.form['localidad'] or None,
            'date_of_emission': request.form['fecha'] \
                and datetime.strptime(request.form['fecha'], '%Y-%m-%d').date() or None,
            'duration': request.form['duracion'] or None,
            'description': request.form['otros'] or None,
            'routine': request.form['rutina'] or None,
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
            'business_name': request.form['razonsocial'] or None,
            'cuit': request.form['cuit'] and (request.form['cuit']) or None,
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
    return send_file(
        BytesIO(content),
        attachment_filename='instructivo.pdf')


@blueprint.route('/paginajurados/<id_>', methods = ['GET', 'POST'])
@tryton.transaction()
@login_required
def jurados(id_=None):
    user = Session.get_user(session['session_key'])
    inscription, = Inscription.search([('id', '=', int(id_))],
                                      limit=1)
    inscriptions = Inscription.search([('id', '>', 0)])
    calification, = Calification.search([
        ('program', '=', int(id_)),
        ('jury.web_user', '=', user)
        ])
    rango = [str(x) for x in range(1,11)]

    if request.method == 'POST':
        print('\n' + '*'*20, request.form)
        print([x for x in request.form])
        print('*'*20 + '\n')
        campos_calificados = [x for x in request.form]
        # Conceptos generales
        calification.general_observations = 'observacion-general' in campos_calificados \
            and request.form['observacion-general'] or None
        calification.originality = 'originalidad' in campos_calificados \
            and request.form['originalidad'] or None
        calification.studio_work = 'trabajo-en-estudio' in campos_calificados \
            and request.form['trabajo-en-estudio'] or None
        calification.synthesis = 'sintesis' in campos_calificados \
            and request.form['sintesis'] or None
        calification.routine = 'planificacion' in campos_calificados \
            and request.form['planificacion'] or None
        calification.outdoor_work = 'trabajo-en-exteriores' in campos_calificados \
            and request.form['trabajo-en-exteriores'] or None
        calification.scenography = 'escenografia' in campos_calificados \
            and request.form['escenografia'] or None
        calification.schedule = 'cronograma' in campos_calificados \
            and request.form['cronograma'] or None
        calification.management_of_times = 'tiempos-de-aire' in campos_calificados \
            and request.form['tiempos-de-aire']
        # 'Conceptos de realizacion'
        calification.realization_observations = 'observacion-de-realizacion' in campos_calificados \
            and request.form['observacion-de-realizacion'] or None
        calification.frames = 'encuadres' in campos_calificados \
            and request.form['encuadres'] or None
        calification.axis_of_action = 'eje-de-accion' in campos_calificados\
            and request.form['eje-de-accion'] or None
        calification.general_post_production = 'post-produccion' in campos_calificados \
            and request.form['post-produccion'] or None
        calification.blueprints = 'planos-realizacion' in campos_calificados \
            and request.form['planos-realizacion'] or None
        calification.illumination = 'toma-de-iluminacion' in campos_calificados \
            and request.form['toma-de-iluminacion'] or None
        calification.camera_sets = 'puestas-de-camaras' in campos_calificados \
            and request.form['puestas-de-camaras'] or None
        calification.sound = 'toma-de-sonido' in campos_calificados \
            and request.form['toma-de-sonido'] or None
        # Encuadres
        calification.frames_observations = 'observacion-de-encuadres' in campos_calificados \
            and request.form['observacion-de-encuadres'] or None
        calification.images = 'imagenes' in campos_calificados \
            and request.form['imagenes'] or None
        calification.creativity = 'creatividad' in campos_calificados \
            and request.form['creatividad'] or None
        calification.inserts = 'inserts' in campos_calificados \
            and request.form['inserts'] or None or None
        # Otros conceptos
        calification.other_concepts_observations = 'observacion-de-otros-conceptos' in campos_calificados \
            and request.form['observacion-de-otros-conceptos'] or None
        calification.camera_movements = 'movimiento-de-camara' in campos_calificados \
            and request.form['movimiento-de-camara'] or None
        calification.cameraman_illumination = 'iluminacion' in campos_calificados \
            and request.form['iluminacion'] or None
        calification.angulation = 'angulacion' in campos_calificados \
            and request.form['angulacion'] or None
        calification.cameraman_sound = 'sonido' in campos_calificados \
            and request.form['sonido'] or None
        calification.cameraman_blueprints = 'planos-camarografo' in campos_calificados \
            and request.form['planos-camarografo'] or None
        calification.iris_management = 'manejo-del-iris' in campos_calificados \
            and request.form['manejo-del-iris'] or None
        # Conceptos mejor editor/a
        calification.editor_observations = 'observacion-de-mejor-editor' in campos_calificados \
            and request.form['observacion-de-mejor-editor'] or None
        calification.musicalization = 'musicalizacion' in campos_calificados \
            and request.form['musicalizacion'] or None
        calification.relevance_of_the_inserts = 'pertinencia-inserts' in campos_calificados \
            and request.form['pertinencia-inserts'] or None
        calification.picture_airtime = 'tiempo-al-aire' in campos_calificados \
            and request.form['tiempo-al-aire'] or None
        calification.skirting_boards = 'zocalos' in campos_calificados \
            and request.form['zocalos'] or None
        calification.rhythm = 'ritmo' in campos_calificados \
            and request.form['ritmo'] or None
        calification.editor_sound = 'sonido-editor' in campos_calificados \
            and request.form['sonido-editor'] or None
        # Conceptos mejor productor
        calification.producer_observations = 'observacion-mejor-productor' in campos_calificados \
            and request.form['observacion-mejor-productor'] or None
        calification.preproduction = 'preproduccion' in campos_calificados \
            and request.form['preproduccion'] or None
        calification.producer_creativity = 'creatividad-productor' in campos_calificados \
            and request.form['creatividad-productor'] or None
        calification.originality_of_the_proposal = 'originalidad-productor' in campos_calificados \
            and request.form['originalidad-productor'] or None
        calification.communication_strategies = 'estrategia-comunicacion' in campos_calificados \
            and request.form['estrategia-comunicacion'] or None
        calification.production = 'produccion' in campos_calificados \
            and request.form['produccion'] or None
        calification.elaboration_of_the_routine = 'elaboracion-rutina' in campos_calificados \
            and request.form['elaboracion-rutina'] or None
        calification.content_originality = 'originalidad-contenido' in campos_calificados \
            and request.form['originalidad-contenido'] or None
        calification.post_production = 'post-mejor-produccion' in campos_calificados \
            and request.form['post-mejor-produccion'] or None
        calification.variety_of_proposals = 'variedad-propuestas' in campos_calificados \
            and request.form['variedad-propuestas'] or None
        calification.adequacy = 'adecuacion-contenido' in campos_calificados \
            and request.form['adecuacion-contenido'] or None
        calification.save()
    return render_template('/paginajurados.html',
                           usuario=int(id_),
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
                           rutina=inscription.routine,
                           cover=inscription.video_short.replace('view','preview'),
                           programa1=inscription.video_long1.replace('view','preview'),
                           programa2=inscription.video_long2.replace('view','preview'),
                           programa3=inscription.video_long3.replace('view','preview'),
                           calification=calification,
                           rango=rango
                           )

@blueprint.route('/paginajurados')
@blueprint.route("/listado")
@blueprint.route("/listado/")
@blueprint.route("/listado/<categoria>")
@tryton.transaction()
@login_required
def show_category(categoria=None):
    inscriptos = []
    user = Session.get_user(session['session_key'])
    #print(5*'\n' + 20*'*',
          #user,
          #20*'*' + 5*'\n')
    if categoria == "a":
        inscriptos = Inscription.search([
            ('category.category.name','=', "CATEGORÍA A"),
            ('jurys.jury.web_user', '=', user)
            ])
    elif categoria == "b":
        inscriptos = Inscription.search([
            ('category.category.name','=', "CATEGORÍA B"),
            ('jurys.jury.web_user', '=', user)
            ])
    elif categoria == "c":
        inscriptos = Inscription.search([
            ('category.category.name','=', "CATEGORÍA C"),
            ('jurys.jury.web_user', '=', user)
            ])
    elif categoria == "d":
        inscriptos = Inscription.search([
            ('category.category.name','=', "CATEGORÍA D"),
            ('jurys.jury.web_user', '=', user)
            ])
    elif categoria == "e":
        inscriptos = Inscription.search([
            ('category.category.name','=', "CATEGORÍA E"),
            ('jurys.jury.web_user', '=', user)
            ])
    elif categoria == "f":
        inscriptos = Inscription.search([
            ('category.category.name','=', "CATEGORÍA F"),
            ('jurys.jury.web_user', '=', user)
            ])
    elif categoria == "vivo":
        inscriptos = Inscription.search([
            ('category.category.name','=', "TRANSMISIONES EN VIVO"),
            ('jurys.jury.web_user', '=', user)
            ])
    elif categoria == "turf":
        inscriptos = Inscription.search([
            ('category.category.name','=', "TURF"),
            ('jurys.jury.web_user', '=', user)
            ])
    else:
        inscriptos = Inscription.search([
            ('id','>',0),
            ('jurys.jury.web_user', '=', user)
            ])
        #return render_template("listado.html", inscriptos=inscriptos, usuarios=len(inscriptos))
    return render_template("listado.html", inscriptos=inscriptos, usuarios=len(inscriptos))

@blueprint.route("/verificar_socio",  methods=['GET', 'POST'])
@tryton.transaction()
def verificar_socio():
    cuit = request.args.get('cuit', 0, type=int)
    print(request.args)
    partners = Partner.search([
        ('cuit', '=', cuit)
        ])
    print("holaa asd")
    print(cuit)
    if partners:
        if partners[0].is_partner:
            print("jsonify(socio='si')")
            return jsonify(socio='si', razonSocial=partners[0].name, numero_socio = partners[0].number) 
        else:
            print("jsonify(socio='no')")
            return jsonify(socio='no', razonSocial=partners[0].name, numero_socio = partners[0].number)
    return jsonify(socio='', razonSocial="")

@blueprint.route("/verificar_localidad",  methods=['GET', 'POST'])
@tryton.transaction()
def verificar_localidad():
    cuit = request.args.get('cuit', 0, type=int)
    localidad = request.args.get('localidad', 0, type=int)
    print(request.args)
    print("antres de buscar tupla")
    print(cuit)
    print(localidad)

    partners = Partner.search([
        ('cuit', '=', cuit),
        ('city.id', '=', localidad)
        ])

    if partners:
        return jsonify(razonSocial=partners[0].name, numero_socio = partners[0].number)
    return jsonify(razonSocial="" , numero_socio = "")

@blueprint.route("/listado_reserva", methods=['GET', 'POST'])
@tryton.transaction()
@login_required
def listado_reserva():
    Invitation = tryton.pool.get('aet_web.invitation')
    user = Session.get_user(session['session_key'])
    invitations = Invitation.search([('web_user', '=', user)])
    return render_template("listado-reserva.html",
        invitations=invitations, user=user)

@blueprint.route("/programa_reserva/<invitation_id>/<user_id>", methods=['GET', 'POST'])
@tryton.transaction()
@login_required
def programa_reserva(invitation_id, user_id):
    Invitation = tryton.pool.get('aet_web.invitation')
    user = Session.get_user(session['session_key'])
    invitation = Invitation(invitation_id)
    if int(user_id) == user.id:
        return render_template("programa-reserva.html",
            invitation=invitation, user=user)
    else:
        return 'No coincide el usuario con la invitacion a reservar'


@blueprint.route("/calcular_precio_entradas", methods=['GET', 'POST'])
@tryton.transaction()
@login_required
def calcular_precio_entradas():
    Invitation = tryton.pool.get('aet_web.invitation')
    cantidad = request.args.get('cantidad', type=int)
    invitation_id = request.args.get('invitation_id', type=int)
    print(5*'\n'+'calculando precio'+5*'\n')
    invitation = Invitation(invitation_id)
    precio =3000 * data['cantidad']
    if invitation.inscription and invitation.inscription.category:
        precio = invitation.inscription.category.category.price * cantidad
    elif not cantidad:
        precio = 0
    return jsonify(precio=precio)
