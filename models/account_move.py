# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError
class AllowSaleOrderLink(models.Model):
    _inherit = 'account.move'
    
    @api.onchange('invoice_origin')
    def _onchange_invoice_origin(self):
        for move in self:
            if move.move_type != 'out_invoice':
                return
            if move.invoice_origin:
                if move.sale_order_count >= 1:
                    raise UserError('Esta factura ya tiene una orden asociada')
                sale_order = self.env['sale.order'].search([('name', '=', move.invoice_origin)], limit=1)
                if sale_order:
                    if move.partner_id.id != sale_order.partner_id.id:
                        raise UserError('El Cliente debe ser el mismo que en la orden de venta')
                    for line in move.invoice_line_ids:
                        sale_order_line = sale_order.order_line.filtered(
                            lambda l: l.product_id.id == line.product_id.id
                        )
                        if sale_order_line:
                            # Relacionar la línea de la factura con la línea de pedido correspondiente
                            sale_order_line.write({
                                'invoice_lines': [(4, line._origin.id)]  # Agrega la línea de factura al campo Many2many `invoice_lines`
                            })
                            #raise UserError(sale_order_line.invoice_lines)
                            #sale_order_line.qty_invoiced += line.quantity
                        else:
                            # Crear una línea de pedido si no existe
                            new_sale_order_line = sale_order.order_line.create({
                                'order_id': sale_order.id,
                                'product_id': line.product_id.id,
                                'qty_invoiced': line.quantity,
                                'product_uom_qty': 0,
                                'price_unit': line.price_unit,
                                'name': line.name,
                            })
                            # Agregar la relación con `invoice_lines` después de crear la línea
                            new_sale_order_line.write({
                                'invoice_lines': [(4, line._origin.id)]
                            })

                    # Forzar el recálculo para que se actualicen `invoice_count` y `invoice_ids`
                    #sale_order._get_invoiced()

