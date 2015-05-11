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
from openerp.tools.translate import _

class acccountAccounttypeProfitstatement(orm.Model):
    """
        This class extend functions of account.account.type
        
        If include_profit_statement_report is checked, those accounts that have this account_type and type == 'view' are include in Profit Statement Report.
        
    """  
    _name = "account.account.type"
    _inherit = "account.account.type"
    
    _columns = {
        'include_profit_statement_report': fields.boolean('Include in Profit Statement Report', help="If it's checked, the account that have this type is include in Profit Statement Report Wizard as Base Account to compare.")
    }