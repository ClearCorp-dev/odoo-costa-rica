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

from openerp.addons.account_financial_report_webkit.report.common_reports import CommonReportHeaderWebkit
from openerp.addons.account_financial_report_webkit.report.partners_ledger import PartnersLedgerWebkit

class conciliation_bank(report_sxw.rml_parse, CommonReportHeaderWebkit):
    
    def __init__(self, cursor, uid, name, context):
        super(conciliation_bank, self).__init__(cursor, uid, name, context=context)
        self.pool = pooler.get_pool(self.cr.dbname)
        self.cursor = self.cr
        
        self.localcontext.update({
            'time': time,
            'cr' : cursor,
            'uid': uid,
            'get_amount': self.get_amount,
            'get_bank_data': self.get_bank_data,
            'get_bank_account': self.get_bank_account,
            'filter_form': self._get_filter,
            'display_target_move': self._get_display_target_move,
        })
    
    def set_context(self, objects, data, ids, report_type=None):
        main_filter = self._get_form_param('filter', data, default='filter_no')
        target_move = self._get_form_param('target_move', data, default='all')
        start_date = self._get_form_param('date_from', data)
        stop_date = self._get_form_param('date_to', data)
        input_bank_balance = self._get_form_param('bank_balance', data)
        start_period = self.get_start_period_br(data)
        stop_period = self.get_end_period_br(data)
        fiscalyear = self.get_fiscalyear_br(data)
        chart_account = self._get_chart_account_id_br(data)
        
        if main_filter == 'filter_no' and fiscalyear:
            start_period = self.get_first_fiscalyear_period(fiscalyear)
            stop_period = self.get_last_fiscalyear_period(fiscalyear)            
        elif main_filter == 'filter_date':
            start = start_date
            stop = stop_date
        else:
            start = start_period
            stop = stop_period
            
        self.localcontext.update({
            'fiscalyear': fiscalyear,
            'start_date': start_date,
            'stop_date': stop_date,
            'start_period': start_period,
            'stop_period': stop_period,
            'target_move': target_move,
            'input_bank_balance': input_bank_balance,
            'chart_account': chart_account,
            
        })

        return super(conciliation_bank, self).set_context(objects, data, ids,
                                                            report_type=report_type)

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

    def get_bank_data(self, cr, uid, parent_account_id, filter_type, filter_data, fiscalyear, target_move, context=None):
        result_bank_balance = {}
        result_move_lines = []
        filters = {}

        account_obj = self.pool.get('account.account')
        account_webkit_report_library_obj = self.pool.get('account.webkit.report.library')
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
        incomes_to_register = 0.0
        credits_to_reconcile = 0.0
        expenditures_to_register = 0.0
        debits_to_reconcile = 0.0
        accounting_total = 0.0
        bank_total = 0.0
        
        '''
        #Filters for the move lines to use in get_account_balance 
        filters['fiscalyear'] = fiscalyear.id
        if filter_type == 'filter_date':
            filters['date_from'] = filter_data[0] 
            filters['date_to'] = filter_data[1]
        elif filter_type == 'filter_period':
            periods_ids = self.pool.get('account.period').search(cr, uid, [('date_stop', '<=', filter_data[1].date_stop)])
            filters['periods'] = periods_ids 
        '''
        fiscal_year_id = fiscalyear.id
        if filter_type == 'filter_date':
            period_ids = False
            end_date = filter_data[1].id
        elif filter_type == 'filter_period':
            period_ids = self.pool.get('account.period').search(cr, uid, [('date_stop', '<=', filter_data[1].date_stop)])
            end_date = False
        
        
        #TODO: Set the max date or period list for the balance query from the wizard data
        #      If the wizard is filtered by date, the max date is entered as is
        #      If the wizard is filtered by period, the query needs the valid list of periods in a WHERE statement form
        balance_query_filter = ''
        if account_is_foreign:
            
            bank_balance = account_webkit_report_library_obj.get_account_balance(cr,
                                                uid,
                                                [reconciled_account.id],
                                                ['balance'],
                                                end_date=end_date,
                                                period_ids=period_ids,
                                                fiscal_year_id=fiscal_year_id,
                                                context=context)[reconciled_account.id]['balance']
            accounting_balance = account_webkit_report_library_obj.get_account_balance(cr,
                                                uid,
                                                [parent_account_id],
                                                ['balance'],
                                                end_date=end_date,
                                                period_ids=period_ids,
                                                fiscal_year_id=fiscal_year_id,
                                                context=context)[parent_account_id]['balance']
        else:
            bank_balance = account_webkit_report_library_obj.get_account_balance(cr,
                                                uid,
                                                [reconciled_account.id],
                                                ['balance'],
                                                end_date=end_date,
                                                period_ids=period_ids,
                                                fiscal_year_id=fiscal_year_id,
                                                context=context)[reconciled_account.id]['balance']
            accounting_balance = account_webkit_report_library_obj.get_account_balance(cr,
                                                uid,
                                                [parent_account_id],
                                                ['balance'],
                                                end_date=end_date,
                                                period_ids=period_ids,
                                                fiscal_year_id=fiscal_year_id,
                                                context=context)[parent_account_id]['balance']
            
            '''
            bank_balance = reconciled_account.foreign_balance
            accounting_balance = parent_account.foreign_balance
        else:
            bank_balance = reconciled_account.balance
            accounting_balance = parent_account.balance
            '''

        move_obj = self.pool.get('account.move')
        move_line_obj = self.pool.get('account.move.line')
        
        unreconciled_move_lines = account_webkit_report_library_obj.get_move_lines(cr, uid, transit_account_ids, filter_type=filter_type, filter_data=filter_data, fiscalyear=fiscalyear, target_move=target_move, unreconcile = True, context=context)
        
        result_move_lines = {
            'credits_to_reconcile' :     [],
            'debits_to_reconcile' :    [],
            'incomes_to_register' :      [],
            'expenditures_to_register' :     [],
        }
        for line in unreconciled_move_lines:
            move = line.move_id
            if not move:
                if account_is_foreign:
                    if line.amount_currency > 0:
                        result_move_lines['incomes_to_register'].append(line)
                        incomes_to_register += line.amount_currency
                    else:
                        result_move_lines['expenditures_to_register'].append(line)
                        expenditures_to_register -= line.amount_currency
                else:
                    if line.debit > 0:
                        result_move_lines['incomes_to_register'].append(line)
                        incomes_to_register += line.debit
                    else:
                        result_move_lines['expenditures_to_register'].append(line)
                        expenditures_to_register += line.credit
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
                        result_move_lines['incomes_to_register'].append(line)
                        incomes_to_register += line.amount_currency
                    else:
                        result_move_lines['expenditures_to_register'].append(line)
                        expenditures_to_register -= line.amount_currency
                else:
                    if line.debit > 0:
                        result_move_lines['incomes_to_register'].append(line)
                        incomes_to_register += line.debit
                    else:
                        result_move_lines['expenditures_to_register'].append(line)
                        expenditures_to_register += line.credit
            else:
                #Debit or credit to register: present in statement but not in other accounts
                if contra_line.account_id.id == reconciled_account.id:
                    if account_is_foreign:
                        if line.amount_currency < 0:
                            result_move_lines['incomes_to_register'].append(line)
                            incomes_to_register -= line.amount_currency
                        else:
                            result_move_lines['expenditures_to_register'].append(line)
                            expenditures_to_register += line.amount_currency
                    else:
                        if line.credit > 0:
                            result_move_lines['incomes_to_register'].append(line)
                            incomes_to_register += line.credit
                        else:
                            result_move_lines['expenditures_to_register'].append(line)
                            expenditures_to_register += line.debit
                #Debit or credit to reconcile: present in other accounts but not in statements
                else:
                    if account_is_foreign:
                        if line.amount_currency > 0:
                            result_move_lines['credits_to_reconcile'].append(line)
                            credits_to_reconcile += line.amount_currency
                        else:
                            result_move_lines['debits_to_reconcile'].append(line)
                            debits_to_reconcile -= line.amount_currency
                    else:
                        if line.debit > 0:
                            result_move_lines['credits_to_reconcile'].append(line)
                            credits_to_reconcile += line.debit
                        else:
                            result_move_lines['debits_to_reconcile'].append(line)
                            debits_to_reconcile += line.credit

        accounting_total = accounting_balance + incomes_to_register - expenditures_to_register
        bank_total = bank_balance + credits_to_reconcile - debits_to_reconcile

        result_bank_balance = {
            'input_bank_balance' : input_bank_balance,
            'bank_balance' : bank_balance,
            'accounting_balance' : accounting_balance,
            'incomes_to_register' : incomes_to_register,
            'credits_to_reconcile' : credits_to_reconcile,
            'expenditures_to_register' : expenditures_to_register,
            'debits_to_reconcile' : debits_to_reconcile,
            'accounting_total' : accounting_total,
            'bank_total' : bank_total,
        }
        
        return result_bank_balance, result_move_lines, account_is_foreign
    
    def get_bank_account(self, cr, uid, data):
        info = data.get('form', {}).get('bank_account_ids')
        if info:
            bank_account = self.pool.get('account.account').browse(cr, uid, info[0])
            return bank_account
        return False
    

report_sxw.report_sxw(
    'report.account_financial_report_webkit.account.account_report_conciliation_bank_webkit',
    'account.account',
    'addons/l10n_cr_account_banking_reports/report/conciliation_bank.mako',
    parser=conciliation_bank)

