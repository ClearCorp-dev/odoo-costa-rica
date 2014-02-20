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
from tools.translate import _
from openerp.osv import fields, osv

from openerp.addons.account_report_lib.account_report_base import accountReportbase

class Parser(accountReportbase):
    
    def __init__(self, cr, uid, name, context):
        #change uid by 1, because 1 is the id for the admin user
        #problems with partner read.
        super(Parser, self).__init__(cr, 1, name, context=context)
        self.pool = pooler.get_pool(self.cr.dbname)
        self.cursor = self.cr
        
        self.localcontext.update({
            'time': time,
            'cr' : cr,
            'uid': uid,
            
            'get_bank_balance': self.get_bank_balance,
            'get_amount': self.get_amount,
            'get_data': self.get_data,       
            
            #====================SET AND GET METHODS ===========================
            'storage':{},
            'set_data_template': self.set_data_template,
            #===================================================================
        })
    
    #===============================================================================
    #    get_data_template set_data_template and methods are used to create a workarround 
    #    (not found a way to have temporary variables in a template in aeroo). 
    #    The set method calls the methods that do the calculations and stores them 
    #    in a dictionary that is built into the localcontext, called storage. 
    #    All values ​​are stored in this dictionary.
    # 
    #    Then get_data_template method that receives a string, which is the key of the dictionary, 
    #    pass the value of the key we want and this method returns the value stored in this key.
    # 
    #    Set_data_template method is called in the template if odt as follows: 
    #    <if test="set_data_template(cr, uid, data)"> </if>. 
    #    In this way, we obtain the values ​​and can work with them directly in the template odt,
    #     shaped <get_data_template('key')>.
    #===============================================================================
    
    #set data to use in odt template. 
    def set_data_template(self, cr, uid, data):        
        account_id = self.get_accounts_ids(cr, uid, data).id               
        bank_balance, bank_move_lines, account_is_foreign = self.get_data(cr, uid, data, account_id)
        input_bank_balance = self.get_bank_balance(data)
        
        dict_update = {
                       'account_id': account_id,
                       'bank_move_lines': bank_move_lines,
                       'account_is_foreign': account_is_foreign,
                       'input_bank_balance': input_bank_balance,
                       #========================================================
                       'bank_balance': bank_balance['bank_balance'],
                       'accounting_balance': bank_balance['accounting_balance'],
                       'accounting_total': bank_balance['accounting_total'],
                       'bank_total': bank_balance['bank_total'],
                       #========================================================
                       'incomes_to_register': bank_balance['incomes_to_register'],
                       'credits_to_reconcile': bank_balance['credits_to_reconcile'],
                       'expenditures_to_register': bank_balance['expenditures_to_register'],
                       'debits_to_reconcile': bank_balance['debits_to_reconcile'],
                       #*************************************************************
                       #========================================================
                       }
        
        self.localcontext['storage'].update(dict_update)
        return False

    #==========================================================================
 
    #Extract bank_balance from wizard.
    def get_bank_balance(self, data):
        return self._get_form_param('bank_balance', data)
    
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

    def get_data(self, cr, uid, data, parent_account_id, context=None):
        result_bank_balance = {}
        result_move_lines = []
        filters = {}
        account_foreign = False
        filter_data = []
        reconciled_account = None
        transit_accounts = []
        transit_account_ids = []
        input_bank_balance = self.get_bank_balance(data) or 0.0 #Extract bank_balance from wizard
        bank_balance = 0.0
        accounting_balance = 0.0
        incomes_to_register = 0.0
        credits_to_reconcile = 0.0
        expenditures_to_register = 0.0
        debits_to_reconcile = 0.0
        accounting_total = 0.0
        bank_total = 0.0        
        
        account_obj = self.pool.get('account.account')
        account_webkit_report_library_obj = self.pool.get('account.webkit.report.library')
        
        #######################Parameters
        fiscalyear = self.get_fiscalyear(data)
        target_move = self.get_target_move(data)
        historic_strict = self.get_historic_strict(data)
        special_period = self.get_special_period(data)
        filter_type = self.get_filter(data)
        
        #Build fiscal_year and filter_data
        if fiscalyear: 
            fiscal_year_id = fiscalyear.id
        else:
            fiscal_year_id = False
            
        if filter_type == 'filter_date':
            period_ids = False
            end_date = self.get_date_to(data)
            
            #Build the filter data
            filter_data.append(None)
            filter_data.append(end_date)
            
        elif filter_type == 'filter_period':
            period_ids = [self.get_end_period(data).id]            
            end_date = False
            
            #Build the filter data
            filter_data.append(None)
            filter_data.append(self.get_end_period(data))
        
        ######################Account configuration
        #1. Get acccount_id (parent_account) selected in wizard       
        parent_account = account_obj.browse(cr, uid, parent_account_id)

        #2. Get child of this account
        child_account_ids = account_obj.search(cr, uid, [('parent_id','=',parent_account_id)])
        child_accounts = child_account_ids and account_obj.browse(cr, uid, child_account_ids) or False

        #Return empty values if account doesn't have children.
        if not child_accounts:
            return result_bank_balance, result_move_lines, account_foreign
        
        #Check values 
        for child_account in child_accounts:
            '''
                *** NOTE: This part required previous configuration ***
                One of child_accounts must have include_conciliation_report attribute checked as True.
                This account is reconciled_account, other accounts are transit_accounts.
            '''
            #Account with include_conciliation_report checked is reconciled_account
            if child_account.user_type.include_conciliation_report == True:
                reconciled_account = child_account
            else:
                #Others accounts are transit accounts.
                if child_account.reconcile:
                    transit_accounts.append(child_account)
                    transit_account_ids.append(child_account.id)

        #A reconciled_account and at least one transit_account is needed
        #Return an error if those accounts don't exist.
        if not reconciled_account:
            raise osv.except_osv(_('Error !'),_('Reconciled account does not exist. Check your configuration!'))
        
        elif not transit_accounts:
            raise osv.except_osv(_('Error !'),_('Transit account does not exist. Check your configuration!'))
        
        #######################################################################################################
        
        #############If accounts configuration is correct, procedeed with report.
        #3. Check currency
        if parent_account.report_currency_id:
            account_currency = parent_account.report_currency_id
        elif parent_account.currency_id:
            account_currency = parent_account.currency_id
        else:
            account_currency = parent_account.company_id.currency_id
        
        #4. Define if account currency is same that company currency
        if account_currency.id == parent_account.company_id.currency_id.id:
            account_is_foreign = False
        else:
            account_is_foreign = True
        
        #######################################################################
        
        #Compute balances.        
        if account_is_foreign:            
            bank_balance = account_webkit_report_library_obj.get_account_balance(cr,
                                                1,
                                                [reconciled_account.id],
                                                ['balance'],
                                                filter_type = filter_type,
                                                end_date=end_date,
                                                period_ids=period_ids,
                                                fiscal_year_id=fiscal_year_id,
                                                context=context)[reconciled_account.id]['balance']

            accounting_balance = account_webkit_report_library_obj.get_account_balance(cr,
                                                1,
                                                [parent_account_id],
                                                ['balance'],
                                                filter_type = filter_type,
                                                end_date=end_date,
                                                period_ids=period_ids,
                                                fiscal_year_id=fiscal_year_id,
                                                context=context)[parent_account_id]['balance']
        else:
            bank_balance = account_webkit_report_library_obj.get_account_balance(cr,
                                                1,
                                                [reconciled_account.id],
                                                ['balance'],
                                                filter_type = filter_type,
                                                end_date=end_date,
                                                period_ids=period_ids,
                                                fiscal_year_id=fiscal_year_id,
                                                context=context)[reconciled_account.id]['balance']
                                                
            accounting_balance = account_webkit_report_library_obj.get_account_balance(cr,
                                                1,
                                                [parent_account_id],
                                                ['balance'],
                                                filter_type = filter_type,
                                                end_date=end_date,
                                                period_ids=period_ids,
                                                fiscal_year_id=fiscal_year_id,
                                                context=context)[parent_account_id]['balance']
        
        move_obj = self.pool.get('account.move')
        move_line_obj = self.pool.get('account.move.line')
                
        unreconciled_move_lines = account_webkit_report_library_obj.get_move_lines(cr, 1, transit_account_ids, filter_type=filter_type, filter_data=filter_data, fiscalyear=fiscalyear, target_move=target_move, unreconcile = True, historic_strict=historic_strict, special_period=special_period, context=context)
        
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
                #print "No move"
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



