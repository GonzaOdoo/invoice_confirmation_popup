from odoo import models, api,fields
import logging

_logger=logging.getLogger(__name__)
class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    picking_type_id = fields.Many2one('stock.picking.type', 'Entregar', required=True, default=False, domain="['|', ('warehouse_id', '=', False), ('warehouse_id.company_id', '=', company_id)]",
        help="This will determine operation type of incoming shipment")
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
