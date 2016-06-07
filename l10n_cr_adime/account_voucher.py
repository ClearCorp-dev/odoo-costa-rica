# -*- coding: utf-8 -*-
# © 2016 ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.osv import osv
from datetime import datetime


class AccountVoucher(osv.osv):

    _inherit = 'account.voucher'

    def proforma_voucher(self, cr, uid, ids, context=None):
        obj_invoice = self.pool.get('account.invoice')
        for voucher in self.pool.get('account.voucher').browse(
                cr, uid, ids, context=context):

            for line in voucher.line_cr_ids:
                invoices = obj_invoice.search(
                    cr, uid, [('number', '=', line.name)])
                for inv in obj_invoice.browse(cr, uid, invoices):
                    voucher_date = datetime.strptime(voucher.date, '%Y-%m-%d')
                    last_date = datetime.strptime(inv.date_invoice, '%Y-%m-%d')

                    if last_date < voucher_date:
                        inv.write({'paid_ontime': True}, context=context)

        self.action_move_line_create(cr, uid, ids, context=context)
        return True
