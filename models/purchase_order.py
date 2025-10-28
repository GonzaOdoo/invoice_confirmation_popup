from odoo import models, api,fields
import logging

_logger=logging.getLogger(__name__)
class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    picking_type_id = fields.Many2one('stock.picking.type', 'Entregar', required=False, default=False, domain="['|', ('warehouse_id', '=', False), ('warehouse_id.company_id', '=', company_id)]",
        help="This will determine operation type of incoming shipment")
    is_only_service = fields.Boolean(string="Es servicio?",compute='_compute_is_only_service')

    def _compute_is_only_service(self):
        for record in self:
            record.is_only_service = any(line.product_id.type == 'product' for line in record.order_line if line.product_id)
            
    @api.model
    def default_get(self, fields_list):
        # Llamamos al original para obtener todos los defaults (partner, company, etc.)
        defaults = super().default_get(fields_list)

        # Forzamos que picking_type_id NO venga por defecto
        if 'picking_type_id' in defaults:
            _logger.info("🧹 Removiendo picking_type_id del default_get: %s", defaults['picking_type_id'])
            defaults['picking_type_id'] = False  # o defaults['picking_type_id'] = False
        _logger.info(defaults)
        return defaults
        

    @api.onchange('company_id')
    def _onchange_company_id(self):
        # No hacer nada → evita que se asigne un picking_type_id automáticamente
        pass