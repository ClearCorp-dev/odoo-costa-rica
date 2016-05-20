# -*- coding: utf-8 -*-
# © 2016 ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import time
from lxml import etree
import logging
import openerp.netsvc
from openerp.osv import fields, osv
import openerp.addons.decimal_precision as dp
from openerp.tools.translate import _
from datetime import timedelta
from datetime import datetime
from dateutil.relativedelta import relativedelta



class account_voucher(osv.osv):
    _inherit = 'account.voucher'

    def proforma_voucher(self, cr, uid, ids, context=None):
        obj_invoice = self.pool.get('account.invoice')
        for voucher in self.pool.get('account.voucher').browse(cr, uid, ids,context=context):

            for line in voucher.line_cr_ids:
                invoices = obj_invoice.search(cr, uid, [('number','=',line.name)])
                for inv in obj_invoice.browse(cr, uid, invoices):
                    voucher_date = datetime.strptime(voucher.date,'%Y-%m-%d')
                    last_date = datetime.strptime(inv.date_invoice,'%Y-%m-%d')

                    if last_date < voucher_date:
                        inv.write({'paid_ontime': True}, context=context)
                        #~ logging.getLogger("account_voucher").info("last_date = %s - voucher.date = %s",  last_date, voucher_date)

        self.action_move_line_create(cr, uid, ids, context=context)
        return True
