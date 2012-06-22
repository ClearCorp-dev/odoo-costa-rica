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

import pooler

from collections import defaultdict
from report import report_sxw
from osv import osv
from tools.translate import _
from datetime import datetime

from openerp.addons.account_financial_report_webkit.report.partners_ledger import PartnersLedgerWebkit
from openerp.addons.account_financial_report_webkit.report.webkit_parser_header_fix import HeaderFooterTextWebKitParser

class l10n_cr_PartnersLedgerWebkit(PartnersLedgerWebkit):

    def __init__(self, cursor, uid, name, context):
        super(l10n_cr_PartnersLedgerWebkit, self).__init__(cursor, uid, name, context=context)
        self.pool = pooler.get_pool(self.cr.dbname)
        self.cursor = self.cr

        self.localcontext.update({
            'get_amount': self.get_amount,
            'get_partner_name': self.get_partner_name,
            'get_accounts_by_curr': self.get_accounts_by_curr,
            'get_currency_symbol': self.get_currency_symbol,
        })

    def get_accounts_by_curr(self, cr, uid, objects):
        currency_names_list = []
        accounts_curr_list = []
        accounts_by_curr = []

        for account in objects:
            currency_name = account.currency_id.name
            if currency_name not in currency_names_list:
                currency_names_list.append(currency_name)

        for currency_name in currency_names_list:
            account_by_curr = []
            for account in objects:
                if account.currency_id.name == currency_name:
                    account_by_curr.append(account)
            accounts_curr_list.append(account_by_curr)

        i = 0
        for currency_name in currency_names_list:
            temp_tup = (currency_name, accounts_curr_list[i])
            accounts_by_curr.append(temp_tup)
            i += 1
            
        return accounts_by_curr

    def get_amount(self,cr, uid, account_move_line, currency):
        account_obj = self.pool.get('account.account').browse(cr,uid,account_move_line['account_id'])
        
        obj_invoice = self.pool.get('account.invoice')
        invoice_search = obj_invoice.search(cr,uid,[('move_id','=',account_move_line['move_id'])])
        invoice = None
        if invoice_search != []:
            invoice = obj_invoice.browse(cr,uid,invoice_search[0])
        
        obj_voucher = self.pool.get('account.voucher')
        voucher_search = obj_voucher.search(cr,uid,[('move_id','=',account_move_line['move_id'])])
        
        voucher = None
        if voucher_search != []:
            voucher = obj_voucher.browse(cr,uid,voucher_search[0])
            
        res = ('none', 0.0, 0.0)

        amount = 0.0
        if currency != None:
            amount = account_move_line['amount_currency']
        else:
            if account_move_line['debit'] != 0.0 :
                amount = account_move_line['debit']
            elif account_move_line['credit'] != 0.0 :
                amount = account_move_line['credit'] * -1

        # Invoices
        if invoice:
            if invoice.type == 'out_invoice': # Customer Invoice 
                res = ('invoice', amount)
            elif invoice.type == 'in_invoice': # Supplier Invoice
                res = ('invoice', amount)
            elif invoice.type == 'in_refund': # Debit Note
                res = ('debit', amount)
            elif invoice.type == 'out_refund': # Credit Note
                res = ('credit', amount)
        # Vouchers
        elif voucher:
            if voucher.type == 'payment': # Payment
                res = ('payment', amount)
            elif voucher.type == 'sale': # Invoice
                res = ('invoice', amount)
            elif voucher.type == 'receipt': # Payment
                res = ('payment', amount)
        # Manual Move
        else:
            res = ('manual', amount)
        
        if res[1] == None or (currency != None and res[1] == 0.0):
            secundary_amount = (account_move_line['debit'] != 0.0) and account_move_line['debit'] or account_move_line['credit']
            res = (res[0], 0.0, secundary_amount)
        else:
            res = (res[0], res[1], None)

        return res
        
    def get_partner_name(self,cr,uid,partner_name, p_id, p_ref, p_name):
        
        res = ''
        if p_ref != None and p_name != None:
            res = res+p_ref+' '+p_name
        else:
            res =  partner_name
        
            
        return res

    def get_currency_symbol(self, cr, uid, currency_id):
        currency = self.pool.get('res.currency').browse(cr,uid,currency_id)

        return currency.symbol

HeaderFooterTextWebKitParser('report.account_financial_report_webkit.account.account_report_partners_ledger_webkit',
                             'account.account',
                             'addons/l10n_cr_account_financial_report_webkit/report/l10n_cr_account_report_partners_ledger.mako',
                             parser=l10n_cr_PartnersLedgerWebkit)
