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
"""
Parser for BCR format files
"""
import re
from datetime import datetime
from dateutil import parser
from pprint import PrettyPrinter
from copy import copy

class BCRParser( object ):
    """
    Para noviembre de 2012 se cambia el formato del archivo del BCR. Se cambia el encabezado del archivo
    así como el final del mismo. Además en la parte de abajo cambia el formato y visualización de los
    saldos finales. 
    
    El cambio más evidente es el formato de la cuenta de banco, pasa de 1-246447-0 a 001-0246447-0
    Revisión # 1                                                                         Revisión#2
    Encabezado anterior:                                                                 Encabezado nuevo
        BANCO DE COSTA RICA                                                              BANCO DE COSTA RICA
        Movimiento de Cuenta Corriente 1-246447-0 Colones (puede ser Dólares o Dolares)  MOVIMIENTO DE LA CUENTA  CORRIENTE No. 001-0246447-0  COLONES (DOLARES)
        Dueño: COMPA IA INMOBILIARIA CENTROA                                             DUENO: COMPA IA INMOBILIARIA CENTROAMERICANA CICCR S                            
        Movimiento realizado el periodo del 01-10-2012 al 31-10-2012                     MOVIMIENTO REALIZADO                           DEL 01-11-2012 AL 30-11-2012
    
    Final de archivo
    Revisión # 1                                                        Revisión #2
    TOTALES DEL MOVIMIENTO CONTABILIZADO                                TOTALES DEL MOVIMIENTO CONTABILIZADO 
          Cantidad  -------Monto--------                                CANTIDAD    -------MONTO-------- 
    Débitos       239       81,876,681.22                               DEBITOS       209        67,553,414.30                                                                                                                                
    Créditos       27       92,636,599.01                               CREDITOS        8        66,086,326.53

    Saldo Inicial            21,682,799.04                              -------- SALDOS --------                            
    Saldo Final              33,992,829.43                              INICIAL             33,992,829.43
                                                                        FINAL               32,525,741.66
    Solicitado el 01/11/2012 20:03:34                                   SOLICITADO EL 01-12-2012 A LAS 15:36:15:17                                       
    """
    def statement_record ( self, rec ):
        lines = []
        line_dict = {}

        line_dict = {
            'transref': 0.0, # _transmission_number
            'account_number': '', #_account_number
            'statementnr':'', # statement_number
            'startingbalance': 0.0, #_opening_balance
            'currencycode': 'CRC', #currencycode
            'endingbalance': 0.0, #_closing_balance
            'bookingdate': '', #moving_date
            'ammount': 0.0,
            'id': '',
        }

        cad = ''
        list_split = rec.split('\r\n')

        for l in list_split:
            
            # _transmission_number -> FIRST REVISION
            if (l.find('Movimiento realizado el periodo', 0, len('Movimiento realizado el periodo')) > -1):
                line_dict['statementnr'] = self.extract_number(l)
            # _transmission_number -> SECOND REVISION
            elif (l.find('MOVIMIENTO REALIZADO', 0, len('MOVIMIENTO REALIZADO')) > -1):
                line_dict['statementnr'] = self.extract_number(l)   
                           
            #_account_number -> FIRST REVISION
            if l.find('Movimiento de Cuenta Corriente', 0, len('Movimiento de Cuenta Corriente')) > -1:
                line_dict['account_number'] = self.extract_number(l)                
                if (l.find('D',0,len(l)) > -1):
                    line_dict['currencycode'] = 'USD'
                else:
                    line_dict['currencycode'] = 'CRC'
            #_account_number -> SECOND REVISION        
            elif (l.find('MOVIMIENTO DE LA CUENTA  CORRIENTE No.', 0, len('MOVIMIENTO DE LA CUENTA  CORRIENTE No.')) > -1):
                account_str = self.extract_number(l)   
                #001-0246447-0
                account_1 = account_str[2:3] #1
                account_2 = account_str[4:]  #246447-0
                account_complete = account_1+self.extract_number(account_2)#12464470
                line_dict['account_number'] = self.extract_number(account_complete)
                if (l.find('DOLARES',0,len(l)) > -1):
                    line_dict['currencycode'] = 'USD'
                else:
                    line_dict['currencycode'] = 'CRC'                      
             
            #FECHA Y HORA -> FIRST REVISION 
            if (l.find('Solicitado el', 0, len('Solicitado el'))  > -1):
                date =  hour = cad = ''
                date = self.extract_date_regular_expresion(l)
                if len(date) > 0:                   
                    hour = self.extract_hour_regular_expresion(l)
                cad = date + ' ' + hour                
                line_dict['transref'] = cad
                line_dict['bookingdate'] = cad
            #FECHA Y HORA -> SECOND REVISION 
            elif (l.find('SOLICITADO EL', 0, len('SOLICITADO EL'))  > -1):
                date =  hour = cad = ''
                date = self.extract_date_regular_expresion(l)
                if len(date) > 0:                   
                    hour = self.extract_hour_regular_expresion(l)
                cad = date + ' ' + hour                
                line_dict['transref'] = cad
                line_dict['bookingdate'] = cad        
                               
            #_opening_balance -> FIRST REVISION
            if l.find('Saldo Inicial', 0, len('Saldo Inicial'))  > -1:
                line_dict['startingbalance'] = self.extract_float(l)
            #_opening_balance -> SECOND REVISION   
            elif l.find('INICIAL', 0, len('INICIAL'))  > -1:
                line_dict['startingbalance'] = self.extract_float(l)
                    
            #_closing_balance -> FIRST REVISION
            if l.find('FINAL', 0, len('FINAL'))  > -1:
                line_dict['endingbalance'] = self.extract_float(l)
            #_closing_balance -> SECOND REVISION    
            elif l.find('Saldo Final', 0, len('Saldo Final'))  > -1:
                line_dict['endingbalance'] = self.extract_float(l)
                    
        line_dict['ammount'] = float( line_dict['startingbalance'] ) + float( line_dict['endingbalance'] )
        line_dict['id'] = line_dict['bookingdate'] + ' - ' + line_dict['account_number']
        self.line_dict = line_dict
      
        return line_dict
            
    def statement_lines ( self, rec ):
        parser = BCRParser()
        mapping = {
            'execution_date' : '',
            'effective_date' : '',
            'local_currency' : '',
            'transfer_type' : '',
            'reference' : '',
            'message' : '',
            'name' : '',
            'transferred_amount': '',
            'creditmarker': '',
        }
        
        lines = []
        line_dict = {}
        currencycode = ''
        
        list_split = rec.split('\r\n')
        entrada = False
        start = 0
        end = 0
        
        for l in list_split: 
            if l.find('TOTALES DEL MOVIMIENTO CONTABILIZADO', 0, len('TOTALES DEL MOVIMIENTO CONTABILIZADO')) <= -1:
                end += 1
            else:
                break                
        end = end - 1
        
        for l in list_split:           
            if l.find('-CONTABLE-', 0, len('-CONTABLE-')) <= -1:
                start += 1
            else:
                break
        start += 1 
        
        for l in list_split:           
            if l.find('Movimiento de Cuenta Corriente', 0, len('Movimiento de Cuenta Corriente')) > -1:
                if (l.find('D',0,len(l)) > -1):
                    currencycode = 'USD'
                else:
                    currencycode = 'CRC'
                break
            
            elif l.find('MOVIMIENTO DE LA CUENTA  CORRIENTE No.', 0, len('MOVIMIENTO DE LA CUENTA  CORRIENTE No.')) > -1:
                if (l.find('DOLARES',0,len(l)) > -1):
                    currencycode = 'USD'
                else:
                    currencycode = 'CRC'
                break
            
        sub_list = list_split [start:end]
        for sub in sub_list:
            #fecha_contable
            date_str = ''
            date_str = self.extract_date_regular_expresion_line(sub,0)
            date= datetime.strptime(date_str, "%d-%m-%y")               
            mapping['effective_date'] = date #fecha_contable.
            
            #fecha_movimiento
            date_str = self.extract_date_regular_expresion_line(sub,1)
            date = datetime.strptime(date_str, "%d-%m-%y")
            mapping['execution_date'] = date #fecha_movimiento                       
           
            mapping['local_currency'] = currencycode
            mapping['transfer_type'] = 'NTRF'
            mapping['reference'] = parser.extract_number(sub[18:26])
            mapping['message'] = sub[27:80]                
            mapping['name'] = sub[27:80]
            mapping['id'] = sub[27:80]
            
            amount = sub[106:]
            amount.replace('\t',' ')
            debit = amount[0:16]
            credit = amount[16:]
            
            if (parser.extract_float(debit) is not ''): #debit
                cad = parser.extract_float(debit)
                mapping['transferred_amount'] = -float(cad)      
                mapping['creditmarker'] = 'C'
                                      
            else: #credit
                cad = parser.extract_float (credit)
                mapping['transferred_amount'] =  float(cad)
            
            lines.append(copy(mapping))
                            
        return lines    
    
    def parse_stamenent_record( self, rec ):

        matchdict = dict()

        matchdict = self.statement_record( rec );

        # Remove members set to None
        matchdict = dict( [( k, v ) for k, v in matchdict.iteritems() if v] )

        matchkeys = set( matchdict.keys() )
        needstrip = set( [ 'transref', 'account_number', 'statementnr', 'currencycode', 'endingbalance', 'bookingdate'] )

        for field in matchkeys & needstrip:
            matchdict[field] = matchdict[field].strip()

        # Convert to float. Comma is decimal separator
        needsfloat = set( ["startingbalance", "endingbalance", "amount"] )
        for field in matchkeys & needsfloat:
            matchdict[field] = float( matchdict[field].replace( ',', '.' ) )

        # Convert date fields
        needdate = set( ["bookingdate"] )
                
        for field in matchkeys & needdate:            
            datestring = matchdict[field]
            date = self.extract_date_regular_expresion(datestring)
            hour = self.extract_hour_regular_expresion(datestring)
            
            date_complete = date + ' ' + hour
            try:
                #FORMAT DATE REVISION # 1
                date_obj= datetime.strptime(date_complete, "%d/%m/%Y %H:%M:%S")
            except:
                #FORMAT DATE REVISION # 2
                date_obj= datetime.strptime(date_complete, "%d-%m-%Y %H:%M:%S")
            matchdict[field] = date_obj
        
        return matchdict
                    
    def extract_number( self, account_number ):
        cad = ''
        result = re.findall(r'[0-9]+', account_number)
               
        for character in result:
            cad = cad + character
        return cad

    def extract_float ( self, ammount ):
        cad = ''
        result = re.findall(r"[-+]?\d*\.\d+|\d+",ammount)
        
        for character in result:
            cad = cad + character       
        return cad
    
    def extract_date_regular_expresion(self, date):
        cad = ''
        result = []
        date_string = ''
        #re.findall('[0-9]{1,2}-[0-9]{1,2}-[0-9]{4}',str)[0]+' '+re.findall('[0-9]{2}:[0-9]{2}:[0-9]{2}',str)[0]
        #FORMAT DATE FIRST REVISION
        result = re.findall('[0-9]{1,2}/[0-9]{1,2}/[0-9]{4}', date)
       
        if len(result) == 0:
            #FORMAT DATE SECOND REVISION
            result = re.findall('[0-9]{1,2}-[0-9]{1,2}-[0-9]{4}',date)      
        
        for character in result:
            cad = cad + character       
        return cad
    
    #con el parametro pos se dice cual de las dos fechas se debe traer
    #result trae una lista con dos elementos, el pos nos dice cual escoger
    def extract_date_regular_expresion_line(self, date, pos):
        cad = ''
        result = []
        date_string = ''
        #re.findall('[0-9]{1,2}-[0-9]{1,2}-[0-9]{4}',str)[0]+' '+re.findall('[0-9]{2}:[0-9]{2}:[0-9]{2}',str)[0]
        result = re.findall('([0-9]{2}-[0-9]{2}-[0-9]{2})[\s]*',date)      
        date_str = result[pos]
        
        for character in date_str:
            cad = cad + character       
        return cad
    
    def extract_hour_regular_expresion(self, date):
        cad = ''
        result = []

        result = re.findall('[0-9]{2}:[0-9]{2}:[0-9]{2}',date)             
        
        for character in result:
            cad = cad + character       
        return cad

    def extract_currency_code_USD(self, currency):
        cad = ''
        result = re.findall('[D.lares]',currency)
        for character in result:
            cad = cad + character
        return cad

    def parse( self, cr, data ):
        records = []
        # Some records are multiline
        for line in data:
            if len(line) <= 1:
                continue
            if line[0] == ':' and len(line) > 1:
                records.append(line)
            else:
                records[-1] = '\n'.join([records[-1], line])
                
        output = []

        for rec in records:
            output.append( self.parse_stamenent_record( rec ) )
                
        return output

def parse_file( filename ):
    bacfile = open( filename, "r" )
    p = BCRParser().parse( bacfile.readlines() )

def main():
    """The main function, currently just calls a dummy filename

    :returns: description
    """
    parse_file("testfile")

if __name__ == '__main__':
    main()

