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

from openerp import pooler
from openerp.report import report_sxw
from openerp.tools.translate import _
from copy import copy
import types
import locale
from openerp.osv import osv, orm
from openerp import models, fields

from openerp.addons.account_report_lib.account_report_base import accountReportbase

class Parser(accountReportbase):
    
    def __init__(self, cr, uid, name, context):
        super(Parser, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'cr': cr,
            'uid':uid,
            'context':context,
            #'pool': pooler,
            'get_data':self.get_data,
        })
   
    '''
        If the display_detail == display_flat, compute all the balance, debit, credit and initial_balance and return 
        one result for each type account selected in the list.
        @param child_list: Can be a list of ids (int) or a browse record list.
    '''
        
    def compute_data(self, cr, uid, 
                                result_dict, 
                                child_list, 
                                filter_type='', 
                                filter_data=None, 
                                fiscalyear=None, 
                                target_move='all', 
                                unreconcile = False, 
                                historic_strict= False, 
                                special_period = False, 
                                all_accounts = True,
                                context=None):
        
        balance = 0.0
        credit = 0.0
        debit = 0.0
        initial_balance = 0.0 
        res = {}
        list_accounts = []
        account_report_lib = self.pool.get('account.webkit.report.library')
        
        #Distinct how return the results if in 4 singles variables or in a dictionary, where key is account_id
        #With all_accounts = False, return a dictionary with account_id as key and four values: Balance, credit, debit and initial_balance
        if all_accounts:
            #Child list can be a list of int or browse_record list
            for c in child_list:                
                if isinstance(c, orm.browse_record):
                    list_accounts.append(c.id)
                    account_id = c.id
                    
                elif isinstance(c, int):
                     list_accounts.append(c)
                     account_id = c
                
                if account_id in result_dict.keys():
                    initial_balance += result_dict[account_id]['balance']
                    
            #Call get_move_lines method to calculate debit and credit 
            move_lines = account_report_lib.get_move_lines(cr, uid, 
                                         account_ids = list_accounts, 
                                         filter_type=filter_type, 
                                         filter_data=filter_data, 
                                         fiscalyear=fiscalyear, 
                                         target_move=target_move, 
                                         unreconcile=unreconcile, 
                                         historic_strict=historic_strict, 
                                         special_period=special_period, 
                                         context=context)
            
            # Compute debit and credit amounts                                
            for line in move_lines:
                debit += line.debit
                credit += line.credit
                
            balance += initial_balance + debit - credit
                
            return balance, debit, credit, initial_balance
        
        else:
            for c in child_list:
                balance = 0.0 
                credit = 0.0 
                debit = 0.0 
                initial_balance = 0.0               
                
                if isinstance(c, orm.browse_record):
                    account_id = c.id
                    
                elif isinstance(c, int):
                     account_id = c                
            
                initial_balance = result_dict[account_id]['balance']
                
                move_lines = account_report_lib.get_move_lines(cr, uid, 
                                         account_ids = [account_id], 
                                         filter_type=filter_type, 
                                         filter_data=filter_data, 
                                         fiscalyear=fiscalyear, 
                                         target_move=target_move, 
                                         unreconcile=unreconcile, 
                                         historic_strict=historic_strict, 
                                         special_period=special_period, 
                                         context=context)
                
                # Compute debit and credit amounts                                
                for line in move_lines:
                    debit += line.debit
                    credit += line.credit
                    
                balance += initial_balance + debit - credit
                
                res[account_id] = {
                                   'initial_balance': initial_balance,
                                   'debit': debit,
                                   'credit': credit,
                                   'balance': balance, 
                                   
                                   }
                
            return res
    
    """ 
        Main methods to compute data. Split account.financial.report types in different
        methods to improve usabillity and maintenance. 
    """
    
    #Method for account.financial.report account_type type. 
    def get_data_account_type(self, cr, uid, filter_data, fiscal_year, filter_type,  target_move, chart_account_id, start_date, end_date, start_period_id, end_period_id, structure={}, final_list=[]):
        
        result_dict = {}
        final_data_parent = {'child_list': []} #Define empty list, avoid problem when list is empty and key isn't created
        final_data = {}
        list_ids = []
        child_list = []
        
        library_obj = self.pool.get('account.webkit.report.library') 
        
        #1. Extract children. It's a list of dictionaries.
        child_list = structure['account_type_child']       
        
        '''
            Display_detail = no_detail = special case
        '''        
        #no_detail: Iterate in the list and compute result in one line.
        if structure['display_detail'] == 'no_detail':
            final_data_parent['name'] = structure['name']
            final_data_parent['code'] = '' 
            final_data_parent['is_parent'] = False
            final_data_parent['level'] = 0
            final_data_parent['display_detail'] = 'no_detail'   
            
            #In account type, iterate in child, because child is all accounts that
            #match with account types selected.
            for parent, child in child_list.iteritems():
                #Add child id to compute data
                for c in child:
                    list_ids.append(c.id)
                
            if len(list_ids) > 0:
                #Compute the balance, debit and credit for child ids list.  
                #Try to reduce numbers of call to get_account_balance method.       
                result_dict = library_obj.get_account_balance(cr,uid, 
                                                                    list_ids, 
                                                                    ['balance'],     
                                                                    initial_balance=True,                                                                                   
                                                                    fiscal_year_id=fiscal_year.id,                                                                                
                                                                    state = target_move,
                                                                    start_date= start_date,
                                                                    end_date=end_date,
                                                                    start_period_id = start_period_id,
                                                                    end_period_id = end_period_id,
                                                                    chart_account_id=chart_account_id.id,
                                                                    filter_type=filter_type)
                
                #Compute all result in one line.
                #list_ids have all the accounts.
                all_accounts = True
                balance, debit, credit, initial_balance = self.compute_data(cr, uid, 
                                                        result_dict, 
                                                        list_ids, 
                                                        filter_type=filter_type, 
                                                        filter_data=filter_data, 
                                                        fiscalyear=fiscal_year, 
                                                        target_move=target_move,
                                                        all_accounts=all_accounts)
    
                final_data_parent.update({
                                            'initial_balance':initial_balance,
                                            'credit':credit,
                                            'debit':debit,
                                            'balance': balance,
                                          })
                    
            else:
                final_data_parent.update({
                                             'initial_balance':0.0,
                                             'credit':0.0,
                                             'debit':0.0,
                                             'balance': 0.0,
                                            })
                
            #Update the dictionary with final results.
            final_list.append(copy(final_data_parent))                    
            
        else:  
            '''
                Optimization process: Call get_account_balance the least possible.
            '''
            if child_list:
                #2. Create dictionaries for parent and children.
                for parent, child in child_list.iteritems():
                   final_data_parent['id'] = parent.id
                   final_data_parent['name'] = parent.name
                   final_data_parent['code'] = parent.code
                   final_data_parent['is_parent'] = True #Distinct child from parent.
                   final_data_parent['level'] = 0
                   
                   if child != []:
                        final_data_parent['child_list'] = child
                   else:
                        final_data_parent['child_list'] = []
 
                   if structure['display_detail'] == 'detail_flat':
                        #Update keys to numbers, because this keys now show results
                        final_data_parent['initial_balance'] = 0.0
                        final_data_parent['debit'] = 0.0
                        final_data_parent['credit'] = 0.0
                        final_data_parent['balance'] = 0.0
                        
                        #Add parent into list
                        final_list.append(copy(final_data_parent))
                        
                   elif structure['display_detail'] == 'detail_with_hierarchy':
                        final_data_parent['initial_balance'] = ''
                        final_data_parent['debit'] = ''
                        final_data_parent['credit'] = ''
                        final_data_parent['balance'] = ''
                        
                        #Add parent into list
                        final_list.append(copy(final_data_parent))
                                   
                        #Build child in a dictionary
                        if 'child_list' in final_data_parent.keys():   
                           for c in final_data_parent['child_list']:                                                        
                               final_data['id'] = c.id
                               final_data['level'] = c.level
