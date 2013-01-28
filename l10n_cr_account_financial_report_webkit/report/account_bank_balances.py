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

from report import report_sxw
from tools.translate import _
import pooler
from datetime import datetime
import math 

from openerp.addons.account_financial_report_webkit.report.trial_balance import TrialBalanceWebkit
from openerp.addons.account_financial_report_webkit.report.webkit_parser_header_fix import HeaderFooterTextWebKitParser

def sign(number):
    return cmp(number, 0)

class account_bank_balances(TrialBalanceWebkit):

    def __init__(self, cursor, uid, name, context):
        super(account_bank_balances, self).__init__(cursor, uid, name, context=context)
        self.pool = pooler.get_pool(self.cr.dbname)
        self.cursor = self.cr   
        self.localcontext.update({
                'get_bank_accounts': self.get_bank_accounts, 
                'accounts_by_currency': self.accounts_by_currency,
                'get_move_lines_account': self.get_move_lines_account,
                'get_total_move_lines': self.get_total_move_lines,
        })

    #Change the filter by code == BKRE
    def get_bank_accounts(self, cr, uid):
        bank_accounts = []
        account_account_type_id = self.pool.get('account.account.type').search(cr, uid, [('code', '=' ,'BKRE')])[0]
        account_list_ids = self.pool.get('account.account').search(cr, uid, [('user_type.id','=',account_account_type_id)])
        account_list = self.pool.get('account.account').browse(cr, uid, account_list_ids)
        
        for account in account_list:
            bank_accounts.append(account)
            
        return bank_accounts

    #Create a dicctionary where each key is the currency and the value is a list with the accounts
    #Return a dictionary  
    """
        dic = {
                'USD': [1,2,3] -> is a object list
                'CR' : [5,6,7]
                } 
    """
    #If the currency don't exist, add as a new key for the dictionary.
    """
        In the mako, show the account like this.
            for currency, account in map.iteritems()
        Print first the currency and then, all accounts that have this currency.
    """
    def accounts_by_currency(self, cr, uid, accounts):
       account_dic = {}
       account_list = []
       
       for account in accounts:
           if account.report_currency_id.name in account_dic.keys():
               account_list =  account_dic[account.report_currency_id.name]
               account_list.append(account)
               account_dic[account.report_currency_id.name] = account_list
               account_list = []
           else:
               account_dic[account.report_currency_id.name] = [account]       
              
       return account_dic
   
    """
        Use the metod get_move_lines in the object account.webkit.report.library (account_webkit_report_library module)
    """   
    def get_move_lines_account(self, cr, uid, account_id, filter_type, filter_data, fiscalyear,target_move): 
        move_lines = []
        move_lines = self.pool.get('account.webkit.report.library').get_move_lines(cr, uid, account_ids=[account_id], filter_type=filter_type, filter_data=filter_data, fiscalyear=fiscalyear, target_move=target_move)
        
        return move_lines
    
    """Se pasa la moneda por parámetro desde el mako (viene del diccionario que separa las listas) """
    def get_total_move_lines(self, cr, uid, account_move_lines,currency):
        
        account_move_obj = self.pool.get('account.move')
        account_move_line_obj = self.pool.get('account.move.line')
        account_move_reconcile_obj = self.pool.get('account.move.reconcile')
        
        amount_transf = amount_check = amount_deposit = amount_debit = amount_credit = 0.0 
        
        total_result = {
                'amount_transf': 0.0,
                'amount_check': 0.0,
                'amount_deposit': 0.0,
                'amount_debit': 0.0,
                'amount_credit': 0.0,
                }
        
        amount_transf = amount_check = amount_deposit = amount_debit = amount_credit = amount_temp = 0.0
        move_line_reconcile = move_line_final = None
        
        #TODO Translate to english
        """
        Primero se obtiene de la linea (MLA) su respectivo account_move (M1). Luego se buscan todos los move_lines (MLA2) asociados al move_line.
        Se busca aquella que es diferente a MLA y se obtiene la MLA2. Con esta línea se busca la conciliación (MR) y se obtienen todas las líneas de
        conciliación. Con estas líneas se buscan aquella donde la diferencia de montos debe ser cero o la menor diferencia. Con esa línea se obtiene
        el move (M2) y de ahi se obtiene el journal para sumar los totales.
            
        """
        for line in account_move_lines:
            #account_move relacionado con la linea (campo de la relacion -> line_id)
            account_move_id = account_move_obj.search(cr, uid, [('line_id', '=', line.id )])
            #se buscan las demás lineas asociadas al move.
            account_move_lines_ids = account_move_line_obj.search (cr, uid, [('move_id', 'in', account_move_id)])            
            
            #si solo existe una -> se suma a los créditos / debitos (línea actual)
            if len(account_move_lines_ids) < 2:
                if line.amount_currency < 0: 
                    amount_credit += math.fabs(line.amount_currency)
                else:
                    amount_debit += line.amount_currency                
                continue
            
            #si existen dos -> se almacena el par de la actual.
            if len(account_move_lines_ids) == 2:
                account_move_lines = account_move_line_obj.browse (cr, uid, account_move_lines_ids)
                for move_line in account_move_lines:
                    if move_line.id != line.id:
                        move_line_reconcile  = move_line
            
            #si son más de dos se conserva la que tenga el monto mayor.
            if len(account_move_lines_ids) > 2:
                account_move_lines = account_move_line_obj.browse (cr, uid, account_move_lines_ids)
                for move_line in account_move_lines:
                    if currency == 'CRC':   
                        if line.debit != 0.0:
                            amount_line = line.debit
                        else:
                            amount_line = line.credit
                    else:
                        amount_line = math.fabs(line.amount_currency)
                                        
                    if amount_line > amount_temp:
                        amount_temp = amount_line 
                        move_line_reconcile  = move_line
            
            #si se encontro una línea de conciliación. 
            if move_line_reconcile:
                move_reconcile_id = account_move_reconcile_obj.search(cr, uid, [('id','=', move_line_reconcile.reconcile_id.id)])
                move_reconcile_lines_ids = account_move_line_obj.search(cr, uid, [('reconcile_id', 'in', move_reconcile_id)])
                
                #si la conciliación tiene líneas, si no tiene se suma a débitos y créditos. (de la línea de conciliación)
                if len(move_reconcile_lines_ids) > 0:                
                    #buscamos la linea que tenga la diferencia más pequeña es la que se queda. (se debe comparar con la que está conciliada ->
                    #account_move_line_reconcile (debit - credit)
                    #con esa linea es la que se busca el account_move y de ahi se saca el diario. Con el diario
                    #se suman los montos correspondientes.(transferencia, cheque, depósito, debitos y créditos)
                    move_line_reconcile_list = account_move_line_obj.browse(cr, uid, move_reconcile_lines_ids)
                   
                    #SE INICIALIZAN LAS VARIABLES CON LA LINEA YA ENCONTRADA DE CONCILIACION
                    #YA QUE SI NO SE ENCUENTRA NINGUNA SE UTILIZA LA LINEA DE CONCILIACION
                    diff = math.fabs(move_line_reconcile.debit - move_line_reconcile.credit)
                    move_line_final = move_line_reconcile
                    
                    for line_reconcile in move_line_reconcile_list:
                        amount_reconcile = diff - math.fabs(line_reconcile.debit - line_reconcile.credit)
                        if amount_reconcile > 0:
                            diff = amount_reconcile
                            move_line_final = line_reconcile
                    
                    #una vez que se encuentra la línea con la menor diferencia se busca el move al que pertenece la linea
                    account_move_final_id = account_move_obj.search(cr, uid, [('line_id','=', move_line_final.id)])
                    account_move_final = account_move_obj.browse(cr, uid, account_move_final_id)[0]
                    
                    #se buscan las opciones que tengan seleccionadas el diario. con eso se realiza la suma. 
                    #si no tiene ninguna, se suma a debitos 
                    if not account_move_final.journal_id.check is False \
                        and account_move_final.journal_id.transfers is False \
                            and account_move_final.journal_id.payment_method_customer is False \
                                and account_move_final.journal_id.payment_method_supplier is False \
                                    and account_move_final.journal_id.payment_verification is False:
                                        if currency == 'CRC':
                                            if line.debit != 0.0:
                                                amount_debit += line.debit
                                            else:
                                                amount_credit += line.credit
                                        else:
                                            if line.amount_currency < 0:
                                                amount_credit += math.fabs(amount_currency)
                                            else:
                                                amount_debit += amount_currency
                    
                    #si tienen marcado payment_method_customer -> deposito
                    if account_move_final.journal_id.payment_method_customer is True:
                        amount = 0.0
                        if currency == 'CRC':
                            if line.debit != 0.0:
                                amount = line.debit
                            else:
                                amount = line.credit
                            amount_deposit += amount
                            
                        else:
                            amount_deposit += math.fabs(line.amount_currency)
                            
                    #si tiene marcado payment_method_supplier -> transfers (transferencia) / check (cheque)
                    if account_move_final.journal_id.payment_method_supplier is True:
                        if account_move_final.journal_id.check is True:
                             amount = 0.0
                             if currency == 'CRC':
                                if line.debit != 0.0:
                                    amount = line.debit
                                else:
                                    amount = line.credit
                             amount_check += amount
                             
                        if account_move_final.journal_id.transfers is True:
                           amount = 0.0
                           if currency == 'CRC':
                               if line.debit != 0.0:
                                   amount = line.debit
                               else:
                                   amount = line.credit
                           amount_transf += amount
                        
                        if  account_move_final.journal_id.check is False and  account_move_final.journal_id.transfers is False:
                             if currency == 'CRC':
                                 if line.debit != 0.0:
                                     amount_debit += line.debit
                                 else:
                                     amount_credit += line.credit
                             else:
                                 if line.amount_currency < 0:
                                     amount_credit += math.fabs(amount_currency)
                                 else:
                                     amount_debit += amount_currency                    
                    
                else:                    
                    if move_line_reconcile.debit != 0.0:
                        amount_debit += move_line_reconcile.debit
                    else:
                        amount_credit += move_line_reconcile.credit
     
        total_result ['amount_transf'] = amount_transf
        total_result ['amount_check'] = amount_check
        total_result ['amount_deposit'] = amount_deposit
        total_result ['amount_debit']= amount_debit
        total_result ['amount_credit'] = amount_credit
        
        return total_result                    

HeaderFooterTextWebKitParser(
    'report.l10n_cr_account_financial_report_webkit.account.account_report_account_bank_balances_webkit',
    'account.account',
    'addons/l10n_cr_account_financial_report_webkit/report/account_bank_balances.mako',
    parser=account_bank_balances)
    

