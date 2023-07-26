from trytond.model import ModelView, ModelSQL, Workflow, fields
from trytond.pyson import Or, Eval, And, Not, Bool
from trytond.pool import Pool, PoolMeta
from trytond.transaction import Transaction
from trytond.wizard import Button
from trytond.exceptions import UserError

from decimal import Decimal
from datetime import date
from io import BytesIO
import treepoem


class AetWeb(Workflow, ModelSQL, ModelView):
    'Aet web'
    __name__= 'aet_web.aet_web'

    name = fields.Char('Program name')
    category = fields.Many2One('aet_web.category', 'Locality/Category/Air Channel')
    gender = fields.Selection([
        ('1', 'NOTICIERO'),
        ('2', 'PERIODISTICO DE OPINION Y/O POLITICO'),
        ('3', 'DEPORTIVO'),
        ('4', 'AGRARIO O RURAL'),
        ('5', 'EVENTOS FOLCLORICOS O TRADICIONALISTAS'),
        ('6', 'MUSICAL'),
        ('7', 'EDUCATIVO'),
        ('8', 'INTERES GENERAL'),
        ('9', 'DOCUMENTAL'),
        ('10', 'ESPECIAL'),
        ('11', 'INFANTIL'),
        ('12', 'TURF'),
        ('13', 'TRANSMISION EN VIVO')
        ], 'Gender')
    live = fields.Selection([
        ('si', 'SI'),
        ('no', 'NO'),
        ], 'Live, direct and simultaneous')
    gender_string = gender.translated('gender')
    locality_of_emission = fields.Char('Locality of emission')
    date_of_emission = fields.Date('Date of emission')
    duration= fields.Char('Duration')
    description = fields.Text('Description')
    video_long = fields.Char('Complete program')
    video_short = fields.chroniclersChar('program_segment')
    producer = fields.Char('Producer')
    co_producer = fields.Char('Co-producer')
    author = fields.Char('Author/screenwriter')
    editor = fields.Char('Editor')
    director = fields.Char('Director')
    cameraman = fields.Char('Cameraman')
    musician = fields.Char('Sound engineer/musician')
    host = fields.Char('Host/presenter/announcer')
    protagonist = fields.Char('Protagonist')
    chroniclers = fields.Char('Chroniclers')
    channel_name = fields.Char('Channel name')
    address_channel = fields.Char('Address of the channel')
    channel_town = fields.Char('Channel town')
    channel_contact = fields.Char('Channel contact')
    channel_phone = fields.Char('Channel phone')
    channel_email = fields.Char('Channel email')
    aet_partner = fields.Selection([
        ('si', 'SI'),
        ('no', 'NO'),
        ], 'AET partner?')
    business_name = fields.Char('Business name')
    cuit = fields.Numeric('CUIT')
    enrolled = fields.Boolean('Enrolled',readonly=True)

    @staticmethod
    def sign_up():
        return False

    @classmethod
    @ModelView.button
    def sign_up(cls, work_orders):
        cls.sign_up(aet_web, {'enrolled':True
                                })
    # Botones
    @classmethod
    def __setup__(cls):
        super(AetWeb, cls).__setup__()

        cls._buttons.update({
                'sign_up': {
                  'invisible': Eval('enrolled')
                    },
                })

class Category(ModelSQL, ModelView):
    "Category"
    __name__ = 'aet_web.category'

    name = fields.Char('Name')
