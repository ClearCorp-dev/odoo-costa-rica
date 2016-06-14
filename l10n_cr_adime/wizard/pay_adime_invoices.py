# -*- coding: utf-8 -*-
# © 2016 ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models
from openerp.exceptions import ValidationError


class PayAdimeInvoices(models.TransientModel):

    _name = 'l10n.cr.adime.pay.invoices.wizard'

    def invoice_pay(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        active_ids = context.get('active_ids', []) or []

        invoice_obj = self.pool.get('account.invoice')
        for inv in invoice_obj.browse(cr, uid, active_ids, context=context):
            if inv.state != 'paid':
                raise ValidationError(
                    _('Selected invoice(s) cannot be paid (ADIME) as they are '
                      'not in "Paid" state.'))
            if not inv.is_adime:
                raise ValidationError(
                    _('Selected invoice(s) cannot be paid (ADIME) as they are '
                      'not ADIME invoices.'))
            inv.write({'paid_adime': True})
        return {'type': 'ir.actions.act_window_close'}
