from trytond.pool import Pool

from . import aet_web

def register():
    Pool.register(
        aet_web.AetWeb,
        aet_web.Category,
        module='aet_web', type_='model')
