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

from openerp.osv import fields, osv

class accountInvoicelineD151(osv.Model):

    _inherit = 'account.invoice.line'

    def _get_type_invoice(self, cr, uid, context=None):
        if context is None:
            context = {}
        return context.get('type')

    def _get_type_invoice_line(self, cr, uid, ids, field_name, arg, context=None):
        res={}
        for line in self.browse(cr, uid, ids,context=context):
            res[line.id] = line.invoice_id.type
        return res

    #This field add category D-151 to invoice line.
    _columns = {
        'd_151_type':fields.selection([('V','Goods and services sales'),
                                       ('C','Goods and services purchases'),
                                       ('A','Rent'),
                                       ('SP','Profesional services'),
                                       ('M','Commissions'),
                                       ('I','Interest')], string="D-151 Type"),
        'type_invoice': fields.function(_get_type_invoice_line, type='char', string='Invoice type', size=64)
    }

    #Get the type of invoice for category D-151    
    _defaults = {
        'type_invoice': _get_type_invoice,
    }