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

from report import report_sxw
from report.report_sxw import rml_parse
import openerp.pooler as pooler
from openerp.tools.translate import _

class Parser(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(Parser, self).__init__(cr, uid, name, context)
        self.cursor = cr
        self.pool = pooler.get_pool(cr.dbname)
        self.localcontext.update({
            'get_label_name': self.get_label_name,
            'get_label_amount': self.get_label_amount,
            'get_label_account': self.get_label_account,
            'compute_payslip_lines': self.compute_payslip_lines,
        })

    def get_label_name(self):
        return _('Employee Name')

    def get_label_amount(self):
        return _('Amount')

    def get_label_account(self):
        return _('Bank Account')

    def compute_payslip_lines(self, data):
        payslip_run_id = data.get('payslip_run_id', False)
        if not payslip_run_id: return False
        employee_ids = data.get('employee_ids', False)
        if not employee_ids: return False
        salary_rule_id = data.get('salary_rule_id', False)
        if not salary_rule_id: return False
        self.cr.execute("""SELECT EMP.name_related AS employee_name,
  CASE WHEN EMP.bank_account_id IS NULL THEN ''
       ELSE
         (SELECT BANK.acc_number
         FROM res_partner_bank AS BANK
         WHERE EMP.bank_account_id = BANK.id
         LIMIT 1)
  END as acc_number,
  CASE WHEN
    (SELECT SUM(LINE.amount)
    FROM hr_payslip_line AS LINE
    WHERE LINE.slip_id = PAYSLIP.id AND
      LINE.salary_rule_id = %s) IS NULL THEN 0.0
  ELSE
    (SELECT SUM(LINE.amount)
    FROM hr_payslip_line AS LINE
    WHERE LINE.slip_id = PAYSLIP.id AND
      LINE.salary_rule_id = %s)
  END AS amount
FROM hr_employee as EMP,
  hr_payslip as PAYSLIP,
  hr_payslip_run as BATCH
WHERE EMP.id in %s AND
  EMP.id = PAYSLIP.employee_id AND
  BATCH.id = PAYSLIP.payslip_run_id AND
  BATCH.id = %s""",[salary_rule_id, salary_rule_id, tuple(employee_ids), payslip_run_id])
        result = self.cr.dictfetchall()
        return result