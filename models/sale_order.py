from odoo import models, fields, api
from odoo.exceptions import UserError

class AllowSaleOrderLink(models.Model):
    _inherit = 'sale.order'

    order_type = fields.Selection(
    selection=[('normal', 'Normal'), ('anticipada', 'Anticipada')],
    string='Tipo de orden',
    default=False
)