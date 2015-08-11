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


class Employee(osv.Model):

    _inherit = 'hr.employee'

    _defaults = {
        'ins_exportable': True,
        'ins_working_day': 'Tiempo completo',
        'ins_paid_days': 30,
        'ins_paid_hours': 240,
    }

    _columns = {
        'ins_exportable': fields.boolean('Export?'),
        'ins_id_type': fields.selection([
                ('CN', 'Cédula Nacional'),
                ('CR', 'Cédula Residencia'),
                ('NP', 'Número Pasaporte'),
                ('PT', 'Permiso Trabajo'),
                ('SD', 'Sin Documentos'),
            ], 'Id Type'),
        'ins_name': fields.char('Name', size=128),
        'ins_last_name1': fields.char('First Last Name', size=128),
        'ins_last_name2': fields.char('Second Last Name', size=128),
        'ins_working_day': fields.selection([
                ('Tiempo completo', 'Tiempo completo'),
                ('Medio tiempo', 'Medio tiempo'),
                ('Ocasional', 'Ocasional'),
                ('Por jornales', 'Por jornales'),
            ], 'Working Day'),
        'ins_paid_days': fields.integer('Paid Days'),
        'ins_paid_hours': fields.integer('Paid Hours'),
        'ins_job_code': fields.char('Job Code'),
    }