#                               if 'child' in final_data:
#                                   final_data['child'] = c.child
                               final_data['name'] = c.name
                               final_data['code'] = c.code
                               final_data['is_parent'] = False
                               
                               final_list.append(copy(final_data))                           
                  
                   #Add child in final list and id to compute data.
                   for c in child:
                       list_ids.append(c.id)
                
                if len(list_ids) > 0: 
                      #Compute the balance, debit and credit for child ids list.         
                      result_dict = library_obj.get_account_balance(cr, uid, 
                                                                        list_ids, 
                                                                        ['balance'],     
                                                                        initial_balance=True,                                                                                   
                                                                        fiscal_year_id=fiscal_year.id,                                                                                
                                                                        state = target_move,
                                                                        start_date= start_date,
                                                                        end_date=end_date,
                                                                        start_period_id = start_period_id,
                                                                        end_period_id = end_period_id,
                                                                        chart_account_id=chart_account_id.id,
                                                                        filter_type=filter_type)
                      
                #Iterate again the list for improve performance. Compute results.
                if structure['display_detail'] == 'detail_flat':
                    #final_list has categories and child of this categories
                    #Compute results for each category 
                    all_accounts = True
                    for data in final_list:          
                        if 'child_list' in data.keys():
                           balance, debit, credit, initial_balance = self.compute_data(cr, uid, 
                                                        result_dict, 
                                                        list_ids, 
                                                        filter_type=filter_type, 
                                                        filter_data=filter_data, 
                                                        fiscalyear=fiscal_year, 
                                                        target_move=target_move,
                                                        all_accounts=all_accounts)
                           data.update({
                                         'initial_balance': initial_balance,
                                         'debit': debit,
                                         'credit': credit,
                                         'balance': balance,
                                         })
                        
                #For this case, search id account in dictionary results and update dictionary. 
                #Categories id can't be in dictionary result
                elif structure['display_detail'] == 'detail_with_hierarchy':
                    #list_ids have all the accounts.
                    #Call once this method with all accounts
                    
                    #In this case, res is a dictionary.
                    all_accounts = False
                    res = self.compute_data(cr, uid, result_dict, 
                                                        list_ids,
                                                        filter_type=filter_type, 
                                                        filter_data=filter_data, 
                                                        fiscalyear=fiscal_year, 
                                                        target_move=target_move,
                                                        all_accounts=all_accounts)
                    
                    for data in final_list:
                        if data['is_parent'] == False and data['id'] in res.keys():
                            data.update({
                                         'initial_balance': res[data['id']]['initial_balance'],
                                         'debit':  res[data['id']]['debit'],
                                         'credit':  res[data['id']]['credit'],
                                         'balance': res[data['id']]['balance'],
                                        })

        return final_list

    def get_data_accounts(self, cr, uid, filter_data, fiscal_year, filter_type,  target_move, chart_account_id, start_date, end_date, start_period_id, end_period_id, structure={}, final_list=[]):
        result_dict = {}
        final_data_parent = {'child_list': []} #Define empty list, avoid problem when list is empty and key isn't created
        final_data = {}
        list_ids = []
        child_list = []
        
        library_obj = self.pool.get('account.webkit.report.library')
        
        #1. Extract children. It's a list of dictionaries.
        child_list = structure['account_child']
        
        #no_detail: Iterate in the list and compute result in one line.
        if structure['display_detail'] == 'no_detail':
            final_data_parent['name'] = structure['name']
            final_data_parent['code'] = ''
            final_data_parent['id'] = structure['code'] 
            final_data_parent['is_parent'] = True
            final_data_parent['level'] = 0    
            final_data_parent['display_detail'] = 'no_detail'        
            
            #In accounts, iterate in parent, parent is 
            #accounts selected in list.
            for parent, child in child_list.iteritems():
                list_ids.append(parent.id)
                
            if len(list_ids) > 0:
                #Compute the balance, debit and credit for child ids list.         
                result_dict = library_obj.get_account_balance(cr, uid, 
                                                                list_ids, 
                                                                ['balance'],     
                                                                initial_balance=True,                                                                                   
                                                                fiscal_year_id=fiscal_year.id,                                                                                
                                                                state = target_move,
                                                                start_date= start_date,
                                                                end_date=end_date,
                                                                start_period_id = start_period_id,
                                                                end_period_id = end_period_id,
                                                                chart_account_id=chart_account_id.id,
                                                                filter_type=filter_type)
                
                
                #Compute all result in one line.
                #list_ids have all the accounts.
                all_accounts = True
                balance, debit, credit, initial_balance = self.compute_data(cr, uid, 
                                                            result_dict, 
                                                            list_ids, 
                                                            filter_type=filter_type, 
                                                            filter_data=filter_data, 
                                                            fiscalyear=fiscal_year, 
                                                            target_move=target_move,
                                                            all_accounts=all_accounts)
                
                final_data_parent.update({
                                             'initial_balance':initial_balance,
                                             'credit':credit,
                                             'debit':debit,
                                             'balance': balance,
                                            })
          
            else:
                final_data_parent.update({
                                             'initial_balance':0.0,
                                             'credit':0.0,
                                             'debit':0.0,
                                             'balance': 0.0,
                                            })
                
            #Update the dictionary with final results.
            final_list.append(copy(final_data_parent)) 
        
        else:            
            for parent, child in child_list.iteritems():
                final_data_parent['id'] = parent.id
                final_data_parent['name'] = parent.name
                final_data_parent['code'] = parent.code
                final_data_parent['is_parent'] = True #Distinct child from parent.
                final_data_parent['level'] = 0
                
                if child != []:
                    final_data_parent['child_list'] = child
                else:
                    final_data_parent['child_list'] = []
                
                final_data_parent['initial_balance'] = 0.0
                final_data_parent['debit'] = 0.0
                final_data_parent['credit'] = 0.0
                final_data_parent['balance'] = 0.0
                
                final_list.append(copy(final_data_parent)) 
                
                list_ids.append(parent.id)
                    
                #Build list of data child.
                if structure['display_detail'] == 'detail_with_hierarchy':
                    for c in child:
                        list_ids.append(c.id) #Add child.id
                        
                        if c.id != parent.id: #Avoid duplicate accounts.
                            final_data['id'] = c.id
                            final_data['level'] = c.level
