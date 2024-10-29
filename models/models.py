# -*- coding: utf-8 -*-

from odoo import models, fields, api

class AllowSaleOrderLink(models.Model):
    _inherit = 'account.move'
    
    @api.onchange('invoice_origin')
    def _onchange_invoice_origin(self):
        if self.invoice_origin:
            # Buscar la orden de venta basada en invoice_origin
            sale_order = self.env['sale.order'].search([('name', '=', self.invoice_origin)], limit=1)
            if not sale_order:
                raise UserError("No se encontró la orden de venta con el nombre especificado en invoice_origin.")
            
            # 1. Actualizar el conteo de facturas (invoice_count)
            sale_order.invoice_count = len(sale_order.invoice_ids) + 1

            # 2. Añadir la factura actual a las invoice_ids de la orden de venta
            sale_order.write({'invoice_ids': [(4, self.id)]})

            # 3. Actualizar la cantidad facturada (qty_invoiced) en las líneas de la orden de venta
            for line in self.invoice_line_ids:
                # Encontrar la línea de pedido correspondiente en la orden de venta
                sale_order_line = sale_order.order_line.filtered(lambda l: l.product_id == line.product_id)

                if sale_order_line:
                    # Si existe, actualizar qty_invoiced sumando la cantidad de la línea de factura
                    sale_order_line.qty_invoiced += line.quantity
                else:
                    # Si no existe una línea de pedido en la orden, crear una nueva con qty_invoiced
                    sale_order.order_line.create({
                        'order_id': sale_order.id,
                        'product_id': line.product_id.id,
                        'qty_invoiced': line.quantity,
                        'product_uom_qty': 0,  # Cantidad solicitada puede quedar en 0 si solo es facturada
                        'price_unit': line.price_unit,
                        'name': line.name,
                    })