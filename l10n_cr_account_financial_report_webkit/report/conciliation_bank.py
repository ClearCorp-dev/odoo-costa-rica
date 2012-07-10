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
            'get_bank_data': self.get_bank_data,
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

    def get_bank_data(self, cr, uid, parent_account_id, context=None):
        result_bank_balance = {}
        result_move_lines = []

        account_obj = self.pool.get('account.account')
        parent_account = account_obj.browse(cr, uid, parent_account_id)
        child_account_ids = account_obj.search(cr, uid, [('parent_id','=',parent_account_id)])
        child_accounts = child_account_ids and account_obj.browse(cr, uid, child_account_ids) or False

        if not child_accounts:
            return result_bank_balance, result_move_lines, account_foreign

        if parent_account.report_currency_id:
            account_currency = parent_account.report_currency_id
        elif parent_account.currency_id:
            account_currency = parent_account.currency_id
        else:
            account_currency = parent_account.company_id.currency_id
        if account_currency.id == parent_account.company_id.currency_id.id:
            account_is_foreign = False
        else:
            account_is_foreign = True

        reconciled_account = None
        transit_accounts = []
        transit_account_ids = []
        for child_account in child_accounts:
            #TODO: get the user types for the reconciled_account from system properties
            if child_account.user_type.code == 'BKRE':
                reconciled_account = child_account
            else:
                if child_account.reconcile:
                    transit_accounts.append(child_account)
                    transit_account_ids.append(child_account.id)

        #A reconciled_account and at least one transit_account is needed
        if not (reconciled_account or transit_accounts):
            return result_bank_balance, result_move_lines, account_foreign

        #TODO: set input_bank_balance with data from wizard
        input_bank_balance = 0.0
        bank_balance = 0.0
        accounting_balance = 0.0
        debits_to_register = 0.0
        debits_to_reconcile = 0.0
        credits_to_register = 0.0
        credits_to_reconcile = 0.0
        accounting_total = 0.0
        bank_total = 0.0

        #TODO: Set the max date or period list for the balance query from the wizard data
        #      If the wizard is filtered by date, the max date is entered as is
        #      If the wizard is filtered by period, the query needs the valid list of periods in a WHERE statement form
        balance_query_filter = ''
        if account_is_foreign:
            '''
            bank_balance = account_obj.__compute(cr,
                                                 uid,
                                                 [reconciled_account.id],
                                                 ['balance'],
                                                 query=balance_query_filter)[reconciled_account.id]['balance']
            accounting_balance = account_obj.__compute(cr,
                                                       uid,
                                                       [parent_account_id],
                                                       ['balance'],
                                                       query=balance_query_filter)[parent_account_id]['balance']
        else:
            bank_balance = account_obj.__compute(cr,
                                                 uid,
                                                 [reconciled_account.id],
                                                 ['balance'],
                                                 query=balance_query_filter)[reconciled_account.id]['foreign_balance']
            accounting_balance = account_obj.__compute(cr,
                                                       uid,
                                                       [parent_account_id],
                                                       ['balance'],
                                                       query=balance_query_filter)[parent_account_id]['foreign_balance']
            '''
            bank_balance = reconciled_account.foreign_balance
            accounting_balance = parent_account.foreign_balance
        else:
            bank_balance = reconciled_account.balance
            accounting_balance = parent_account.balance

        move_obj = self.pool.get('account.move')
        move_line_obj = self.pool.get('account.move.line')
        unreconciled_move_line_ids = move_line_obj.search(cr, uid, [('account_id','in',transit_account_ids),('reconcile_id','=',False)])
        unreconciled_move_lines = unreconciled_move_line_ids and move_line_obj.browse(cr, uid, unreconciled_move_line_ids) or False
        result_move_lines = {
            'debits_to_reconcile' :     [],
            'credits_to_reconcile' :    [],
            'debits_to_register' :      [],
            'credits_to_register' :     [],
        }
        for line in unreconciled_move_lines:
            move = line.move_id
            if not move:
                if account_is_foreign:
                    if line.amount_currency > 0:
                        result_move_lines['debits_to_register'].append(line)
                        debits_to_register += line.amount_currency
                    else:
                        result_move_lines['credits_to_register'].append(line)
                        credits_to_register -= line.amount_currency
                else:
                    if line.debit > 0:
                        result_move_lines['debits_to_register'].append(line)
                        debits_to_register += line.debit
                    else:
                        result_move_lines['credits_to_register'].append(line)
                        credits_to_register += line.credit
                print "No move"
                continue

            #Select the best contra move line (biggest amount, inverse amount from line)
            contra_line = line
            for other_line in move.line_id:
                if other_line.id == line.id:
                    continue
                elif other_line.debit == line.credit or other_line.credit == line.debit:
                    contra_line = other_line
                    break
                elif account_is_foreign and (other_line.amount_currency == -1 * line.amount_currency):
                    contra_line = other_line
                    break
                if (line.debit != 0 and contra_line.credit > other_line.credit) or \
                   (line.credit != 0 and contra_line.debit < other_line.debit):
                    contra_line = other_line
                elif (account_is_foreign and
                      (
                       (line.amount_currency > 0 and
                        contra_line.amount_currency < other_line.amount_currency)
                       or
                       (line.amount_currency <= 0 and
                        contra_line.amount_currency > other_line.amount_currency)
                      )
                     ):
                    contra_line = other_line

            if line.id == contra_line.id:
                if account_is_foreign:
                    if line.amount_currency > 0:
                        result_move_lines['debits_to_register'].append(line)
                        debits_to_register += line.amount_currency
                    else:
                        result_move_lines['credits_to_register'].append(line)
                        credits_to_register -= line.amount_currency
                else:
                    if line.debit > 0:
                        result_move_lines['debits_to_register'].append(line)
                        debits_to_register += line.debit
                    else:
                        result_move_lines['credits_to_register'].append(line)
                        credits_to_register += line.credit
            else:
                #Debit or credit to register: present in statement but not in other accounts
                if contra_line.account_id.id == reconciled_account.id:
                    if account_is_foreign:
                        if line.amount_currency < 0:
                            result_move_lines['debits_to_register'].append(line)
                            debits_to_register -= line.amount_currency
                        else:
                            result_move_lines['credits_to_register'].append(line)
                            credits_to_register += line.amount_currency
                    else:
                        if line.credit > 0:
                            result_move_lines['debits_to_register'].append(line)
                            debits_to_register += line.credit
                        else:
                            result_move_lines['credits_to_register'].append(line)
                            credits_to_register += line.debit
                #Debit or credit to reconcile: present in other accounts but not in statements
                else:
                    if account_is_foreign:
                        if line.amount_currency > 0:
                            result_move_lines['debits_to_reconcile'].append(line)
                            debits_to_reconcile += line.amount_currency
                        else:
                            result_move_lines['credits_to_reconcile'].append(line)
                            credits_to_reconcile -= line.amount_currency
                    else:
                        if line.debit > 0:
                            result_move_lines['debits_to_reconcile'].append(line)
                            debits_to_reconcile += line.debit
                        else:
                            result_move_lines['credits_to_reconcile'].append(line)
                            credits_to_reconcile += line.credit

        accounting_total = accounting_balance + debits_to_register - credits_to_register
        bank_total = bank_balance + debits_to_reconcile - credits_to_reconcile

        result_bank_balance = {
            'input_bank_balance' : input_bank_balance,
            'bank_balance' : bank_balance,
            'accounting_balance' : accounting_balance,
            'debits_to_register' : debits_to_register,
            'debits_to_reconcile' : debits_to_reconcile,
            'credits_to_register' : credits_to_register,
            'credits_to_reconcile' : credits_to_reconcile,
            'accounting_total' : accounting_total,
            'bank_total' : bank_total,
        }
        
        return result_bank_balance, result_move_lines, account_is_foreign

report_sxw.report_sxw(
    'report.l10n.cr.conciliation.bank.layout_ccorp',
    'account.account',
    'addons/l10n_cr_account_financial_report_webkit/report/conciliation_bank.mako',
    parser=conciliation_bank)

