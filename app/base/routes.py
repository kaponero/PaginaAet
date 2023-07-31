from flask import render_template, redirect, request, url_for, flash, session

from app import tryton
from app.base import blueprint
from app.base.forms import LoginForm, Formulario

from functools import wraps


WebUser = tryton.pool.get('web.user')
Session = tryton.pool.get('web.user.session')
Inscription = tryton.pool.get('aet_web.inscription')

category_dict = {
    'CATEGORÍA A:1º De Mayo - Categoría A': '1',
    'CATEGORÍA A:Alcaraz - Categoría A': '2',
    'CATEGORÍA A:Aldea San Antonio - Categoría A': '3',
    'CATEGORÍA A:Aldea Valle Maria - Categoría A': '4',
    'CATEGORÍA A:Aranguren - Categoría A': '5',
    'CATEGORÍA A:Basavilbaso - Categoría A': '6',
    'CATEGORÍA A:Bovril - Categoría A': '7',
    'CATEGORÍA A:Caseros - Categoría A': '8',
    'CATEGORÍA A:Ceibas - Categoría A': '9',
    'CATEGORÍA A:Cerrito - Categoría A': '10',
    'CATEGORÍA A:Colonia Avellaneda - Categoría A': '11',
    'CATEGORÍA A:Colonia Ayui - Categoría A': '12',
    'CATEGORÍA A:Colonia Elia - Categoría A': '13',
    'CATEGORÍA A:Conscripto Bernardi - Categoría A': '14',
    'CATEGORÍA A:Enrique Carbo - Categoría A': '15',
    'CATEGORÍA A:Estancia Grande - Categoría A': '16',
    'CATEGORÍA A:General Campos - Categoría A': '17',
    'CATEGORÍA A:General Galarza - Categoría A': '18',
    'CATEGORÍA A:General Ramirez - Categoría A': '19',
    'CATEGORÍA A:Gilbert - Categoría A': '20',
    'CATEGORÍA A:Gobernador Mansilla - Categoría A': '21',
    'CATEGORÍA A:Hasenkamp - Categoría A': '22',
    'CATEGORÍA A:Hernandarias - Categoría A': '23',
    'CATEGORÍA A:Hernandez - Categoría A': '24',
    'CATEGORÍA A:Herrera - Categoría A': '25',
    'CATEGORÍA A:Ibicuy - Categoría A': '26',
    'CATEGORÍA A:La Criolla - Categoría A': '27',
    'CATEGORÍA A:Larroque - Categoría A': '28',
    'CATEGORÍA A:Los Charruas - Categoría A': '29',
    'CATEGORÍA A:Los Conquistadores - Categoría A': '30',
    'CATEGORÍA A:Lucas Gonzalez - Categoría A': '31',
    'CATEGORÍA A:Macia - Categoría A': '32',
    'CATEGORÍA A:Maria Grande - Categoría A': '33',
    'CATEGORÍA A:Oro Verde - Categoría A': '34',
    'CATEGORÍA A:Piedras Blancas - Categoría A': '35',
    'CATEGORÍA A:Pronunciamiento - Categoría A': '36',
    'CATEGORÍA A:Pueblo General Belgrano - Categoría A': '37',
    'CATEGORÍA A:Puerto Yerua - Categoría A': '38',
    'CATEGORÍA A:San Benito - Categoría A': '39',
    'CATEGORÍA A:San Gustavo - Categoría A': '40',
    'CATEGORÍA A:San Jaime De La Frontera - Categoría A': '41',
    'CATEGORÍA A:San Justo - Categoría A': '42',
    'CATEGORÍA A:Santa Ana - Categoría A': '43',
    'CATEGORÍA A:Santa Anita - Categoría A': '44',
    'CATEGORÍA A:Sauce De Luna - Categoría A': '45',
    'CATEGORÍA A:Segui - Categoría A': '46',
    'CATEGORÍA A:Tabossi - Categoría A': '47',
    'CATEGORÍA A:Ubajay - Categoría A': '48',
    'CATEGORÍA A:Urdinarrain - Categoría A': '49',
    'CATEGORÍA A:Viale - Categoría A': '50',
    'CATEGORÍA A:Villa Clara - Categoría A': '51',
    'CATEGORÍA A:Villa Del Rosario - Categoría A': '52',
    'CATEGORÍA A:Villa Dominguez - Categoría A': '53',
    'CATEGORÍA A:Villa Libertador San Martin - Categoría A': '54',
    'CATEGORÍA A:Villa Mantero - Categoría A': '55',
    'CATEGORÍA A:Villa Paranacito - Categoría A': '56',
    'CATEGORÍA A:Villa Urquiza - Categoría A': '57',
    'CATEGORÍA A:Villa Elisa - Categoría A': '58',
    'CATEGORÍA A:San Jose De Feliciano - Categoría A': '59',
    'CATEGORÍA A:San Salvador - Categoría A': '60',
    'CATEGORÍA A:Rosario Del Tala - Categoría A': '61',
    'CATEGORÍA A:Federacion - Categoría A': '62',
    'CATEGORÍA A:Santa Elena - Categoría A': '63',
    'CATEGORÍA A:Federal - Categoría A': '64',
    'CATEGORÍA A:San Jose - Categoría A': '65',
    'CATEGORÍA A:Diamante - Categoría A': '66',
    'CATEGORÍA A:Crespo - Categoría A': '67',
    'CATEGORÍA A:Nogoya - Categoría A': '68',
    'CATEGORÍA A:Colon - Categoría A': '69',
    'CATEGORÍA A:La Paz - Categoría A': '70',
    'CATEGORÍA A:Victoria - Categoría A': '71',
    'CATEGORÍA A:Villaguay - Categoría A': '72',
    'CATEGORÍA A:Chajari - Categoría A': '73',
    'CATEGORÍA A:Gualeguay - Categoría A': '74',
    'CATEGORÍA A:Concepcion Del Uruguay - Categoría A': '75',
    'CATEGORÍA A:Gualeguaychu - Categoría A': '76',
    'CATEGORÍA A:Concordia - Categoría A': '77',
    'CATEGORÍA A:Parana - Categoría A': '78',
    'CATEGORÍA E:Canales abiertos - Categoría E': '79',
    'CATEGORÍA F:Productoras independientes - Categoría F': '80',
    'TRANSMISIONES EN VIVO': '81',
    'TURF': '82'
    }

