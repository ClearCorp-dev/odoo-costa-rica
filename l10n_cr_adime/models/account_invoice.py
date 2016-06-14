# -*- coding: utf-8 -*-
# © 2016 ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api
import openerp.addons.decimal_precision as dp
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT
from datetime import datetime


class AccountInvoice(models.Model):

    _inherit = 'account.invoice'

    @api.multi
    def onchange_partner_id(
            self, type, partner_id, date_invoice=False, payment_term=False,
            partner_bank_id=False, company_id=False):
        res = super(AccountInvoice, self).onchange_partner_id(
            type, partner_id, date_invoice=date_invoice,
            payment_term=payment_term, partner_bank_id=partner_bank_id,
            company_id=company_id)

        if partner_id and self.env['res.partner'].browse(partner_id).is_adime:
            res['value']['is_adime'] = True
        return res

    @api.depends('amount_untaxed', 'is_adime')
    def _compute_adime_total(self):
        for inv in self:
            if inv.is_adime:
                inv.adime_total = inv.amount_untaxed * (
                    inv.partner_id.adime_id.percentage / 100)
            else:
                inv.adime_total = 0.0

    @api.multi
    def confirm_paid(self):
        for inv in self:
            if inv.is_adime:
                line_ids = self.move_line_id_payment_get()
                query = """SELECT aml2.id
                FROM account_move_line AS aml2,
                  account_move_reconcile AS amr,
                  account_move_line AS aml
                WHERE amr.id = aml.reconcile_id
                  AND aml.id IN %s
                  AND aml2.id NOT IN %s
                  AND aml2.reconcile_id = amr.id
                ORDER BY aml2.date DESC
                LIMIT 1"""
                self._cr.execute(query, (tuple(line_ids), tuple(line_ids),))
                move_id = self._cr.fetchone()
                move = self.env['account.move.line'].browse(move_id)
                invoice_date = datetime.strptime(
                    inv.date_due, DEFAULT_SERVER_DATE_FORMAT).date()
                move_date = datetime.strptime(
                    move.date, DEFAULT_SERVER_DATE_FORMAT).date()
                if move_date <= invoice_date:
                    inv.paid_ontime = True
                    inv.payment_date = move.date
                else:
                    inv.paid_ontime = False
                    inv.payment_date = move.date
        return super(AccountInvoice, self).confirm_paid()

    is_adime = fields.Boolean(
        'Admine Invoice', states={'draft': [('readonly', False)]},
        default=False)
    paid_ontime = fields.Boolean(
        'Paid on time', readonly=True, copy=False, default=False)
    payment_date = fields.Date('Payment Date', readonly=True)
    paid_adime = fields.Boolean(
        'Paid to partner (Adime)', readonly=True, copy=False, default=False)
    adime_total = fields.Float(
        'Adime Amount', compute='_compute_adime_total',
        digits=dp.get_precision('Account'), store=True)
