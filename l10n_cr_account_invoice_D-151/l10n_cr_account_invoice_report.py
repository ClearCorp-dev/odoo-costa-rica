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

class AccountInvoiceReport(osv.Model):

    _name = 'account.invoice.report'
    _inherit = 'account.invoice.report'

    _columns = {
        'd_151_type':fields.selection([('V','Goods and services sales'),
                                       ('C','Goods and services purchases'),
                                       ('A','Rent'),
                                       ('SP','Profesional services'),
                                       ('M','Commissions'),
                                       ('I','Interest')], string='D-151 Type',readonly=True),
    }

    #Add into query the D-151-type field
    def _select (self):
        select_str = super(AccountInvoiceReport, self)._select()
        new_str = select_str.replace('SELECT sub.id,', 'SELECT sub.id, sub.d_151_type,')
        return new_str

    #Add into query the D-151-type field
    def _sub_select(self):
        select_str = super(AccountInvoiceReport, self)._sub_select()
        new_str = select_str.replace('ai.payment_term, ai.period_id,', 'ai.payment_term, ai.period_id, ail.d_151_type AS d_151_type,')
        return new_str

    #Add into query the D-151-type field
    def _group_by(self):
        group_by_str = super(AccountInvoiceReport,self)._group_by()
        new_str = group_by_str.replace('GROUP BY ail.product_id,', 'GROUP BY ail.product_id, ail.d_151_type,')
        return new_str