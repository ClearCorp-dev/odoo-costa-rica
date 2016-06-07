# -*- coding: utf-8 -*-
# © 2016 ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api


class AccountInvoice(models.Model):

    _inherit = 'account.invoice'

    is_adime = fields.Boolean(string='Factura Adime')
    paid_ontime = fields.Boolean(string='Pagado a tiempo')
    paid_adime = fields.Boolean(string='Pagado al Socio (Adime)')
    adime_total = fields.Float(string='Aporte Adime', default=0, required=True)

    @api.multi
    def write(self, vals):
        rate = 0
        for inv in self:
            rate = inv.company_id.currency_id.rate / inv.currency_id.rate
            if inv.partner_id.is_adime:
                vals['is_adime'] = True
                vals['adime_total'] =\
                    inv.amount_untaxed * rate *\
                    (inv.partner_id.adime_id.percentaje / 100)
        res = super(AccountInvoice, self).write(vals)
        return res

    @api.model
    def create(self, vals):
        res = super(AccountInvoice, self).create(vals)
        return res
