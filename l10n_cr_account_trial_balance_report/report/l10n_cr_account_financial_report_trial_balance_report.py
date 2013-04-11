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
from report import report_sxw
from tools.translate import _

from openerp.addons.account_report_lib.account_report_base import accountReportbase

class trialBalancereport(accountReportbase):
    
    def __init__(self, cr, uid, name, context):      
        super(trialBalancereport, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'cr': cr,
            'uid':uid,
            'get_data':self.get_data,
            'get_accounts':self.get_accounts,
            'filter_form': self.get_filter,
        })
    
    """   
       1. The report needs the accounts that match with the chart account selected
       2. With this accounts, get the initial balance
       3. With this accounts, get the move lines and calculate the debit and credit.
       
    """   
    
    def get_accounts (self, cr, uid, data):
        library_obj = self.pool.get('account.webkit.report.library')
        
        #Get the accounts with the chart account selected.
        chart_account_id = self.get_chart_account_id(data)
        
        #account list based on chart_account
        accounts_ids = library_obj.get_account_child_ids(cr, uid, chart_account_id.id) #-> this function return ids.
        
        return self.pool.get('account.account').browse(cr, uid, accounts_ids)
    
    def get_data (self, cr, uid, data):
        library_obj = self.pool.get('account.webkit.report.library')
        filter_data = [] #contains the start and stop period or dates.
        initial_balance = total_result = {}
        
        fiscal_year = self.get_fiscalyear(data)
        
        #get the filters
        filter_type = self.get_filter(data)        
                
        #Get the accounts with the chart account selected.
        chart_account_id = self.get_chart_account_id(data)
        
        #account list based on chart_account
        accounts_ids = library_obj.get_account_child_ids(cr, uid, chart_account_id.id) #-> this function return ids.

        target_move = self.get_target_move(data)
        
        ####################################################################################################
        # 1. Get the initial balance for all the accounts
        
        #el metodo get_account_balance devuelve un diccionario con la llave de la cuenta
        #y el valor que se le está pidiendo, en este caso el balance inicial.        
        if filter_type == 'filter_period':
            #el método recibe los ids de los períodos (filtro por períodos)            
            start_period_id = self.get_start_period(data).id
            end_period_id = self.get_end_period(data).id
            
            filter_data.append(self.get_start_period(data))
            filter_data.append(self.get_end_period(data))
            
            initial_balance = self.pool.get('account.webkit.report.library').get_account_balance(cr,
                                                                                        uid, 
                                                                                        accounts_ids, 
                                                                                        ['balance'],     
                                                                                        initial_balance=True,                                                                                   
                                                                                        fiscal_year_id=fiscal_year.id,                                                                                
                                                                                        state = target_move,
                                                                                        start_period_id = start_period_id,
                                                                                        end_period_id = end_period_id,
                                                                                        chart_account_id=chart_account_id.id,
                                                                                        filter_type=filter_type)
        if filter_type == 'filter_date':
            #el método recibe las fechas (en caso de filtro por fechas)
            start_date = self.get_date_from(data)
            end_date = self.get_date_to(data)
            
            filter_data.append(start_date)
            filter_data.append(end_date)
            
            initial_balance = self.pool.get('account.webkit.report.library').get_account_balance(cr, 
                                                                                        uid, 
                                                                                        accounts_ids, 
                                                                                        ['balance'],  
                                                                                        initial_balance=True, 
                                                                                        fiscal_year_id=fiscal_year.id,
                                                                                        state = target_move, 
                                                                                        start_date = start_date,                                                                      
                                                                                        end_date = end_date,                                                                                        
                                                                                        chart_account_id=chart_account_id.id,
                                                                                        filter_type=filter_type)
        if filter_type == 'filter_no':
            initial_balance = self.pool.get('account.webkit.report.library').get_account_balance(cr, 
                                                                                        uid, 
                                                                                        accounts_ids, 
                                                                                        ['balance'],  
                                                                                        initial_balance=True, 
                                                                                        fiscal_year_id=fiscal_year.id,
                                                                                        state = target_move, 
                                                                                        chart_account_id=chart_account_id.id,
                                                                                        filter_type='')
        #2. Get the debit and credit.
        debit_credit_totals = library_obj.calculate_debit_credit_for_account(cr, uid,
                                                                             accounts_ids,
                                                                             filter_type=filter_type,
                                                                             filter_data=filter_data,
                                                                             fiscalyear=fiscal_year,
                                                                             target_move = target_move)
        
        #3. Compute the 4 fields and return a dictionary, where the key is the account_id
        for account in accounts_ids:
            total_result [account] = {'initial_balance':initial_balance[account]['balance'],
                                      'debit': debit_credit_totals[account]['debit'],
                                      'credit': debit_credit_totals[account]['credit'],
                                      'balance': initial_balance[account]['balance'] + debit_credit_totals[account]['debit'] - debit_credit_totals[account]['credit']}
        return total_result

report_sxw.report_sxw(
    'report.l10n_cr_trial_balance_report',
    'account.account',
    'addons/l10n_cr_account_trial_balance_report/report/l10n_cr_account_financial_report_trial_balance_report.mako',
    parser=trialBalancereport)
