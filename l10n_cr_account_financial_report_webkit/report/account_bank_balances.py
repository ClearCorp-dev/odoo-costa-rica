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
        
        company = self.pool.get('res.users').browse(self.cr, uid, uid, context=context).company_id
        header_report_name = ' - '.join((_('Account Bank Balance'), company.name, company.currency_id.name))
        
        self.localcontext.update({
                'report_name': _('Account Bank Balance'),
                'get_bank_accounts': self.get_bank_accounts, 
                'accounts_by_currency': self.accounts_by_currency,
                'get_move_lines_account': self.get_move_lines_account,
                'get_total_move_lines': self.get_total_move_lines,
                'get_initia_balance_accounts': self.get_initia_balance_accounts,
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
    
        """
        @param account: Es la cuenta a la cual pertenenecen las lineas
        @param account_move_lines: Son los move_lines que pertenecen a la cuenta 
    """
    def get_total_move_lines(self, cr, uid, account_move_lines, account):
        
        """
        #TODO Translate to english
         
        Primero se obtiene de la linea (MLA1) su respectivo account_move (MA). Luego se buscan todos los move_lines (MLA2) asociados al move_line.
        Se busca aquella que es diferente a MLA y se obtiene la MLA2. Con esta línea se busca la conciliación (MR) y se obtienen todas las líneas de
        conciliación. Con estas líneas se buscan aquella donde la diferencia de montos debe ser cero o la menor diferencia. Con esa línea se obtiene
        el move (M2) y de ahi se obtiene el journal para sumar los totales.
            
        """
        amount_transf = amount_check = amount_deposit = amount_debit = amount_credit =  0.0
        
        """
        #LA MONEDA DE LA COMPAÑIA COINCIDA CON LA MONEDA DE LA CUENTA QUE VIENE POR PARÁMETRO -> Si son iguales (Son colones, moneda de la compañía)
        """
        foreign_currency = not account.company_id.currency_id.id == account.report_currency_id.id

        for line in account_move_lines:
            temp_line = temp_line2 = None
            no_journal = False
                           
            #account_move relacionado con la linea (campo de la relacion -> move_id)
            move =  line.move_id
            #se buscan las demás lineas asociadas al move (move_id -> line_id)
            move_lines = move.line_id
            
            #si solo existe una -> move_line_final es la línea actual
            if len(move_lines) < 2:
                no_journal = True
            
            #si existen dos -> se almacena el par de la actual.
            elif len(move_lines) == 2:
                for move_line in move_lines:
                    if move_line.id != line.id:
                        temp_line = move_line
            
            #si son más de dos se conserva la que tenga el monto mayor.
            else:
                #Si son dólares se suma el amount_currency
                if foreign_currency:
                    amount_temp = math.fabs(line.amount_currency)
                #si son colones -> se suman los débitos y créditos (uno de los dos es 0)
                else:
                    amount_temp = math.fabs(line.debit + line.credit)
                
                #se reccorren todas las líneas que no sean iguales a la línea
                temp_line = line
                for move_line in move_lines:                    
                    if not move_line.id == line.id:
                        #si son dolares -> se saca el valor absoluto del amount_currency y se compara con amount_temp
                        if foreign_currency:
                            #Se debe hacer la comparación con los valores contrarios, si el amount_currency de la linea
                            #original es positivo, se busca su contrario.
                            if (line.amount_currency > 0 and move_line.amount_currency < 0) or (line.amount_currency < 0 and move_line.amount_currency > 0):
                                if math.fabs(line.amount_currency + move_line.amount_currency) <= amount_temp:
                                    temp_line = move_line
                                    amount_temp = math.fabs(move_line.amount_currency + line.amount_currency)
                        else:
                            #si son colones -> se saca el valor absoluto de la diferencia entre los debitos y los créditos de ambas lines
                            #debe ser menor al amount_temp
                            #Se debe buscar su contrario, positivos con negativos. La búsqueda no se hace con todos los valores.
                            if (line.debit > 0 and move_line.credit > 0) or (line.credit > 0 and move_line.debit > 0): 
                                if math.fabs((move_line.debit + move_line.credit) - (line.debit + line.credit)) <= amount_temp:
                                    temp_line = move_line
                                    amount_temp = math.fabs((move_line.debit + move_line.credit) - (line.debit + line.credit))
            """
            Debe cumplir ciertas condiciones para seguir el proceso. 
                1- Debe existir el temp_line, es decir debe ser la misma línea, su línea espejo o bien la línea que cumpla el valor más aproximado
                2- El temp_line (linea espejo) no puede ser la misma que la línea original
                3- La línea espejo debe tener conciliación
            """                    
            
            if not temp_line:
                no_journal = True
            elif temp_line.id == line.id:
                no_journal = True
            elif not temp_line.reconcile_id:
                no_journal = True
            
            """
                Si se cumplieron las condiciones anteriores entonces se puede buscar la conciliación y las líneas de conciliación correspondientes
                temp_line corresponde a la línea espejo de la línea original (line)
            """
            if not no_journal:
                #extraemos la conciliacion y las líneas de conciliación 
                reconcile = temp_line.reconcile_id
                move_lines = reconcile.line_id
                
                #si la conciliación no tiene líneas no se puede continuar el proceso.
                if len(move_lines) < 2:
                    no_journal = True
                
                #si existen sólo dos líneas de conciliación, se busca la que es diferente. 
                elif len(move_lines) == 2:
                    temp_line2 = temp_line
                    for move_line in move_lines:
                        if move_line.id != temp_line2.id:
                            temp_line = move_line
                
                else:
                    if foreign_currency:
                        amount_temp = math.fabs(temp_line.amount_currency)
                    else:
                        amount_temp = math.fabs(temp_line.debit - temp_line.credit)
                    
                    temp_line2 = temp_line
                    for move_line in move_lines:
                        if not move_line.id == temp_line2.id:
                            if foreign_currency:
                                #las comparaciones deben hacerse con el monto opuesto (positivo con negativo)
                                if (temp_line2.amount_currency > 0 and move_line.amount_currency < 0) or (temp_line2.amount_currency < 0 and move_line.amount_currency > 0):
                                    if math.fabs(move_line.amount_currency + temp_line2.amount_currency) <= amount_temp:
                                        temp_line = move_line
                                        amount_temp = math.fabs(move_line.amount_currency + temp_line2.amount_currency)
                            else:
                                #las comparaciones se deben hacer con los montos opuestos, (debit - credit)
                                if (temp_line2.debit > 0 and move_line.credit > 0) or (temp_line2.credit > 0 and move_line.debit > 0):        
                                    if math.fabs((move_line.debit + move_line.credit) - (temp_line2.debit + temp_line2.credit)) <= amount_temp:
                                        temp_line = move_line
                                        amount_temp = math.fabs((move_line.debit + move_line.credit) - (temp_line2.debit + temp_line2.credit))
                    
                    if temp_line2.id == temp_line.id:
                        temp_line = None                    
                                        
                if not temp_line or not temp_line.move_id or not temp_line.move_id.journal_id:
                    no_journal = True
                
                else:
                    #temp_line debe ser la línea de conciliación que más se acerca a la línea de conciliación
                    #con los valores del journal, se obtienen los cálculos
                    journal = temp_line.move_id.journal_id
                    
                    if journal.payment_method_customer:
                        if foreign_currency:
                            amount_deposit += line.amount_currency
                        else:
                            amount_deposit += line.debit - line.credit
                    
                    elif journal.payment_method_supplier:
                        if journal.transfers:
                            if foreign_currency:
                                amount_transf += line.amount_currency
                            else:
                                amount_transf += line.debit - line.credit
                        
                        elif journal.check:
                            if foreign_currency:
                                amount_check += line.amount_currency
                            else:
                                amount_check += line.debit - line.credit
                        else:
                            no_journal = True
                    else:
                        no_journal = True
            
            #si no cumple ninguna de las condiciones anteriores, se suman los resultados a débitos y créditos. 
            if no_journal:
                if foreign_currency:
                    if line.amount_currency > 0:
                        amount_debit += line.amount_currency
                    else:
                        amount_credit += line.amount_currency
                else:
                    amount_debit += line.debit
                    amount_credit += -1 * line.credit
     
        return {
            'amount_transf' : amount_transf,
            'amount_check' : amount_check,
            'amount_deposit' : amount_deposit,
            'amount_debit' : amount_debit,
            'amount_credit' : amount_credit,
        }
    
    """
        @param accounts: cuentas para calcular el balance inicial
        @param filter_type: tipo de filtro (filter_date, filter_period)
        @param filter_dat: valores seleccionados en el wizard para generar el reporte
        @param target_move : posted, all (tipo de apunte)    
    """
    def get_initia_balance_accounts (self, cr, uid, accounts, filter_type, filter_data, fiscalyear, target_move,chart_account_id,context={}):
        accounts_ids = []
       
        #todas las cuentas ya vienen agrupadas por moneda.
        for account in accounts:
            accounts_ids.append(account.id)
        
        #si la moneda no es colones, se pide el foreign_balance. si son colones se pide el balance.
        account_foreign_currency = accounts[0]  
        foreign_currency = not account_foreign_currency.company_id.currency_id.id == account_foreign_currency.report_currency_id.id
        if foreign_currency:
            field_names = ['foreign_balance']
        else:
            field_names = ['balance']
        
        #el metodo get_account_balance devuelve un diccionario con la llave de la cuenta
        #y el valor que se le está pidiendo, en este caso el balance inicial.        
        if filter_type == 'filter_period':
            #el método recibe los ids de los períodos (filtro por períodos)
            if filter_data[0]:
                start_period_id = filter_data[0].id
            else:
                start_period_id = False
                
            end_period_id = filter_data[1].id
            initial_balance = self.pool.get('account.webkit.report.library').get_account_balance(cr,
                                                                                        uid, 
                                                                                        accounts_ids, 
                                                                                        field_names,     
                                                                                        initial_balance=True,                                                                                   
                                                                                        fiscal_year_id=fiscalyear.id,                                                                                
                                                                                        state = target_move,
                                                                                        start_period_id = start_period_id,
                                                                                        end_period_id = end_period_id,
                                                                                        chart_account_id=chart_account_id,
                                                                                        filter_type=filter_type)
        if filter_type == 'filter_date':
            #el método recibe las fechas (en caso de filtro por fechas)
            start_date = filter_data[0]
            end_date = filter_data[1]
            initial_balance = self.pool.get('account.webkit.report.library').get_account_balance(cr, 
                                                                                        uid, 
                                                                                        accounts_ids, 
                                                                                        field_names,  
                                                                                        initial_balance=True, 
                                                                                        fiscal_year_id=fiscalyear.id,
                                                                                        state = target_move, 
                                                                                        start_date = start_date,                                                                      
                                                                                        end_date = end_date,                                                                                        
                                                                                        chart_account_id=chart_account_id,
                                                                                        filter_type=filter_type)
        if filter_type == '':
            initial_balance = self.pool.get('account.webkit.report.library').get_account_balance(cr, 
                                                                                        uid, 
                                                                                        accounts_ids, 
                                                                                        field_names,  
                                                                                        initial_balance=True, 
                                                                                        fiscal_year_id=fiscalyear.id,
                                                                                        state = target_move, 
                                                                                        chart_account_id=chart_account_id,
                                                                                        filter_type=filter_type)
        
        #CASO ESPECIAL PARA ESTE TIPO DE REPORTE -> FILTRO DE SOLAMENTE PERIODO DE APERTURA                                                                                        
        if filter_type == 'filter_opening':
            period_ids = [self.pool.get('account.period').search(cr, uid, [('fiscalyear_id','=',fiscal_year_id),('special','=',True)],order='date_start asc')[0]]
            
            initial_balance = self.pool.get('account.webkit.report.library').get_account_balance(cr, 
                                                                                        uid, 
                                                                                        accounts_ids, 
                                                                                        field_names,  
                                                                                        initial_balance=True, 
                                                                                        fiscal_year_id=fiscalyear.id,
                                                                                        state = target_move, 
                                                                                        period_ids = period_ids,
                                                                                        chart_account_id=chart_account_id,
                                                                                        filter_type=filter_type)
        
        
        return initial_balance

HeaderFooterTextWebKitParser(
    'report.l10n_cr_account_financial_report_webkit.account.account_report_account_bank_balances_webkit',
    'account.account',
    'addons/l10n_cr_account_financial_report_webkit/report/account_bank_balances.mako',
    parser=account_bank_balances)
    

