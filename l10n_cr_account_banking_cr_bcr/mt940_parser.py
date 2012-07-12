#!/usr/bin/env python
# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2011 credativ Ltd (<http://www.credativ.co.uk>).
#    All Rights Reserved
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
Parser for BAC CR MT940 format files
Based on fi_patu's parser
"""
import re
from datetime import datetime
from dateutil import parser
import pprint
from copy import copy

class BCRParser( object ):

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
        }

        #file = open( filename, 'r' )
        #line = file.readline()
        
        list_split = rec.split('\r\n')

        for l in list_split:
            # _transmission_number
            if l.find('Movimiento realizado el periodo', 0, len('Movimiento realizado el periodo')) > -1:
                line_dict['statementnr'] = self.extract_number(l)
            #_account_number
            if l.find('Movimiento de Cuenta Corriente', 0, len('Movimiento de Cuenta Corriente')) > -1:
                line_dict['account_number'] = self.extract_number(l)
            # _transmission_number
            if l.find('Solicitado el', 0, len('Solicitado el'))  > -1 :
                line_dict['transref'] = self.extract_number(l)
                line_dict['bookingdate'] = self.extract_number(l)               
            #_opening_balance
            if l.find('Saldo Inicial', 0, len('Saldo Inicial'))  > -1:
                line_dict['startingbalance'] = self.extract_float(l)
            #_closing_balance
            if l.find('Saldo Final', 0, len('Saldo Final'))  > -1:
                line_dict['endingbalance'] = self.extract_float(l)
        
        amount_statement = float( line_dict['startingbalance'] ) + float( line_dict['endingbalance'] )
        line_dict['ammount'] = amount_statement

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
            'id': '',
        }
        
        lines = []
        line_dict = {}
        
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
            
        sub_list = list_split [start:end]
        for sub in sub_list:
            #03-05-12
            day = sub[0:2]
            month = sub[3:5]            
            date_n = datetime.now()                        
            try:
                date = datetime(int(date_n.year), int(month), int (day))
            except Exception:
                day = sub[1]
                month = sub[4]
                date_n = datetime.now()
                date = datetime(int(date_n.year), int(month), int (day))
                
            mapping['execution_date'] = date                        
            mapping['effective_date'] = date
            mapping['local_currency'] = 'CRC'
            mapping['transfer_type'] = 'NTRF'
            mapping['reference'] = parser.extract_number(sub[17:36])
            mapping['message'] = sub[26:80]                
            mapping['name'] = sub[26:80]
            mapping['id'] = sub[26:80]
            
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
            try:
                day = datestring[0:2]
                month = datestring[2:4]
                year = datestring[4:8]
                hour = datestring[8:10]
                minute = datestring[10:12]
                second = datestring[12:14]
            except Exception:
                day = datestring[2]
                month = datestring[4]
                year = datestring[4:8]
                hour = datestring[8:10]
                minute = datestring[10:12]
                second = datestring[12:14]          
                       
            date = datetime(int(year),int(month),int(day),int(hour),int(minute),int(second))
            matchdict[field] = date
        
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

