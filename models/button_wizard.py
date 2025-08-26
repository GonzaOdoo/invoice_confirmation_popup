from odoo import models, fields, api, _
from odoo.exceptions import UserError


class AccountMoveConfirmWizard(models.TransientModel):
    _name = 'account.move.confirm.wizard'
    _description = 'Confirmación antes de validar asiento contable'

    move_id = fields.Many2one('account.move', string='Asiento contable', required=True, ondelete='cascade')
    confirmation_message = fields.Text(string='Mensaje de confirmación', readonly=True)
    company_id = fields.Many2one('res.company')

    def action_confirm(self):
        """Confirma la validación del asiento contable"""
        self.ensure_one()
        if self.move_id.state != 'draft':
            raise UserError(_("El asiento ya está confirmado o cancelado."))
        self.move_id.action_post()  # Este es el método que confirma el asiento
        return {'type': 'ir.actions.act_window_close'}

    def action_cancel(self):
        """Cancela la acción y cierra el wizard"""
        return {'type': 'ir.actions.act_window_close'}



class AccountMove(models.Model):
    _inherit = 'account.move'

    def action_open_confirm_wizard_supplier(self):
        """
        Sobrescribimos action_post para mostrar el wizard antes de confirmar.
        """

        # Abrir el wizard de confirmación
        return {
            'name': 'Confirmar Validación',
            'type': 'ir.actions.act_window',
            'res_model': 'account.move.confirm.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_move_id': self.id,
                'default_company_id': self.company_id.id,
                'default_confirmation_message': (
                    f"Esta cargando una factura para la empresa {self.company_id.name}, si es correcto oprima De acuerdo, si desea corregirlo oprima Cancelar.\n\n"
                    "Por favor, verifique que todos los datos sean correctos. \n"
                    f"Empresa: {self.company_id.name}"
                ),
            },
        }