#                            if 'child' in final_data:
#                               final_data['child'] = c.child
                            final_data['name'] = c.name
                            final_data['code'] = c.code
                            final_data['is_parent'] = False
                            
                            final_list.append(copy(final_data))

            if len(list_ids) > 0:
                #Compute the balance, debit and credit for child ids list.         
                result_dict = library_obj.get_account_balance(cr, uid, 
                                                                    list_ids, 
                                                                    ['balance', 'debit', 'credit'],     
                                                                    initial_balance=True,                                                                                   
                                                                    fiscal_year_id=fiscal_year.id,                                                                                
                                                                    state = target_move,
                                                                    start_date= start_date,
                                                                    end_date=end_date,
                                                                    start_period_id = start_period_id,
                                                                    end_period_id = end_period_id,
                                                                    chart_account_id=chart_account_id.id,
                                                                    filter_type=filter_type)
                
            #Iterate again the list for improve performance. Compute results.
            #In this case, accounts in list and child are in final_list, isn't necesary check wich type of display is.
            #Check only if id is in result_dict keys.
            
            #In this case, res is a dictionary.
            all_accounts = False
            res = self.compute_data(cr, uid, result_dict, 
                                                list_ids,
                                                filter_type=filter_type, 
                                                filter_data=filter_data, 
                                                fiscalyear=fiscal_year, 
                                                target_move=target_move,
                                                all_accounts=all_accounts)
            
            for data in final_list:
                if data['is_parent'] == False and data['id'] in res.keys():
                    data.update({
                                 'initial_balance': res[data['id']]['initial_balance'],
                                 'debit':  res[data['id']]['debit'],
                                 'credit':  res[data['id']]['credit'],
                                 'balance': res[data['id']]['balance'],
                                })

        return final_list
   
    '''
        Get a dictionary list, each dictionary have debit, credit, initial balance and balance for each account or
        for each group of type account.
        
        @param main_structure: account.financial.report choose in wizard, comes from the library in a dictionary.
        @param data: dictionary, contains all values selected in wizard
        @param final_list: list, return a list with all dictionaries.
    '''
        
    def get_total_result(self, cr, uid, main_structure, data, final_list=[]):
        
        filter_data = [] #contains the start and stop period or dates.
        
        fiscal_year = self.get_fiscalyear(data)
        
        #get the filters
        filter_type = self.get_filter(data)        
               
        target_move = self.get_target_move(data)
        
        #Get the accounts with the chart account selected.
        chart_account_id = self.get_chart_account_id(data)
        
        #############################Parameters depends of the type.        
        if filter_type == 'filter_period':
            #el método recibe los ids de los períodos (filtro por períodos)            
            start_period_id = self.get_start_period(data).id
            end_period_id = self.get_end_period(data).id
            
            #Build filter_data
            filter_data.append(self.get_start_period(data))
            filter_data.append(self.get_end_period(data))
            
            start_date = False
            end_date = False
            
            
        elif filter_type == 'filter_date':
            #el método recibe las fechas (en caso de filtro por fechas)
            start_date = self.get_date_from(data)
            end_date = self.get_date_to(data)
            
            #Build filter_data
            filter_data.append(start_date)
            filter_data.append(end_date)
            
            start_period_id = False
            end_period_id = False

        else:
            filter_type = ''
            
            start_period_id = False
            end_period_id = False
            start_date = False
            end_date = False
            
        #################################################################################
        
        '''
            In the dictionary (main_structure['account_type_child'] or main_structure['account_child'])
            the key is the account or type account and content is a list of child's account or 
            all the accounts that match with type account in the list.
        '''
            
        #The main account.financial.report (parent view) is always a dictionary.
        #If the instance is a dictionary and doesn't has a parent_id is the main structure
        #Child of main structure is a list.
        
        #Clean list, avoid problem that repeat structure (print twice)
        if final_list != []:
            final_list = []
        
        if isinstance(main_structure, list) == True:         
            #TODO: Implement account_report (Valor en informe)
            for structure in main_structure:
                if structure['type'] == 'account_type':
                    final_list = self.get_data_account_type(cr, uid, filter_data, fiscal_year, filter_type,  target_move, chart_account_id, start_date, end_date, start_period_id, end_period_id, structure, final_list)
                    
                elif structure['type'] == 'accounts':
                    final_list = self.get_data_accounts(cr, uid, filter_data, fiscal_year, filter_type,  target_move, chart_account_id, start_date, end_date, start_period_id, end_period_id, structure, final_list)

      
        #Call the method only with a dictionary list.         
        if type(main_structure) is types.DictType:
            self.get_total_result(cr, uid, main_structure['child'], data, final_list)
        
        return final_list              
    
    #Call all the methods that extract data, and build final dictionary with all the result.
    def get_data(self, data):
        
        #1. Extract the account_financial_report.
        account_financial_report = self.get_account_base_report(data)
        
        #2. Call method that extract the account_financial_report
        main_structure_obj = self.pool.get('account.financial.report')
        main_structure = main_structure_obj.get_structure_account_financial_report(self.cr, self.uid, account_financial_report.id)
        
        #3. Return a dictionary with all result. 
        final_data = self.get_total_result(self.cr, self.uid, main_structure,data)

        return  final_data
    

class report_partnerledger(osv.AbstractModel):
    _name = 'report.l10n_cr_account_trial_balance_report.report_trial_balance'
    _inherit = 'report.abstract_report'
    _template = 'l10n_cr_account_trial_balance_report.report_trial_balance'
    _wrapped_report_class = Parser


