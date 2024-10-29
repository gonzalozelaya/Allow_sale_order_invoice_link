# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError
class AllowSaleOrderLink(models.Model):
    _inherit = 'account.move'
    
    @api.onchange('invoice_origin')
    def _onchange_invoice_origin(self):
        for move in self:
            if move.invoice_origin:
                sale_order = self.env['sale.order'].search([('name', '=', move.invoice_origin)], limit=1)
                if sale_order:
                    for line in move.invoice_line_ids:
                        sale_order_line = sale_order.order_line.filtered(
                            lambda l: l.product_id.id == line.product_id.id
                        )
                        if sale_order_line:
                            # Relacionar la línea de la factura con la línea de pedido correspondiente
                            sale_order_line.invoice_lines.write([(4, sale_order_line.id)])
                            #raise UserError(sale_order_line.invoice_lines)
                            #sale_order_line.qty_invoiced += line.quantity
                        else:
                            # Crear una línea de pedido si no existe
                            sale_order.order_line.create({
                                'order_id': sale_order.id,
                                'product_id': line.product_id.id,
                                'qty_invoiced': line.quantity,
                                'product_uom_qty': 0,
                                'price_unit': line.price_unit,
                                'name': line.name,
                            })

                    # Forzar el recálculo para que se actualicen `invoice_count` y `invoice_ids`
                    #sale_order._get_invoiced()

