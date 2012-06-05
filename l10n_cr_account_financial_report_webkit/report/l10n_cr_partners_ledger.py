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
        })

    def get_amount(self,cr, uid, account_move_line,field):
        move_line_obj = self.pool.get('account.move.line').browse(cr,uid,account_move_line['id'])
        account_obj = self.pool.get('account.account').browse(cr,uid,account_move_line['account_id'])
        
        obj_invoice = self.pool.get('account.invoice')
        invoice_search = obj_invoice.search(cr,uid,[('move_id','=',account_move_line['move_id'])])
        invoice = None
        if invoice_search != []:
            invoice = obj_invoice.browse(cr,uid,invoice_search[0])
        
        #invoice = account_move_line.invoice 
        
        obj_voucher = self.pool.get('account.voucher')
        voucher_search = obj_voucher.search(cr,uid,[('move_id','=',account_move_line['move_id'])])
        voucher = None
        if voucher_search != []:
            voucher = obj_voucher.browse(cr,uid,voucher_search[0])
        
        result_empty = 0.0
        
        if account_obj.type == 'receivable': #CxC
            amount_debit_sign = 1
            amount_credit_sign = 1
            
            if invoice:
                if invoice.type == 'out_invoice': # Customer Invoice 
                    if not account_obj.currency_id : 
                        if field == 'invoice':
                            res = amount_debit_sign * account_move_line['debit']
                        else:
                            res = result_empty
                    else:
                        if field == 'invoice':
                            res = amount_debit_sign * account_move_line['amount_currency']
                        else:
                            res = result_empty
                elif invoice.type == 'in_invoice': # Supplier Invoice
                    if not account_obj.currency_id : 
                        if field == 'invoice':
                            res = amount_debit_sign * account_move_line['credit']
                        else:
                            res = result_empty
                    else:
                        if field == 'invoice':
                            res = amount_debit_sign * account_move_line['amount_currency']
                        else:
                            res = result_empty
                elif invoice.type == 'out_refund': # Nota de Credito Customer
                    if not account_obj.currency_id : 
                        if field == 'credit':
                            res = amount_credit_sign * account_move_line['credit']
                        else:
                            res = result_empty
                    else:
                        if field == 'credit':
                            res = amount_credit_sign * account_move_line['amount_currency']
                        else:
                            res = result_empty
                elif invoice.type == 'in_refund': # Nota Debito Supplier
                    if not account_obj.currency_id : 
                        if field == 'debit':
                            res = amount_debit_sign * account_move_line['debit']
                        else:
                            res = result_empty
                    else:
                        if field == 'debit':
                            res = amount_debit_sign * account_move_line['amount_currency']
                        else:
                            res = result_empty
                else:
                    res = result_empty

            elif voucher:
                if voucher.type == 'sale': # 
                    if not account_obj.currency_id : 
                        if field == 'invoice':
                            res = amount_credit_sign * account_move_line['credit']
                        else:
                            res = result_empty
                    else:
                        if field == 'invoice':
                            res = amount_credit_sign * account_move_line['amount_currency']
                        else:
                            res = result_empty
                elif voucher.type == 'payment': # 
                    if not account_obj.currency_id : 
                        if field == 'payment':
                            res = amount_debit_sign * account_move_line['debit']
                        else:
                            res = result_empty
                    else:
                        if field == 'payment':
                            res = amount_debit_sign * account_move_line['amount_currency']
                        else:
                            res = result_empty
                elif voucher.type == 'purchase': # 
                    if not account_obj.currency_id : 
                        if field == 'debit':
                            res = amount_debit_sign * account_move_line['debit']
                        else:
                            res = result_empty
                    else:
                        if field == 'debit':
                            res = amount_debit_sign * account_move_line['amount_currency']
                        else:
                            res = result_empty
                elif voucher.type == 'receipt': # 
                    if move_line_obj.reconcile_id or move_line_obj.reconcile_partial_id:
                        if not account_obj.currency_id : 
                            if field == 'receipt':
                                res = amount_credit_sign * account_move_line['credit']
                            else:
                                res = result_empty
                        else:
                            if field == 'receipt':
                                res = amount_debit_sign * account_move_line['amount_currency']
                            else:
                                res = result_empty
                    else:
                        if not account_obj.currency_id : 
                            if field == 'credit':
                                res = amount_debit_sign * account_move_line['credit']
                            else:
                                res = result_empty
                        else:
                            if field == 'credit':
                                res = amount_debit_sign * account_move_line['amount_currency']
                            else:
                                res = result_empty
                else:
                    res = result_empty
                    
            else: # Manual Move
                if field == 'move':
                    if not account_obj.currency_id : 
                        if account_move_line['credit'] != 0.0 :
                            res = amount_credit_sign * account_move_line['credit']
                        elif account_move_line['debit'] != 0.0 :
                            res = amount_debit_sign * account_move_line['debit']
                        else:
                            res = result_empty
                    else:
                        if account_move_line['credit'] != 0.0 :
                            res = amount_credit_sign * account_move_line['amount_currency']
                        elif account_move_line['debit'] != 0.0 :
                            res = amount_debit_sign * account_move_line['amount_currency']
                else:
                    res = result_empty
        
        elif account_obj.type == 'payable': #CxP
            amount_debit_sign = 1
            amount_credit_sign = -1
            
            if invoice:
                if invoice.type == 'out_invoice': # Customer Invoice 
                    if not account_obj.currency_id : 
                        if field == 'invoice':
                            res = amount_debit_sign * account_move_line['debit']
                        else:
                            res = result_empty
                    else:
                        if field == 'invoice':
                            res = amount_debit_sign * account_move_line['amount_currency']
                        else:
                            res = result_empty
                elif invoice.type == 'in_invoice': # Supplier Invoice
                    if not account_obj.currency_id : 
                        if field == 'invoice':
                            res = amount_debit_sign * account_move_line['debit']
                        else:
                            res = result_empty
                    else:
                        if field == 'invoice':
                            res = amount_debit_sign * account_move_line['amount_currency']
                        else:
                            res = result_empty
                elif invoice.type == 'out_refund': # Nota de Credito Customer
                    if not account_obj.currency_id : 
                        if field == 'invoice':
                            res = amount_debit_sign * account_move_line['credit']
                        else:
                            res = result_empty
                    else:
                        if field == 'invoice':
                            res = amount_debit_sign * account_move_line['amount_currency']
                        else:
                            res = result_empty
                elif invoice.type == 'in_refund': # Nota Debito Supplier
                    if not account_obj.currency_id : 
                        if field == 'debit':
                            res = amount_debit_sign * account_move_line['credit']
                        else:
                            res = result_empty
                    else:
                        if field == 'debit':
                            res = amount_debit_sign * account_move_line['amount_currency']
                        else:
                            res = result_empty
                else:
                    res = result_empty

            elif voucher:
                if voucher.type == 'sale': # 
                    if not account_obj.currency_id : 
                        if field == 'invoice':
                            res = amount_credit_sign * account_move_line['credit']
                        else:
                            res = result_empty
                    else:
                        if field == 'invoice':
                            res = amount_credit_sign * account_move_line['amount_currency']
                        else:
                            res = result_empty
                elif voucher.type == 'payment': # 
                    if move_line_obj.reconcile_id or move_line_obj.reconcile_partial_id:
                        if not account_obj.currency_id : 
                            if field == 'payment':
                                res = amount_credit_sign * account_move_line['credit']
                            else:
                                res = result_empty
                        else:
                            if field == 'payment':
                                res = amount_debit_sign * account_move_line['amount_currency']
                            else:
                                res = result_empty
                    else:
                        if not account_obj.currency_id : 
                            if field == 'credit':
                                res = amount_debit_sign * account_move_line['debit']
                            else:
                                res = result_empty
                        else:
                            if field == 'credit':
                                res = amount_debit_sign * account_move_line['amount_currency']
                            else:
                                res = result_empty
                elif voucher.type == 'purchase': # 
                    if invoice:
                        if not account_obj.currency_id : 
                            if field == 'credit':
                                res = amount_debit_sign * account_move_line['credit']
                            else:
                                res = result_empty
                        else:
                            if field == 'credit':
                                res = amount_debit_sign * account_move_line['amount_currency']
                            else:
                                res = result_empty
                    else:
                        if not account_obj.currency_id : 
                            if field == 'debit':
                                res = amount_debit_sign * account_move_line['credit']
                            else:
                                res = result_empty
                        else:
                            if field == 'debit':
                                res = amount_debit_sign * account_move_line['amount_currency']
                            else:
                                res = result_empty
                elif voucher.type == 'receipt': # 
                    #if invoice:
                    if not account_obj.currency_id : 
                        if field == 'payment':
                            res = amount_debit_sign * account_move_line['credit']
                        else:
                            res = result_empty
                    else:
                        if field == 'payment':
                            res = amount_debit_sign * account_move_line['amount_currency']
                        else:
                            res = result_empty
                    #else:
                        #if not account_obj.currency_id : 
                            #if field == 'credit':
                                #res = amount_debit_sign * account_move_line['credit']
                            #else:
                                #res = result_empty
                        #else:
                            #if field == 'credit':
                                #res = amount_debit_sign * account_move_line['amount_currency']
                            #else:
                                #res = result_empty
                else:
                    res = result_empty
                    
            else: # Manual Move
                if field == 'move':
                    if not account_obj.currency_id : 
                        if account_move_line['credit'] != 0.0 :
                            res = amount_credit_sign * account_move_line['credit']
                        elif account_move_line['debit'] != 0.0 :
                            res = amount_debit_sign * account_move_line['debit']
                        else:
                            res = result_empty
                    else:
                        if account_move_line['credit'] != 0.0 :
                            res = amount_credit_sign * account_move_line['amount_currency']
                        elif account_move_line['debit'] != 0.0 :
                            res = amount_debit_sign * account_move_line['amount_currency']
                else:
                    res = result_empty
        
        
        
        
        
        return res
        
    def get_partner_name(self,cr,uid,partner_name, p_id, p_ref, p_name):
        
        res = ''
        if p_ref != None and p_name != None:
            res = res+p_ref+' '+p_name
        else:
            res =  partner_name
        
            
        return res

HeaderFooterTextWebKitParser('report.account_financial_report_webkit.account.account_report_partners_ledger_webkit',
                             'account.account',
                             'addons/l10n_cr_account_financial_report_webkit/report/l10n_cr_account_report_partners_ledger.mako',
                             parser=l10n_cr_PartnersLedgerWebkit)
