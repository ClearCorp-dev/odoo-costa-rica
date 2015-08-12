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

from openerp.osv import osv, fields
from ..tools import custom_encoder


class generatorWizardCreate(osv.TransientModel):

    _name = "hr.ins.csv.generator.generator.wizard"

    _columns = {
        'name': fields.char('Name', size=128),
        'salary_rule_ids': fields.many2many(
            'hr.salary.rule', string='Salary Rules', required=True),
        'date_start': fields.date('Date Start', required=True),
        'date_end': fields.date('Date End', required=True),
        'data': fields.binary('File', readonly=True),
        'state': fields.selection([
                ('generate', 'Generate'),  # generate file
                ('get', 'Get')  # get the file
            ], string='State'),
    }

    _defaults = {
        'state': 'generate',
    }

    def generate_csv(self, cr, uid, ids, context=None):
        this = self.browse(cr, uid, ids)[0]
        this.name = 'ins_generated_file.csv'
        codes = [rule.code for rule in this.salary_rule_ids]
        out = custom_encoder.encodeInsCsv(
            cr, uid, this.date_start, this.date_end,
            codes, context)
        self.write(cr, uid, ids, {
                'state': 'get',
                'data': out,
                'name': this.name,
            }, context=context)
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'hr.ins.csv.generator.generator.wizard',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': this.id,
            'views': [(False, 'form')],
            'target': 'new',
        }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
