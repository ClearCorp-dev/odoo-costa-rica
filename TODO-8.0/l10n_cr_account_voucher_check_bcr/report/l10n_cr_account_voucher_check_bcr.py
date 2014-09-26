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
from  openerp.addons.account_report_lib.tools.tools_amount_to_text import number_to_text_es
import locale

class check_voucher(report_sxw.rml_parse):

    def __init__(self, cr, uid, name, context):
        super(check_voucher, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
            'cr'  : cr,
            'uid' : uid,
            'get_text':self.get_text,
            'count_text':self.count_text,
            'get_concept':self.get_concept,
        })
        self.context = context
        self._node = None


    def get_text(self,amount,currency,lang,company_id):
        separator = ','
        decimal_point = '.'
        name_currency = currency.currency_name
        if name_currency == False:
            name_currency = company_id.currency_id.currency_name
        if name_currency == None:
            name_currency = company_id.currency_id.currency_name
        if lang:
            lang_pool = self.pool.get('res.lang')
            id_lang = lang_pool.search(self.cr,self.uid,[('code','=',lang)])
            obj_lang = lang_pool.browse(self.cr,self.uid,id_lang)[0]
            separator = obj_lang  and obj_lang.thousands_sep or separator
            decimal_point = obj_lang  and obj_lang.decimal_point or decimal_point
        #debug(separator)
        #debug(decimal_point)
        res = number_to_text_es(amount,name_currency,separator=separator,decimal_point=decimal_point)
        return res
        
        
        
    def count_text(self,amount,currency,lang,company_id):
        res = len(self.get_text(amount,currency,lang,company_id))
        return res
        
        
    def get_concept(self,moves):
        res = 'error'
        for move in moves:
            move_line = self.pool.get('acccount.move.line').browse(self.cr,self.uid,move.id)
            invoice = self.pool.get('account.invoice').browse(self.cr,self.uid,move_line.invoice)
            if invoice.name != ''or invoice.name != False:
                res = invoice.name
        return res
        
report_sxw.report_sxw(
    'report.webkit_report_l10n_cr_account_voucher_check_bcr',
    'account.voucher',
    'addons/l10n_cr_account_voucher_check_bcr/report/l10n_cr_account_voucher_check_bcr.mako',
    parser=check_voucher
)
