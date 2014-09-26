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

from openerp.osv import fields, osv, orm

class accountInvoiceD151(orm.Model):
    
    _name = 'account.invoice'
    _inherit = 'account.invoice'

    #Work arround to get the type of the invoice from context
    def _get_type_invoice(self, cr, uid, context=None):
        if context is None:
            context = {}
        return context.get('type')

    #This field add category D-151 to invoice line.
    _columns = {
        'type_invoice': fields.char(string='Invoice type', size=64)
    }
    
    #Get the type of invoice for category D-151    
    _defaults = {
        'type_invoice': _get_type_invoice,
    }

class accountInvoicelineD151(orm.Model):
    
    _name = 'account.invoice.line'
    _inherit = 'account.invoice.line'

    #Work arround to get the type of the invoice from context
    def _get_type_invoice(self, cr, uid, context=None):
        if context is None:
            context = {}
        return context.get('type')

    #This field add category D-151 to invoice line.
    _columns = {
        'd_151_type':fields.selection([('V','Goods and services sales'),
                                       ('C','Goods and services purchases'),
                                       ('A','Rent'),
                                       ('SP','Profesional services'),
                                       ('M','Commissions'),
                                       ('I','Interest')], string="D-151 Type"),
       
        'type_invoice': fields.char(string='Invoice type', size=64)
    }
    
    #Get the type of invoice for category D-151    
    _defaults = {
        'type_invoice': _get_type_invoice,
    }
