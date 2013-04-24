# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Addons modules by CLEARCORP S.A.
#    Copyright (C) 2009-TODAY CLEARCORP S.A. (<http://clearcorp.co.cr>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import time
import pooler
from report import report_sxw
import locale
from datetime import date

class l10n_cr_partner_balance(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(l10n_cr_partner_balance, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
            'cr' : cr,
            'uid': uid,
            'get_partners_by_curr':self.get_partners_by_curr,
            'currency_convert':self.currency_convert,
            'get_time_today':self.get_time_today,
            'get_conversion_rate':self.get_conversion_rate,
            'get_currency':self.get_currency,
        })
    

    def get_partners_by_curr(self, cr, uid, partner):
        currency_names_list = []
        partners_curr_list = []
        partners_by_curr = []

        obj_move = self.pool.get('account.move.line')
        obj_search = obj_move.search(cr, uid, [('partner_id','=',partner.id),'&',('reconcile_id','=',False),'|',('account_id.type','=','payable'),('account_id.type','=','receivable')])
        move_lines = obj_move.browse(cr, uid, obj_search)

        for move_line in move_lines:
            currency_name = move_line.currency_id.name
            if currency_name not in currency_names_list:
                currency_names_list.append(currency_name)

        for currency_name in currency_names_list:
            move_lines_by_curr = []
            for move_line in move_lines:
                if move_line.currency_id.name == currency_name:
                    move_lines_by_curr.append(move_line)
            partners_curr_list.append(move_lines_by_curr)

        i = 0
        for currency_name in currency_names_list:
            temp_tup = (currency_name, partners_curr_list[i])
            partners_by_curr.append(temp_tup)
            i += 1
            
        return partners_by_curr
    

    def currency_convert(self, cr, uid, from_currency, to_currency, amount):
        res = self.pool.get('res.currency').compute(cr, uid, from_currency, to_currency, amount)

        return res

    def get_time_today(self):
        today = str(date.today())

        return today

    def get_conversion_rate(self, cr, uid, from_currency, to_currency):
        res = self.pool.get('res.currency')._get_conversion_rate(cr, uid, from_currency, to_currency)

        return res

    def get_currency(self, cr, uid, currency_id):
        currency = self.pool.get('res.currency').browse(cr, uid, currency_id)

        return currency
        
report_sxw.report_sxw(
    'report.l10n.cr.partner.balance.layout_ccorp',
    'res.partner',
    'addons/l10n_cr_account_financial_report_webkit/report/l10n_cr_account_report_partner_balance.mako',
    parser=l10n_cr_partner_balance)
