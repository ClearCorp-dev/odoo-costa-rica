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

from copy import copy
from openerp.osv import fields, osv, orm
from openerp.tools.translate import _
import types
from openerp import pooler

from openerp.addons.account_report_lib.account_report_base import accountReportbase #Library Base

class Parser(accountReportbase):
    
    def __init__(self, cr, uid, name, context):
        super(Parser, self).__init__(cr, uid, name, context=context)
        
        self.localcontext.update({
            'cr': cr,
            'uid': uid,
            'get_last_period': self.get_last_period,
            'get_base_account_compare': self.get_base_account_compare,
            'get_data': self.get_data,
        })
        
  #Get base account to compare result
    def get_base_account_compare(self, data):
        return self._get_info(data, 'base_compare_account', 'account.account')
             
    #Get last period based in period selected. 
    def get_last_period(self, data):
        start_period = self.get_start_period(data)
        return self.pool.get('account.period').get_last_period(self.cr,self.uid,start_period)
   
    '''
        If the display_detail == display_flat, compute all the balance, debit, credit and initial_balance and return 
        one result for each type account selected in the list.
        @param child_list: Can be a list of ids (int) or a browse record list.
    '''
    
    def compute_data(self, cr, uid, result_dict, child_list):
        balance = 0.0 
         
        #Child list can be a list of int or browse_record list
        for c in child_list:
            if isinstance(c, orm.browse_record):
                if c.id in result_dict.keys():
                    balance += result_dict[c.id]['balance']
        
            elif isinstance(c, int):
                if c in result_dict.keys():
                    balance += result_dict[c]['balance']

        return balance
    
    """ 
        Main methods to compute data. Split account.financial.report types in different
        methods to improve usabillity and maintenance. 
    """
    #Method for account.financial.report account_type type. 
    def get_data_account_type(self, cr, uid, base_account, target_move, fiscal_year, filter_type, period, last_period, structure={}, final_list=[]):
        
        result_dict = {}
        final_data_parent = {'child_list': []} #Define empty list, avoid problem when list is empty and key isn't created
        final_data = {}
        list_ids = []
        child_list = []
        
        library_obj = self.pool.get('account.webkit.report.library') 
        
        #1. Extract children. It's a list of dictionaries.
        child_list = structure['account_type_child']       
        
          #Extract base_account selected and add id into list_ids to compute data.
        base_account_id = base_account[0].id
        list_ids.append(base_account_id)
        
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
                for c in child:                   
                    list_ids.append(c.id)
                
            if len(list_ids) > 0:                    
                    #In this report, call method three times, calculate balance for                    
                    #    period selected
                    #    last period
                    #    fiscal year
                    
                    #Period selected -> Change witch period take as start_period and end_period
                    result_dict_period = library_obj.get_account_balance(cr, uid, 
                                                                            list_ids, 
                                                                            ['balance'],   
                                                                            fiscal_year_id=fiscal_year.id,                                                                                
                                                                            state = target_move,  
                                                                            start_period_id=period.id, 
                                                                            end_period_id=period.id,
                                                                            filter_type=filter_type)
                    
                    #Last period
                    result_dict_last_period = library_obj.get_account_balance(cr, uid, 
                                                                            list_ids, 
                                                                            ['balance'],     
                                                                            fiscal_year_id=fiscal_year.id,                                                                                
                                                                            state = target_move,
                                                                            start_period_id=last_period.id, 
                                                                            end_period_id=last_period.id,
                                                                            filter_type=filter_type)
                    
                    #Fiscal year
                    result_dict_fiscal_year = library_obj.get_account_balance(cr, uid, 
                                                                            list_ids, 
                                                                            ['balance'],     
                                                                            state = target_move,
                                                                            end_period_id=period.id, 
                                                                            fiscal_year_id=fiscal_year.id, 
                                                                            filter_type=filter_type)
                                      
                    ##Extract results for base_account selected in wizard.
                    base_account_last_period = result_dict_last_period[base_account_id]['balance']
                    base_account_period = result_dict_period[base_account_id]['balance']
                    base_account_total_variation = base_account_period - base_account_last_period
                    base_account_fiscal_year = result_dict_fiscal_year[base_account_id]['balance']                    
                    base_account_percentage_period = 100
                    base_account_percentage_last_period = 100
                    base_account_percentage_variation = base_account_last_period != 0 and (100 * base_account_total_variation / base_account_last_period) or 0
                    base_account_percentage_fiscalyear = 100 
                    
                    balance_period = 0.0
                    balance_last_period = 0.0
                    balance_fiscal_year = 0.0
                    balance_total_variation = 0.0                
                    
                    #Get results for all groups that belongs to account_type.
                    balance_period += self.compute_data(cr, uid, result_dict_period, list_ids)
                    balance_last_period += self.compute_data(cr, uid, result_dict_last_period, list_ids)
                    balance_fiscal_year += self.compute_data(cr, uid, result_dict_fiscal_year, list_ids)
                    balance_total_variation += balance_period - balance_last_period
                    
                    #Update dictionary
                    final_data_parent.update({
                                             'balance_total_period': balance_period,
                                             'balance_total_last_period': balance_last_period,
                                             'balance_total_variation': balance_period - balance_last_period,
                                             'balance_total_fiscal_year':base_account_fiscal_year,
                                             'balance_total_percentage_last_period': base_account_last_period != 0 and (100 * balance_last_period / base_account_last_period) or 0,
                                             'balance_total_percentage_period': base_account_period != 0 and (100 * balance_period / base_account_period) or 0,
                                             'balance_total_percentage_variation': balance_last_period != 0 and (100 * balance_total_variation / balance_last_period) or 0,
                                             'balance_total_percentage_fiscal_year': base_account_fiscal_year != 0 and (100 * balance_fiscal_year / base_account_fiscal_year) or 0,
                                            })
                
                    #Update the dictionary with final results.
                    final_list.append(copy(final_data_parent))
                       
            else:
                final_data_parent.update({
                                             'balance_total_period': 0.0,
                                             'balance_total_last_period': 0.0,
                                             'balance_total_variation': 0.0,
                                             'balance_total_fiscal_year':0.0,
                                             'balance_total_percentage_period': 0.0,
                                             'balance_total_percentage_last_period': 0.0,
                                             'balance_total_percentage_variation': 0.0,
                                             'balance_total_percentage_fiscal_year': 0.0,
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
                   final_data_parent['level'] = 0
                   
                   #child_list is use to compute final results and save child and the relation with parent.
                   if child != []:
                        final_data_parent['child_list'] = child
                   else:
                        final_data_parent['child_list'] = []
 
                   if structure['display_detail'] == 'detail_flat':
                        final_data_parent['is_parent'] = False #Distinct child from parent.
                        #Update keys to numbers, because this keys now show results
                        final_data_parent['balance_total_period'] = 0.0
                        final_data_parent['balance_total_last_period'] = 0.0
                        final_data_parent['balance_total_variation'] = 0.0
                        final_data_parent['balance_total_fiscal_year'] = 0.0
                        final_data_parent['balance_total_percentage_period'] = 0.0,
                        final_data_parent['balance_total_percentage_last_period'] = 0.0
                        final_data_parent['balance_total_percentage_variation'] = 0.0
                        final_data_parent['balance_total_percentage_fiscal_year'] = 0.0                        
                        
                        #Add parent into list
                        final_list.append(copy(final_data_parent))
                        
                   elif structure['display_detail'] == 'detail_with_hierarchy':
                        final_data_parent['is_parent'] = True #Distinct child from parent.
                        final_data_parent['balance_total_period'] = ''
                        final_data_parent['balance_total_last_period'] = ''
                        final_data_parent['balance_total_variation'] = ''
                        final_data_parent['balance_total_fiscal_year'] = ''
                        final_data_parent['balance_total_percentage_period'] = ''
                        final_data_parent['balance_total_percentage_last_period'] = ''
                        final_data_parent['balance_total_percentage_variation'] = ''
                        final_data_parent['balance_total_percentage_fiscal_year'] = ''
                        
                        #Add parent into list
                        final_list.append(copy(final_data_parent))
                                   
                        #Build child in a dictionary
                        if 'child_list' in final_data_parent.keys():   
                           for c in final_data_parent['child_list']:                                                        
                               final_data['id'] = c.id
                               final_data['level'] = c.level
                               final_data['name'] = c.name
                               final_data['code'] = c.code
                               final_data['is_parent'] = False
                               
                               final_list.append(copy(final_data))                           
                  
                   #Add child in final list and id to compute data.
                   for c in child:
                       list_ids.append(c.id)
                
                if len(list_ids) > 0: 
                      #Compute the balance for child ids list.         
                      #Period selected -> Change witch period take as start_period and end_period
                      result_dict_period = library_obj.get_account_balance(cr, uid, 
                                                                            list_ids, 
                                                                            ['balance'],     
                                                                            fiscal_year_id=fiscal_year.id,                                                                                
                                                                            state = target_move,
                                                                            start_period_id=period.id, 
                                                                            end_period_id=period.id,
                                                                            filter_type=filter_type)
                    
                      #Last period
                      result_dict_last_period = library_obj.get_account_balance(cr, uid, 
                                                                            list_ids, 
                                                                            ['balance'],   
                                                                            fiscal_year_id=fiscal_year.id,                                                                                
                                                                            state = target_move,  
                                                                            start_period_id=last_period.id, 
                                                                            end_period_id=last_period.id,
                                                                            filter_type=filter_type)
                    
                      #Fiscal year
                      result_dict_fiscal_year = library_obj.get_account_balance(cr, uid, 
                                                                            list_ids, 
                                                                            ['balance'],   
                                                                            fiscal_year_id=fiscal_year.id,                                                                                
                                                                            state = target_move,  
                                                                            end_period_id=period.id, 
                                                                            filter_type=filter_type)
                      
                
                ##Extract results for base_account selected in wizard.
                base_account_last_period = result_dict_last_period[base_account_id]['balance']
                base_account_period = result_dict_period[base_account_id]['balance']
                base_account_total_variation = base_account_period - base_account_last_period
                base_account_fiscal_year = result_dict_fiscal_year[base_account_id]['balance']                    
                base_account_percentage_period = 100
                base_account_percentage_last_period = 100
                base_account_percentage_variation = base_account_last_period != 0 and (100 * base_account_total_variation / base_account_last_period) or 0
                base_account_percentage_fiscalyear = 100
                
                #Iterate again the list for improve performance. Compute results.
                if structure['display_detail'] == 'detail_flat':
                    #final_list has categories and child of this categories
                    #Compute results for each category 
                    for data in final_list:          
                        if 'child_list' in data.keys():
                            #Balance for all accounts (compare with base_account_selected)
                            balance_period = self.compute_data(cr, uid, result_dict_period, data['child_list'])
                            balance_last_period = self.compute_data(cr, uid, result_dict_last_period, data['child_list'])
                            balance_fiscal_year = self.compute_data(cr, uid, result_dict_fiscal_year, data['child_list'])
                            balance_total_variation = balance_period - balance_last_period

                            #Update dictionary
                            data.update({
                                         'balance_total_period': balance_period,
                                         'balance_total_last_period': balance_last_period,
                                         'balance_total_variation': balance_total_variation,
                                         'balance_total_fiscal_year':balance_fiscal_year,
                                         'balance_total_percentage_period': base_account_period != 0 and (100 * balance_period / base_account_period) or 0,
                                         'balance_total_percentage_last_period': base_account_last_period != 0 and (100 * balance_last_period / base_account_last_period) or 0,
                                         'balance_total_percentage_variation': balance_last_period != 0 and (100 * balance_total_variation / balance_last_period) or 0,
                                         'balance_total_percentage_fiscal_year': base_account_fiscal_year != 0 and (100 * balance_fiscal_year / base_account_fiscal_year) or 0,
                                        })
                
                #For this case, search id account in dictionary results and update dictionary. 
                #Categories id can't be in dictionary result
                elif structure['display_detail'] == 'detail_with_hierarchy':
                    for data in final_list:
                        if 'id' in data.keys():
                            if data['is_parent'] == False and \
                                (data['id'] in result_dict_period.keys() and data['id'] in result_dict_last_period.keys() and data['id'] in result_dict_fiscal_year.keys()):
                                
                                balance_total_period = result_dict_period[data['id']]['balance']
                                balance_total_last_period = result_dict_last_period[data['id']]['balance']
                                balance_fiscal_year = result_dict_fiscal_year[data['id']]['balance']
                                balance_total_variation = balance_total_period - balance_total_last_period
                                
                                data.update({
                                             'balance_total_period': balance_total_period,
                                             'balance_total_last_period': balance_total_last_period,
                                             'balance_total_fiscal_year': balance_fiscal_year,
                                             'balance_total_variation': balance_total_variation,
                                             'balance_total_percentage_period': base_account_period != 0 and (100 * balance_total_period / base_account_period) or 0,
                                             'balance_total_percentage_last_period': base_account_last_period != 0 and (100 * balance_total_last_period / base_account_last_period) or 0,
                                             'balance_total_percentage_variation': balance_total_last_period != 0 and (100 * balance_total_variation / balance_total_last_period) or 0,
                                             'balance_total_percentage_fiscal_year': base_account_fiscal_year != 0 and (100 * balance_fiscal_year / base_account_fiscal_year) or 0,
                                                                  
                                             })

        return final_list
    
    def get_data_accounts(self, cr, uid, base_account, target_move, fiscal_year, filter_type, period, last_period, structure={}, final_list=[]):
        result_dict = {}
        final_data_parent = {'child_list': []} #Define empty list, avoid problem when list is empty and key isn't created
        final_data = {}
        list_ids = []
        child_list = []
        
        library_obj = self.pool.get('account.webkit.report.library')
        
        #1. Extract children. It's a list of dictionaries.
        child_list = structure['account_child']
        
        #Extract base_account selected and add id into list_ids to compute data.
        base_account_id = base_account[0].id
        list_ids.append(base_account_id)
        
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
            
            #For accounts append parents, no childs.         
            for parent, child in child_list.iteritems():
                list_ids.append(parent.id)
                
            if len(list_ids) > 0:
                #In this report, call method three times, calculate balance for                    
                #    period selected
                #    last period
                #    fiscal year
                
                #Period selected -> Change witch period take as start_period and end_period
                result_dict_period = library_obj.get_account_balance(cr, uid, 
                                                                        list_ids, 
                                                                        ['balance'],     
                                                                        fiscal_year_id=fiscal_year.id,                                                                                
                                                                        state = target_move,
                                                                        start_period_id=period.id, 
                                                                        end_period_id=period.id,
                                                                        filter_type=filter_type)
                
                #Last period
                result_dict_last_period = library_obj.get_account_balance(cr, uid, 
                                                                        list_ids, 
                                                                        ['balance'],     
                                                                        fiscal_year_id=fiscal_year.id,                                                                                
                                                                        state = target_move,
                                                                        start_period_id=last_period.id, 
                                                                        end_period_id=last_period.id,
                                                                        filter_type=filter_type)
                
                #Fiscal year
                result_dict_fiscal_year = library_obj.get_account_balance(cr, uid, 
                                                                        list_ids, 
                                                                        ['balance'], 
                                                                        fiscal_year_id=fiscal_year.id,                                                                                
                                                                        state = target_move,    
                                                                        end_period_id=period.id, 
                                                                        filter_type=filter_type)
                
                ##Extract results for base_account selected in wizard.
                base_account_last_period = result_dict_last_period[base_account_id]['balance']
                base_account_period = result_dict_period[base_account_id]['balance']
                base_account_total_variation = base_account_period - base_account_last_period
                base_account_fiscal_year = result_dict_fiscal_year[base_account_id]['balance']                    
                base_account_percentage_period = 100
                base_account_percentage_last_period = 100
                base_account_percentage_variation = base_account_last_period != 0 and (100 * base_account_total_variation / base_account_last_period) or 0
                base_account_percentage_fiscalyear = 100 
                
                balance_period = 0.0
                balance_last_period = 0.0
                balance_fiscal_year = 0.0
                balance_total_variation = 0.0
                
                for parent, child in child_list.iteritems():   
                    balance_period += result_dict_period[parent.id]['balance']
                    balance_last_period += result_dict_last_period[parent.id]['balance']
                    balance_fiscal_year += result_dict_fiscal_year[parent.id]['balance']
                    balance_total_variation += balance_period - balance_last_period
                    
                    #Update dictionary
                    final_data_parent.update({
                                         'balance_total_last_period': balance_last_period,   
                                         'balance_total_percentage_last_period': base_account_last_period != 0 and (100 * (balance_last_period / base_account_last_period)) or 0,                                                                                      
                                         'balance_total_period': balance_period,
                                         'balance_total_percentage_period': base_account_period != 0 and (100 * balance_period / base_account_period) or 0,                                             
                                         'balance_total_variation': balance_period - balance_last_period,
                                         'balance_total_fiscal_year':balance_fiscal_year,         
                                         'balance_total_percentage_variation': balance_last_period != 0 and (100 * (balance_total_variation / balance_last_period)) or 0,
                                         'balance_total_percentage_fiscal_year': base_account_fiscal_year != 0 and (100 * balance_fiscal_year / base_account_fiscal_year) or 0,
                                        })
                    
                #Update the dictionary with final results.
                final_list.append(copy(final_data_parent))
                       
            else:
                final_data_parent.update({
                                             'balance_total_period': 0.0,
                                             'balance_total_last_period': 0.0,
                                             'balance_total_variation': 0.0,
                                             'balance_total_fiscal_year':0.0,
                                             'balance_total_percentage_period': 0.0,
                                             'balance_total_percentage_last_period': 0.0,
                                             'balance_total_percentage_variation': 0.0,
                                             'balance_total_percentage_fiscal_year': 0.0,
                                            })
      
                #Update the dictionary with final results.
                final_list.append(copy(final_data_parent))  
                
        else:   
            '''
                Optimization process: Call get_account_balance the least possible.
            '''      
            if child_list:   
                for parent, child in child_list.iteritems():
                    final_data_parent['id'] = parent.id
                    final_data_parent['name'] = parent.name
                    final_data_parent['code'] = parent.code
                    final_data_parent['is_parent'] = False #In Both case, parents show numerics results
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
                    
                    #For detail_flat, append parent.id, that is id for account selected in list.
                    if structure['display_detail'] == 'detail_flat':
                        list_ids.append(parent.id)
                        
                    #Build list of data child.
                    if structure['display_detail'] == 'detail_with_hierarchy':
                        for c in child:
                            list_ids.append(c.id) #Add child.id
                            parent_type = type(parent)
                            c_type = type(c)
                            
                            if c.name != parent.name: #Avoid duplicate accounts.
                                final_data['id'] = c.id
                                final_data['level'] = c.level
                                final_data['name'] = c.name
                                final_data['code'] = c.code
                                final_data['is_parent'] = False
                                
                                final_list.append(copy(final_data))
                        
                        #if parent.id don't exist in list, add it
                        if parent.id not in list_ids:
                            #Add parent.id 
                            list_ids.append(parent.id)
                            
                if len(list_ids) > 0:
                    #In this report, call method three times, calculate balance for                    
                    #    period selected
                    #    last period
                    #    fiscal year
                    
                    #Period selected -> Change witch period take as start_period and end_period
                    result_dict_period = library_obj.get_account_balance(cr, uid, 
                                                                            list_ids, 
                                                                            ['balance'],     
                                                                            fiscal_year_id=fiscal_year.id,
                                                                            state = target_move,
                                                                            start_period_id=period.id, 
                                                                            end_period_id=period.id,
                                                                            filter_type=filter_type)
                    
                    #Last period
                    result_dict_last_period = library_obj.get_account_balance(cr, uid, 
                                                                            list_ids, 
                                                                            ['balance'],    
                                                                            fiscal_year_id=fiscal_year.id,
                                                                            state = target_move, 
                                                                            start_period_id=last_period.id, 
                                                                            end_period_id=last_period.id,
                                                                            filter_type=filter_type)
                    
                    #Fiscal year
                    result_dict_fiscal_year = library_obj.get_account_balance(cr, uid, 
                                                                            list_ids, 
                                                                            ['balance'],
                                                                            fiscal_year_id=fiscal_year.id,
                                                                            state = target_move,
                                                                            end_period_id=period.id, 
                                                                            filter_type=filter_type)
                
                ##Extract results for base_account selected in wizard.
                base_account_last_period = result_dict_last_period[base_account_id]['balance']
                base_account_period = result_dict_period[base_account_id]['balance']
                base_account_total_variation = base_account_period - base_account_last_period
                base_account_fiscal_year = result_dict_fiscal_year[base_account_id]['balance']
                base_account_percentage_period = 100
                base_account_percentage_last_period = 100
                base_account_percentage_variation = base_account_last_period != 0 and (100 * base_account_total_variation / base_account_last_period) or 0
                base_account_percentage_fiscalyear = 100
                    
                #Iterate again the list for improve performance. Compute results.
                #In this case, accounts in list and child are in final_list, isn't necessary check wich type of display is.
                #Check only if id is in result_dict keys.
                for data in final_list:
                    if 'id' in data.keys():
                        if (data['id'] in result_dict_period.keys() and data['id'] in result_dict_last_period.keys() \
                              and data['id'] in result_dict_fiscal_year.keys()):
                        
                            balance_total_period = result_dict_period[data['id']]['balance']
                            balance_total_last_period = result_dict_last_period[data['id']]['balance']
                            balance_fiscal_year = result_dict_fiscal_year[data['id']]['balance']
                            balance_total_variation = balance_total_period - balance_total_last_period
                            
                            data.update({
                                         'balance_total_period': balance_total_period,
                                         'balance_total_last_period': balance_total_last_period,
                                         'balance_total_fiscal_year': balance_fiscal_year,
                                         'balance_total_variation': balance_total_variation,
                                         'balance_total_percentage_period': base_account_period != 0 and (100 * balance_total_period / base_account_period) or 0,
                                         'balance_total_percentage_last_period': base_account_last_period != 0 and (100 * balance_total_last_period / base_account_last_period) or 0,
                                         'balance_total_percentage_variation': balance_total_last_period != 0 and (100 * balance_total_variation / balance_total_last_period) or 0,
                                         'balance_total_percentage_fiscal_year': base_account_fiscal_year != 0 and (100 * balance_fiscal_year / base_account_fiscal_year) or 0,
                                          
                                         })

        return final_list    

    def get_total_result(self, cr, uid, main_structure, data, final_list=[]):
        
        account_period_obj = self.pool.get('account.period')
        
        period = self.get_start_period(data)
        last_period = account_period_obj.get_last_period(cr, uid, period)
        fiscal_year = self.get_fiscalyear(data)
        filter_type = self.get_filter(data)
        target_move = self.get_target_move(data)
        
        #Get base_account to compare
        base_account = self.get_base_account_compare(data)
        
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
                    list_data = [] #Avoid repeat accounts when an account is in list and it's a child for account type selected.
                    final_list += self.get_data_account_type(cr, uid, base_account, target_move, fiscal_year, filter_type, period, last_period, structure, list_data)
                    
                elif structure['type'] == 'accounts':
                    list_data = [] #Avoid repeat accounts when an account is in list and it's a child for account type selected.
                    final_list += self.get_data_accounts(cr, uid, base_account, target_move, fiscal_year, filter_type,  period, last_period, structure, list_data)
      
        #Call the method only with a dictionary list.         
        if type(main_structure) is types.DictType:
            self.get_total_result(cr, uid, main_structure['child'], data, final_list)

        return final_list
    
    #Call all the methods that extract data, and build final dictionary with all the result.
    def get_data(self, data):
        
        #1. Extract the account_financial_report.
        account_financial_report = self.get_account_base_report(data)
        
        #2. Call method that extract the account_financial_report
        main_structure = self.pool.get('account.financial.report').get_structure_account_financial_report(self.cr, self.uid, account_financial_report.id)
        
        #3. Return a dictionary with all result. 
        final_data = self.get_total_result(self.cr, self.uid, main_structure,data)

        return  final_data

class report_partnerledger(osv.AbstractModel):
    _name = 'report.l10n_cr_account_profit_statement_report.report_profit_statement'
    _inherit = 'report.abstract_report'
    _template = 'l10n_cr_account_profit_statement_report.report_profit_statement'
    _wrapped_report_class = Parser
