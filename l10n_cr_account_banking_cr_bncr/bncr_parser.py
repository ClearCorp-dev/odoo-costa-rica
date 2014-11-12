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
Parser for Davivienda format files
"""
import re
from datetime import datetime
from dateutil import parser
from pprint import PrettyPrinter
from copy import copy

class BNCRParser( object ):
    
    #Define the header for the extract to import.
    '''
     ** Kwargs parameter is used for a dynamic list of parameters. 
        The wizard imported extracts used in all parsers and not all parsers have all the necessary information in your file, 
        so get information from the wizard and passed by the ** kwargs. 
        Then in the parses that are needed, are extracted from the ** kwargs and if needed, 
        the parser still works the same way without this parameter.
        
        The rest of the methods must receive this parameter. (As the method that parse the header and the lines). 
        
        If you need a new parameter, you specify its name and value, using the ** kwargs is a dictionary, 
        extract its value, with the respective key
    '''
    def statement_record ( self, rec, **kwargs):
        lines = []
        line_dict = {}
        startingbalance = 0.0

        line_dict = {
            'transref': '', # _transmission_number
            'account_number': '', #_account_number
            'statementnr':'', # statement_number
            'startingbalance': 0.0, #_opening_balance
            'currencycode': '', #currencycode
            'endingbalance': 0.0, #_closing_balance
            'bookingdate': '', #moving_date
            'ammount': 0.0,
            'id': '',
        }
        #Split the file in statements
        list_split = rec.split('\n')        
       
        #currency_code (local_currency in the stament) extracted 
        #from account_number object from the wizard.
        #account_number (local_account) extracted from account_number
        #object from the wizard. date_to_str and date_from_str are
        #the dates in wizard, both are strings
        
        line_dict['account_number'] = kwargs['account_number']
        
        line_dict['currencycode'] = kwargs['local_currency']
        
        line_dict['statementnr'] = kwargs['date_from_str'] + ' - '+ \
        kwargs['date_to_str'] + ' Extracto BNCR ' + \
        line_dict['account_number'] #Interval time of the file.
        
        #transmission_number (Date when done the import)
        date_obj= datetime.now()
        line_dict['transref'] = date_obj.strftime("%d-%m-%Y %H:%M:%S")
        #bookingdate
        line_dict['bookingdate'] = date_obj.strftime("%d-%m-%Y %H:%M:%S")
        
        '''
            For the BNCR parser, the ending_balance comes from wizard. With
            total of debit and credit and the ending_balance
            compute the initial_balance.
        '''
        #extract the total of debit and credit from the file.
        #The last statements and compute the startingbalance
        last_position = (len(list_split) - 1)
        last_line = list_split[last_position] 
        #last line can be blanck, find the last line with data.
        if last_line == "":
            while True:
                last_position -= 1
                last_line = list_split[last_position]
                if last_line is not "":
                    break       
        
        last_line_split = last_line.split(';')
        
        #For another type of format, take the character \t
        if len(last_line_split) > 1:        
            final_line_totals =  last_line_split        
        else:
            final_line_totals = last_line.split('\t')
        
        #######################################################
        
        if final_line_totals[3] != '':
            debit = float(final_line_totals[3].replace(",",""))
        else:
            debit = 0.0
        if final_line_totals[4] != '':
            credit = float(final_line_totals[4].replace(",",""))
        else:
            credit = 0.0        
        
        startingbalance = float(kwargs['ending_balance']) + debit - credit 
        line_dict['startingbalance'] =  str(startingbalance)
        
        #the ending_balance extracted from **kwargs (comes from wizard)
        endingbalance = float(kwargs['ending_balance'])
        line_dict['endingbalance'] =  str(kwargs['ending_balance'])
        
        line_dict['ammount'] = startingbalance + endingbalance
        line_dict['id'] = kwargs['date_from_str'] + ' - '+ \
        kwargs['date_to_str'] + ' Extracto BNCR ' + \
        line_dict['account_number']
        
        return line_dict
        
    '''
    Parse all the lines in the file. Once the header is parser, the next step are the lines.
    '''     
    def statement_lines ( self, rec ):
        parser = BNCRParser()
        mapping = {
            'execution_date' : '',
            'effective_date' : '',
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
        
        list_split = rec.split('\n')
        entrada = False
            
        start = 1
        end = (len(list_split) - 1)
        last_line = list_split[end]
        #last line can be blanck, find the last line with data.
        if last_line == "":
            while True:
                end -= 1
                last_line = list_split[end]
                if last_line is not "":
                    break
                    
        sub_list = list_split [start:end] #The end line is amount totals of credit and debit
        for sub in sub_list:
            line = sub.split(';')
            if len(line) > 1:
                final_line = line
            #For another type of format, take the character \t
            else:
                final_line = sub.split('\t')
                
            #effective_date
            date_str = final_line[1].replace("/","-")
            date= datetime.strptime(date_str, "%Y-%m-%d")               
            mapping['effective_date'] = date #fecha_contable.                        
            #execution_date
            mapping['execution_date'] = date #fecha_movimiento
                                   
            mapping['transfer_type'] = 'NTRF'
            mapping['reference'] = final_line[2] #NumDocumento
            mapping['message'] = final_line[2]+' '+final_line[5] #NumDocumento + Description         
            mapping['name'] = final_line[2]+' '+final_line[5] #NumDocumento + Description       
            mapping['id'] = final_line[2]+' '+final_line[5] #NumDocumento + Description     
            
            #the field in position 3 is debit, the position 4 is credit
            if final_line[4] != '':
                credit = float(final_line[4].replace(",",""))
                mapping['transferred_amount'] = credit    
                mapping['creditmarker'] = 'C'
            
            elif final_line[3] != '':
                #In this case, the debit is negative.
                debit = float(final_line[3].replace(",",""))
                mapping['transferred_amount'] =  -1 * debit
           
            lines.append(copy(mapping))
                            
        return lines    
     
    """
    ** Kwargs parameter is used for a dynamic list of parameters. 
        The wizard imported extracts used in all parsers and not 
        all parsers have all the necessary information in your file, 
        so get information from the wizard and passed by the ** kwargs. 
        Then in the parses that are needed, are extracted from the ** kwargs and if needed, 
        the parser still works the same way without this parameter.
        
        The rest of the methods must receive this parameter. (As the method 
        that parse the header and the lines). 
        
        If you need a new parameter, you specify its name and value,
        using the ** kwargs is a dictionary, 
        extract its value, with the respective key
    """
    def parse_stamenent_record( self, rec, **kwargs):

        matchdict = dict()
        
        #Set the header for the stament.
        matchdict = self.statement_record(rec, **kwargs);

        # Remove members set to None
        matchdict = dict( [( k, v ) for k, v in matchdict.iteritems() if v] )

        matchkeys = set( matchdict.keys() )
        needstrip = set( [ 'transref', 'account_number', 'statementnr',
                          'currencycode', 'endingbalance', 'bookingdate'] )

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
            date_obj= datetime.strptime(datestring, "%d-%m-%Y %H:%M:%S")
            matchdict[field] = date_obj
        
        return matchdict
        
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
            #parse_stament_record call the method that
            #parse the header and the stament of the file.
            output.append(self.parse_stamenent_record( rec ))
                
        return output

def parse_file( filename ):
    bncrfile = open( filename, "r" )
    p = BNCRParser().parse( bncrfile.readlines() )


def main():
    """The main function, currently just calls a dummy filename

    :returns: description
    """
    parse_file("testfile")

if __name__ == '__main__':
    main()