genre_dict = {
    '': None,
    'NOTICIERO': '1',
    'PERIODISTICO DE OPINION Y/O POLITICO': '2',
    'DEPORTIVO': '3',
    'AGRARIO O RURAL': '4',
    'EVENTOS FOLCLORICOS O TRADICIONALISTAS': '5',
    'MUSICAL': '6',
    'EDUCATIVO': '7',
    'INTERES GENERAL': '8',
    'DOCUMENTAL': '9',
    'ESPECIAL': '10',
    'INFANTIL': '11',
    'TURF': '12',
    'TRANSMISION EN VIVO': '13'
    }


live_dict = {
    'SI': 'si',
    'NO': 'no'
    }

aet_partner_dict = {
    'SI': 'si',
    'NO': 'no'
    }

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
@tryton.transaction(readonly=False, user=1)
def inscripcion():
    if request.method == 'POST':
        nom = request.form['programa']
        #cat = request.form['categoria']
        fecha = request.form['fecha']
        dura  = request.form['duracion']
        vid = request.form['video']
        print(request)
        inscription, = Inscription.create([{
            'name': request.form['programa'],
            'genre': '1',
            'category': category_dict[request.form['categoria']],
            'genre': genre_dict[request.form['genero']],
            'live': live_dict[request.form['vivo']],
            'aet_partner': aet_partner_dict[request.form['socio']],
            }])
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


