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

from openerp.tools.translate import _
from openerp.osv import fields,osv, orm

class hrSettingsConf(osv.osv_memory):
    _inherit = 'hr.config.settings'
    
    def _check_percentage_limit_over_hundred(self, cr, uid, ids, context=None):
        for config in self.browse(cr, uid, ids, context=context):
            if config.first_limit > 100 or config.second_limit > 100:
                return False
        return True
    
    def _check_percentage_limit_under_zero(self, cr, uid, ids, context=None):
        for config in self.browse(cr, uid, ids, context=context):
            if config.first_limit < 0 or config.second_limit < 0:
                return False
        return True
    
    _columns = {
        'rent_company_id': fields.many2one('res.company', string='Company', required=True),
        'first_limit': fields.float('First Limit'),
        'second_limit':fields.float('Second Limit'), 
    }
    
    _defaults = {
        'first_limit': 0.0,
        'second_limit': 0.0,
    }
    
    _constraints = [
        (_check_percentage_limit_under_zero, 'Error! The percentage for first or second limit can not be under zero.', ['first_limit', 'second_limit']),
        (_check_percentage_limit_over_hundred, 'Error! The percentage for first or second limit can not be over hundred.', ['first_limit', 'second_limit']),
    ]
    
    """Override onchange_company_id to update rent limits """ 
    def onchange_rent_company_id(self, cr, uid, ids, rent_company_id, context=None):
        vals = {}
        if rent_company_id:
            company = self.pool.get('res.company').browse(cr, uid, rent_company_id, context=context)
            vals = {
                'first_limit': company.first_limit,
                'second_limit':company.second_limit, 
            }
        else:
            vals = {
                'first_limit': 0.0,
                'second_limit': 0.0, 
             }
            
        return {'value': vals}
                
    def get_default_rent_company_id(self, cr, uid, fields, context=None):
        """Get the default company for the module"""
        company_obj = self.pool.get('res.company')
        company_id = company_obj._company_default_get(cr, uid, 'l10n.cr.hr.payroll', context=context)
        return {'rent_company_id': company_id}
    
    """Get the default first_limit"""
    def get_first_limit(self, cr, uid, fields, context=None):
        company_obj = self.pool.get('res.company')
        company_id = company_obj._company_default_get(cr, uid, 'l10n.cr.hr.payroll', context=context) #module name
        company = company_obj.browse(cr, uid, company_id, context=context)
        return {'first_limit': company.first_limit}
    
    """Set the default first_limit"""
    def set_first_limit(self, cr, uid, ids, context=None):
        config = self.browse(cr, uid, ids[0], context)
        config.rent_company_id.write({'first_limit': config.first_limit})
    
    """Get the default limit_spouse_per"""
    def get_second_limit(self, cr, uid, fields, context=None):
        company_obj = self.pool.get('res.company')
        company_id = company_obj._company_default_get(cr, uid, 'l10n.cr.hr.payroll', context=context) #module name
        company = company_obj.browse(cr, uid, company_id, context=context)
        return {'second_limit': company.second_limit}
    
    """Set the default limit_spouse_per in the selected company"""
    def set_second_limit(self, cr, uid, ids, context=None):
        config = self.browse(cr, uid, ids[0], context)
        config.rent_company_id.write({'second_limit': config.second_limit})
