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
from report import report_sxw
from tools.translate import _
import pooler
from datetime import datetime

from openerp.addons.account_financial_report_webkit.report.trial_balance import TrialBalanceWebkit
from openerp.addons.account_financial_report_webkit.report.webkit_parser_header_fix import HeaderFooterTextWebKitParser


class conciliation_bank(report_sxw.rml_parse):
    
    def __init__(self, cr, uid, name, context):
        super(conciliation_bank, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
            'cr' : cr,
            'uid': uid,
            'get_amount': self.get_amount,
            'get_move_lines': self.get_move_lines,
            'get_bank_accounts': self.get_bank_accounts,
            'get_bank_balance': self.get_bank_balance,
        })
    
    def get_amount(self,cr, uid, account_move_line, currency):
        account_obj = self.pool.get('account.account').browse(cr,uid,account_move_line.account_id.id)
        
        obj_invoice = self.pool.get('account.invoice')
        invoice_search = obj_invoice.search(cr,uid,[('move_id','=',account_move_line.move_id.id)])
        invoice = None
        if invoice_search != []:
            invoice = obj_invoice.browse(cr,uid,invoice_search[0])
        
        obj_voucher = self.pool.get('account.voucher')
        voucher_search = obj_voucher.search(cr,uid,[('move_id','=',account_move_line.move_id.id)])
        
        voucher = None
        if voucher_search != []:
            voucher = obj_voucher.browse(cr,uid,voucher_search[0])
            
        res = ('none', 0.0, 0.0)

        amount = 0.0
        if currency != False:
            amount = account_move_line.amount_currency
        else:
            if account_move_line.debit != 0.0 :
                amount = account_move_line.debit
            elif account_move_line.credit != 0.0 :
                amount = account_move_line.credit * -1

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
        # Debit o Credit
        else:
            if amount > 0.0:
                res = ('debit', amount)
            else:
                res = ('credit', amount)
                
        
        if res[1] == None or (currency != None and res[1] == 0.0):
            secundary_amount = (account_move_line.debit != 0.0) and account_move_line.debit or account_move_line.credit
            res = (res[0], 0.0, secundary_amount)
        else:
            res = (res[0], res[1], None)

        return res
    
    def get_move_lines(self, cr, uid, account_id, context=None):
        obj_move = self.pool.get('account.move.line')
        obj_search = obj_move.search(cr, uid, [('account_id','=',account_id),('reconcile_id','=',False)])
        move_lines = obj_move.browse(cr, uid, obj_search)
        
        return move_lines 
    
    def get_bank_accounts(self, cr, uid, account_id, context=None):
        account_ids = self.pool.get('account.account').search(cr, uid, [('parent_id','=',account_id)])
        accounts = self.pool.get('account.account').browse(cr, uid, account_ids)
        
        return accounts
    
    def get_bank_balance(self, cr, uid, accounts, context=None):
        total_debit = 0.0
        total_credit = 0.0
        total_invoice = 0.0
        total_payment = 0.0
        result = []
        
        for account in accounts:
            user_type = account.user_type.name
            if user_type == 'Banco Saldo Real':
                move_lines = self.get_move_lines(cr, uid, account.id, context)
                for move_line in move_lines:
                    amount = self.get_amount(cr, uid, move_line, account.currency_id.id)
                    if amount[0] == 'invoice':
                        total_invoice += amount[1]
                    elif amount[0] == 'payment':
                        total_payment += amount[1]
                    elif amount[0] == 'credit':
                        total_credit += amount[1]
                    elif amount[0] == 'debit':
                        total_debit += amount[1]
                        
        bank_balance = total_debit + total_credit + total_invoice + total_payment
        
        result.append(bank_balance)
        result.append(total_invoice)
        result.append(total_payment)
        result.append(total_debit)
        result.append(total_credit)
        
        return result
                
report_sxw.report_sxw(
    'report.l10n.cr.conciliation.bank.layout_ccorp',
    'account.account',
    'addons/l10n_cr_account_financial_report_webkit/report/conciliation_bank.mako',
    parser=conciliation_bank)

