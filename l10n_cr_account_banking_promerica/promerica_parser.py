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

import re
from datetime import datetime
from dateutil import parser
from pprint import PrettyPrinter
from copy import copy
from openerp.osv import osv, fields
from openerp.tools.translate import _

class PromericaParser(object):
    """Parser for Promerica's xlsx Bank Statements"""
    #from_card = False TODO: remove


    def statement_record (self, rec, **kwargs):
        '''** Kwargs parameter is used for a dynamic list of parameters. Due to
        the fact that not all bank statements include all the necessary information, 
        so to get it is strictly necessary to gather information from user. 
        If you need a new parameter, you specify its name and value, using the **kwargs
        as a dictionary, to extract a value use the respective key'''

        line_dict = {
            'transref': '', # _transmission_number
            'account_number': '', #_account_number
            'statementnr':'', # statement_number
            'startingbalance': 0.0, #_opening_balance
            'currencycode': '', #currencycode
            'endingbalance': 0.0, #_closing_balance
            'bookingdate': '', #moving_date
            'amount': 0.0,
            'id': '',
        }

        real_account = kwargs['real_account']
        account_number = kwargs['account_number']
        date_from = kwargs['date_from_str'] 
        date_to = kwargs['date_to_str']
        starting_balance = kwargs['starting_balance']
        ending_balance = kwargs['ending_balance']

        # Check if account numbers match
        if real_account != account_number:
            raise osv.except_osv(_('Import Error'),
                                 _('The account specified in file does not '
                                   'match with the one selected in wizard.'))

        line_dict['account_number'] = account_number
        # Get currency from wizard
        line_dict['currencycode'] = kwargs['local_currency']
        # Set name for the new bank statements to be created
        line_dict['statementnr'] = _('Promerica %s from %s to %s') % \
        (account_number, date_from, date_to)
        # transmission_number (Date when done the import)
        date_obj = datetime.strptime(date_from, '%Y-%m-%d')
        line_dict['transref'] = date_obj.strftime('%d-%m-%Y %H:%M:%S')
        line_dict['bookingdate'] = date_obj
        line_dict['startingbalance'] = starting_balance
        line_dict['endingbalance'] =  ending_balance
        line_dict['amount'] = starting_balance + ending_balance
        line_dict['id'] = _('Promerica %s from %s to %s') % \
        (account_number, date_from, date_to)
        
        return line_dict
    
    '''
    Parse all the lines in the file. Once the header
    is parser, the next step are the lines.
    '''     
    def statement_lines (self, rec):
        parser = PromericaParser()
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
        currencycode = '' # TODO: remove not used
        
        for record in rec:
            mapping['effective_date'] = record[0]
            mapping['execution_date'] = record[0]
            mapping['transfer_type'] = 'NTRF'
            mapping['reference'] = record[1]
            mapping['name'] = record[2]
            mapping['id'] = record[2]
            mapping['message'] = record[4]
            
            #Check if it is debit or credit
            amount = record[5]
            mapping['transferred_amount'] = amount
            if amount < 0:
                mapping['creditmarker'] = 'D'
            else:
                mapping['creditmarker'] = 'C'
                    
            lines.append(copy(mapping))
                            
        return lines   
    
    #clear special characters in a row. 
    def clean_special_characters(self, text_celd):
        special_characters = {'\r':''}
         
        for i, j in special_characters.iteritems():
            text = text_celd.replace(i, j)    
            
        #remove all the blank space.
        return re.sub(r'\s', '', text) 
    
    """
    ** Kwargs parameter is used for a dynamic list of parameters. 
        The wizard imported extracts used in all parsers 
        and not all parsers have all the necessary information in your file, 
        so get information from the wizard and passed by the ** kwargs. 
        Then in the parses that are needed, are extracted from the ** kwargs and if needed, 
        the parser still works the same way without this parameter.
        
        The rest of the methods must receive this parameter. (As the 
        method that parse the header and the lines). 
        
        If you need a new parameter, you specify its name and value, 
        using the ** kwargs is a dictionary, 
        extract its value, with the respective key
    """
    
    def parse_stamenent_record( self, rec, **kwargs): #parse the header.
        matchdict = dict()
        # Set the header for the statement
        matchdict = self.statement_record(rec, **kwargs);
        # TODO: check if we need effective_date or execution_date as date
        return matchdict
    
    #call the method that parse the header and the statements.    
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
            #parse_stamenent_record parse the header and the statements
            output.append( self.parse_stamenent_record( rec ) )
                
        return output
