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
import types
from openerp import pooler
from openerp.report import report_sxw
from openerp.tools.translate import _
from copy import copy
from openerp.osv import fields, orm, osv

from openerp.addons.account_report_lib.account_report_base import accountReportbase

class Parser(accountReportbase):
    
    def __init__(self, cr, uid, name, context):
        super(Parser, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'cr': cr,
            'uid':uid,
            'get_data': self.get_data,
            'formatLang':self.formatLang, #Give format to numbers and percentages
        })
    
    '''
        If the display_detail == display_flat, compute all the balance, debit, credit and initial_balance and return 
        one result for each type account selected in the list.
    '''
    def compute_balances(self, cr, uid, result_dict, child_list):
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
    def get_data_account_type(self, cr, uid, period, target_move, opening_period, fiscal_year, filter_type, structure={}, final_list=[]):
        
        result_dict_period_balance = {}
        result_dict_fiscal_year_balance = {}
        final_data = {}
        final_data_parent = {}
        list_ids = []
        child_list = []
        
        library_obj = self.pool.get('account.webkit.report.library') 
        
        #1. Extract children. It's a list of dictionaries.
        child_list = structure['account_type_child']
        
        #no_detail: Iterate in the list and compute result in one line.
        if structure['display_detail'] == 'no_detail':
            final_data_parent['name'] = structure['name']
            final_data_parent['code'] = ''
            final_data_parent['level'] = 0
            
            #In account type, iterate in child, because child is all accounts that
            #match with account types selected.
            for parent, child in child_list.iteritems():
                #Add child id to compute data
                for c in child:
                    list_ids.append(c.id)
                
            if len(list_ids) > 0:
                #Compute the balance for child ids list.         
                result_dict_period_balance = library_obj.get_account_balance(cr, uid, 
                                                                             list_ids, 
                                                                             ['balance'], 
                                                                             fiscal_year_id=fiscal_year.id,
                                                                             state = target_move,
                                                                             end_period_id=period.id, 
                                                                             filter_type=filter_type)
                
                result_dict_fiscal_year_balance = library_obj.get_account_balance(cr, uid, 
                                                                                  list_ids, 
                                                                                  ['balance'], 
                                                                                  fiscal_year_id=fiscal_year.id,
                                                                                  state = target_move,
                                                                                  start_period_id=opening_period.id, 
                                                                                  end_period_id=opening_period.id,
                                                                                  filter_type=filter_type)
                total_period = 0.0
                total_fiscal_year = 0.0
                total_variation = 0.0
                                      
                #Compute all result in one line.                  
                #for parent, child in child_list.iteritems():                
                total_period += self.compute_balances(cr, uid, result_dict_period_balance, list_ids)
                total_fiscal_year += self.compute_balances(cr, uid, result_dict_fiscal_year_balance, list_ids)
                total_variation += total_period - total_fiscal_year
            
                final_data_parent.update({
                                         'total_fiscal_year': total_fiscal_year,
                                         'total_period': total_period,
                                         'total_variation': total_variation,
                                         'total_percent_variation': total_fiscal_year != 0 and (100 * total_variation / total_fiscal_year) or 0,
                                        })
                    
            else:
                final_data_parent.update({
                                             'total_fiscal_year': 0.0,
                                             'total_period': 0.0,
                                             'total_variation': 0.0,
                                             'total_percent_variation': 0.0,
                                            })
                
            #Update the dictionary with final results.
            final_list.append(copy(final_data_parent))
            
        else:  
            if child_list:
                #2. Create dictionaries for parent and children.
                for parent, child in child_list.iteritems():
                   final_data_parent['id'] = parent.id
                   final_data_parent['name'] = parent.name
                   final_data_parent['code'] = parent.code
                   final_data_parent['is_parent'] = True #Distinct child from parent.
                   final_data_parent['level'] = 0
                   
                   #child_list is use to compute final results and save child and the relation with parent.
                   if child != []:
                        final_data_parent['child_list'] = child
                   else:
                        final_data_parent['child_list'] = []

                   #3. For parent account_types when display_detail = detail_with_hierarchy, don't compute the balance, debit, credit and initial_balance. 
                   if structure['display_detail'] == 'detail_flat':
                        #Update keys to numbers, because this keys now show results
                        final_data_parent['total_fiscal_year'] = 0.0
                        final_data_parent['total_period'] = 0.0
                        final_data_parent['total_variation'] = 0.0
                        final_data_parent['total_percent_variation'] = 0.0
                        
                        #Add parent
                        final_list.append(copy(final_data_parent))
                        
                        #Add child id to compute data
                        for c in child:
                            list_ids.append(c.id)
                  
                   elif structure['display_detail'] == 'detail_with_hierarchy':
                        final_data_parent['total_fiscal_year'] = ''
                        final_data_parent['total_period'] = ''
                        final_data_parent['total_variation'] = ''
                        final_data_parent['total_percent_variation'] = ''
                        
                        #Add parent
                        final_list.append(copy(final_data_parent))
                        
                        #Add child in final list and id to compute data.
                        for c in child:
                            list_ids.append(c.id)
                            
                            final_data['id'] = c.id
                            final_data['level'] = c.level
                            final_data['name'] = c.name
                            final_data['code'] = c.code
                            final_data['is_parent'] = False
                            
                            final_list.append(copy(final_data)) 
                    
                if len(list_ids) > 0:
                    #Compute the balance, debit and credit for child ids list.         
                    result_dict_period_balance = library_obj.get_account_balance(cr, 
                                                                                 uid, 
                                                                                 list_ids, 
                                                                                 ['balance'], 
                                                                                 fiscal_year_id=fiscal_year.id,
                                                                                 state = target_move,
                                                                                 end_period_id=period.id, 
                                                                                 filter_type=filter_type)
                    
                    result_dict_fiscal_year_balance = library_obj.get_account_balance(cr,
                                                                                      uid,
                                                                                      list_ids,
                                                                                      ['balance'],
                                                                                      fiscal_year_id=fiscal_year.id,
                                                                                      state = target_move,
                                                                                      start_period_id=opening_period.id,
                                                                                      end_period_id=opening_period.id,
                                                                                      filter_type=filter_type)
                                        
                    if structure['display_detail'] == 'detail_flat':
                        #Compute all the results
                        for data in final_list:
                            if 'child_list' in data.keys():
                                total_period = self.compute_balances(cr, uid, result_dict_period_balance, data['child_list'])
                                total_fiscal_year = self.compute_balances(cr, uid, result_dict_fiscal_year_balance, data['child_list'])
                                total_variation = total_period - total_fiscal_year
                                      
                                data.update({
                                             'total_fiscal_year': total_fiscal_year,
                                             'total_period': total_period,
                                             'total_variation': total_variation,
                                             'total_percent_variation': total_fiscal_year != 0 and (100 * total_variation / total_fiscal_year) or 0,
                                            })
                            
                    elif structure['display_detail'] == 'detail_with_hierarchy':
                        for data in final_list:
                            #Only for child, compute this values
                            if data['is_parent'] == False:
                                 #Search the result with the account id in the result dictionary
                                 if 'id' in data.keys():
                                     if data['id'] in result_dict_period_balance.keys() and \
                                         data['id'] in result_dict_fiscal_year_balance.keys():
                                         #Search the result with the account id in the result dictionary
                                         total_period = result_dict_period_balance[data['id']]['balance']
                                         total_fiscal_year = result_dict_fiscal_year_balance[data['id']]['balance']
                                         total_variation = total_period - total_fiscal_year
                                         
                                         data.update({
                                                      'total_fiscal_year': total_fiscal_year,
                                                      'total_period': total_period,
                                                      'total_variation': total_variation,
                                                      'total_percent_variation': total_fiscal_year != 0 and (100 * total_variation / total_fiscal_year) or 0,
                                            })

               
        return final_list

    def get_data_accounts(self, cr, uid, period, target_move, opening_period, fiscal_year, filter_type, structure={}, final_list=[]):
        
        result_dict_period_balance = {}
        result_dict_fiscal_year_balance = {}
        final_data = {}
        final_data_parent = {}
        list_ids = []
        child_list = []
        
        library_obj = self.pool.get('account.webkit.report.library')
        
        #1. Extract children. It's a list of dictionaries.
        child_list = structure['account_child']
        
        #no_detail: Iterate in the list and compute result in one line.
        if structure['display_detail'] == 'no_detail':
            final_data_parent['name'] = structure['name']
            final_data_parent['code'] = ''
            final_data_parent['is_parent'] = True
            final_data_parent['level'] = 0
            
            #In accounts, iterate in parent, parent is 
            #accounts selected in list.
            for parent, child in child_list.iteritems():
                list_ids.append(parent.id)
                
            if len(list_ids) > 0:
                #Compute the balance for child ids list.         
                result_dict_period_balance = library_obj.get_account_balance(cr,
                                                                             uid,
                                                                             list_ids,
                                                                             ['balance'],
                                                                             fiscal_year_id=fiscal_year.id,
                                                                             state = target_move,
                                                                             end_period_id=period.id,
                                                                             filter_type=filter_type)

                result_dict_fiscal_year_balance = library_obj.get_account_balance(cr, 
                                                                                  uid, 
                                                                                  list_ids, 
                                                                                  ['balance'], 
                                                                                  fiscal_year_id=fiscal_year.id,
                                                                                  state = target_move,
                                                                                  start_period_id=opening_period.id, 
                                                                                  end_period_id=opening_period.id,
                                                                                  filter_type=filter_type)
                
                total_period = 0.0
                total_fiscal_year = 0.0
                total_variation = 0.0
                
                #Compute all result in one line.
                total_period += self.compute_balances(cr, uid, result_dict_period_balance,list_ids)
                total_fiscal_year += self.compute_balances(cr, uid, result_dict_fiscal_year_balance,list_ids)
                total_variation += total_period - total_fiscal_year
            
                final_data_parent.update({
                                         'total_fiscal_year': total_fiscal_year,
                                         'total_period': total_period,
                                         'total_variation': total_variation,
                                         'total_percent_variation': total_fiscal_year != 0 and (100 * total_variation / total_fiscal_year) or 0,
                                        })
                    
            else:
                final_data_parent.update({
                                             'total_fiscal_year': 0.0,
                                             'total_period': 0.0,
                                             'total_variation': 0.0,
                                             'total_percent_variation': 0.0,
                                            })
                
            #Update the dictionary with final results.
            final_list.append(copy(final_data_parent)) 
    
        else:            
            for parent, child in child_list.iteritems():
                #Create a dictionary with parent info 
                final_data_parent['id'] = parent.id
                final_data_parent['name'] = parent.name
                final_data_parent['code'] = parent.code
                final_data_parent['is_parent'] = True #Distinct child from parent.
                final_data_parent['level'] = 0
                
                final_data_parent['total_fiscal_year'] = 0.0
                final_data_parent['total_period'] = 0.0
                final_data_parent['total_variation'] = 0.0
                final_data_parent['total_percent_variation'] = 0.0
                
                #Show and compute data of account selected
                final_list.append(copy(final_data_parent))
                    
                #Add parents ids, parents are accounts in main list
                list_ids.append(parent.id)
                               
                if structure['display_detail'] == 'detail_with_hierarchy':
                    for c in child:
                        if c.id not in list_ids: #Avoid duplicate ids
                            list_ids.append(c.id)
                            
                            final_data['id'] = c.id
                            final_data['level'] = c.level
                            final_data['name'] = c.name
                            final_data['code'] = c.code
    
                            final_list.append(copy(final_data)) 
                                    
            if len(list_ids) > 0:
                #Compute the balance, debit and credit for child ids list. 
                result_dict_period_balance = library_obj.get_account_balance(cr, uid, 
                                                                             list_ids, 
                                                                             ['balance'], 
                                                                             fiscal_year_id=fiscal_year.id,
                                                                             state = target_move,
                                                                             end_period_id=period.id, 
                                                                             filter_type=filter_type)

                result_dict_fiscal_year_balance = library_obj.get_account_balance(cr, uid, 
                                                                                  list_ids, 
                                                                                  ['balance'], 
                                                                                  fiscal_year_id=fiscal_year.id,
                                                                                  state = target_move,
                                                                                  start_period_id=opening_period.id, 
                                                                                  end_period_id=opening_period.id,
                                                                                  filter_type=filter_type)
               
                #Get data for accounts selected in list.
                if structure['display_detail'] == 'detail_flat':
                    for final_data_parent in final_list:
                        total_period = result_dict_period_balance[parent.id]['balance']
                        total_fiscal_year = result_dict_fiscal_year_balance[parent.id]['balance']
                        total_variation = total_period - total_fiscal_year
                        
                        final_data_parent.update({
                                     'total_period':total_period,
                                     'total_fiscal_year':total_fiscal_year,
                                     'total_variation':total_variation,
                                     'total_percent_variation': total_fiscal_year != 0 and (100 * total_variation / total_fiscal_year) or 0,
                                    })                                        
            
                elif structure['display_detail'] == 'detail_with_hierarchy':  
                    for data in final_list:            
                        #Search the result with the account id in the result dictionary
                        if 'id' in data.keys():
                            if data['id'] in result_dict_period_balance.keys() and \
                                data['id'] in result_dict_fiscal_year_balance.keys():
                                
                                #Search the result with the account id in the result dictionary
                                total_period = result_dict_period_balance[data['id']]['balance']
                                total_fiscal_year = result_dict_fiscal_year_balance[data['id']]['balance']
                                total_variation = total_period - total_fiscal_year
                                 
                                data.update({
                                              'total_fiscal_year': total_fiscal_year,
                                              'total_period': total_period,
                                              'total_variation': total_variation,
                                              'total_percent_variation': total_fiscal_year != 0 and (100 * total_variation / total_fiscal_year) or 0,
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
        
        account_period_obj = self.pool.get('account.period')
        library_obj = self.pool.get('account.webkit.report.library')
        
        #************ Parameters
        period = self.get_start_period(data)
        fiscal_year = self.get_fiscalyear(data)
        opening_period = account_period_obj.get_opening_period(cr, uid, period)
        filter_type = self.get_filter(data)
        target_move = self.get_target_move(data)
        #****************
        
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
                    final_list += self.get_data_account_type(cr, uid, period, target_move, opening_period, fiscal_year, filter_type, structure, list_data)
                    
                elif structure['type'] == 'accounts':
                    list_data = [] #Avoid repeat accounts when an account is in list and it's a child for account type selected.                
                    final_list += self.get_data_accounts(cr, uid, period, target_move, opening_period, fiscal_year, filter_type, structure, list_data)

      
        #Call the method only with a dictionary list.         
        if type(main_structure) is types.DictType:
            self.get_total_result(cr, uid, main_structure['child'], data, final_list)
        
        return final_list
        
    def get_data(self, data):
         #1. Extract the account_financial_report.
        account_financial_report = self.get_account_base_report(data)
        
        #2. Call method that extract the account_financial_report
        main_structure = self.pool.get('account.financial.report').get_structure_account_financial_report(self.cr, self.uid, account_financial_report.id)
        
        #3. Return a dictionary with all result. 
        final_data = self.get_total_result(self.cr, self.uid, main_structure,data)
        
        return final_data
    
class report_partnerledger(osv.AbstractModel):
    _name = 'report.l10n_cr_account_situation_balance_report.report_situation_balance'
    _inherit = 'report.abstract_report'
    _template = 'l10n_cr_account_situation_balance_report.report_situation_balance'
    _wrapped_report_class = Parser
