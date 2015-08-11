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

import base64
import cStringIO
import csv
import openerp.pooler as pooler


def encodeInsCsv(cr, uid, date_start, date_end, codes, context=None):
    def _information_export(_buffer, cr, uid, codes, context):
        def _get_user_wage(
                cr, uid, pool, date_start, date_end, codes, _id, context):
            payslip_obj = pool.get('hr.payslip')
            payslip_ids = payslip_obj.search(
                cr, uid, [
                    ('employee_id', '=', _id),
                    ('date_to', '>=', date_start),
                    ('date_to', '<=', date_end)
                ], context=context)
            payslips = payslip_obj.browse(
                cr, uid, payslip_ids, context=context)
            wage_sum = 0
            for payslip in payslips:
                for line in payslip.line_ids:
                    if line.salary_rule_id.code in codes:
                        wage_sum += line.total
            return int(wage_sum)

        def _encode(s):
            if isinstance(s, unicode):
                return s.encode('utf8')
            else:
                if isinstance(s, bool):
                    return ''
                return str(s)

        def _process(employees, _buffer):
            writer = csv.writer(_buffer, 'excel', delimiter=';')
            # write header first
            writer.writerow(("TI", "NA", "N° Cedula", "N° Asegurado", "Nombre",
                             "Apellido1", "Apellido2", "Tipo Jornada", "Dias",
                             "Horas", "Salario", "Observaciones", "Ocupacion"))
            for _tuple in employees:
                employee = _tuple[0]
                writer.writerow((
                    _encode(employee.ins_id_type),
                    _encode(employee.country_id.code),
                    _encode(employee.identification_id),
                    _encode(employee.sinid),
                    _encode(employee.ins_name),
                    _encode(employee.ins_last_name1),
                    _encode(employee.ins_last_name2),
                    _encode(employee.ins_working_day),
                    _encode(employee.ins_paid_days),
                    _encode(employee.ins_paid_hours),
                    _encode(_tuple[1]),
                    "",  # Observations are not added automatically
                    _encode(employee.ins_job_code)
                ))
        dbname = cr.dbname
        pool = pooler.get_pool(dbname)
        employee_obj = pool.get('hr.employee')
        employee_ids = employee_obj.search(
            cr, uid, [('ins_exportable', '=', True)], context=context)
        employees = employee_obj.browse(cr, uid, employee_ids, context=context)
        tmp_employees = []
        for employee in employees:
            ins_wage = _get_user_wage(
                cr, uid, pool, date_start, date_end,
                codes, employee.id, context)
            tmp_employees.append((employee, ins_wage))
        _process(tmp_employees, _buffer)

    _buffer = cStringIO.StringIO()
    _information_export(_buffer, cr, uid, codes, context)
    out = base64.encodestring(_buffer.getvalue())
    _buffer.close()
    return out
