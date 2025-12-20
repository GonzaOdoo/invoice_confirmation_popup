# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools.misc import clean_context
import logging

_logger = logging.getLogger(__name__)
class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    @api.model
    def _prepare_purchase_order_line(self, product_id, product_qty, product_uom_id, company_id, supplier_info, po):
        """ Sobrescribimos para permitir inyectar una descripción personalizada desde approval. """
        vals = super()._prepare_purchase_order_line(
            product_id, product_qty, product_uom_id, company_id, supplier_info, po
        )
        # Intentamos obtener la descripción personalizada desde el contexto
        custom_description = self.env.context.get('custom_po_description')
        if custom_description:
            vals['name'] = custom_description

        return vals
#reason

class ApprovalRequest(models.Model):
    _inherit = 'approval.request'
    def action_create_purchase_orders(self):
        """ Create and/or modifier Purchase Orders. """
        self.ensure_one()
        self.product_line_ids._check_products_vendor()

        purchase_orders_to_update = self.env['purchase.order']

        for line in self.product_line_ids:
            seller = line._get_seller_id()
            vendor = seller.partner_id
            po_domain = line._get_purchase_orders_domain(vendor)
            purchase_orders = self.env['purchase.order'].search(po_domain)

            if purchase_orders:
                # Siempre usar la primera orden existente (no importa si ya tiene líneas)
                purchase_order = purchase_orders[0]
            else:
                # Crear nueva orden
                po_vals = line._get_purchase_order_values(vendor)
                purchase_order = self.env['purchase.order'].create(po_vals)
                _logger.info('Ordén creada')
                _logger.info(purchase_order)
            # ✅ Siempre crear una NUEVA línea, sin buscar existentes
            po_line_vals = self.env['purchase.order.line'].with_context(
                custom_po_description=line.description or line.name
            )._prepare_purchase_order_line(
                line.product_id,
                line.quantity,
                line.product_uom_id,
                line.company_id,
                seller,
                purchase_order,
            )
            new_po_line = self.env['purchase.order.line'].create(po_line_vals)
            line.purchase_order_line_id = new_po_line.id
    
            # Actualizar origin
            new_origin = {self.name}
            origins = set((purchase_order.origin or '').split(', ')) - {''}
            if not new_origin.issubset(origins):
                origins.update(new_origin)
                purchase_order.write({'origin': ', '.join(sorted(origins))})
               
