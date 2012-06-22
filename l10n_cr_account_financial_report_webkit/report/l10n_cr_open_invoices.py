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

import pooler

from collections import defaultdict
from report import report_sxw
from datetime import datetime
from itertools import groupby
from operator import itemgetter
from mako.template import Template

from tools.translate import _

from openerp.osv import osv
from openerp.addons.report_webkit import report_helper
import addons

from l10n_cr_partners_ledger import l10n_cr_PartnersLedgerWebkit
from openerp.addons.account_financial_report_webkit.report.webkit_parser_header_fix import HeaderFooterTextWebKitParser

class l10n_cr_PartnersOpenInvoicesWebkit(l10n_cr_PartnersLedgerWebkit):

    def __init__(self, cursor, uid, name, context):
        super(l10n_cr_PartnersOpenInvoicesWebkit, self).__init__(cursor, uid, name, context=context)
        self.pool = pooler.get_pool(self.cr.dbname)
        self.cursor = self.cr

        company = self.pool.get('res.users').browse(self.cr, uid, uid, context=context).company_id
        header_report_name = ' - '.join((_('OPEN INVOICES REPORT'), company.name, company.currency_id.name))

        footer_date_time = self.formatLang(str(datetime.today()), date_time=True)

        self.localcontext.update({
            'is_open': self.is_open,
            'report_name':_('Open Invoices Report'),
            'additional_args': [
                ('--header-font-name', 'Helvetica'),
                ('--footer-font-name', 'Helvetica'),
                ('--header-font-size', '10'),
                ('--footer-font-size', '6'),
                ('--header-left', header_report_name),
                ('--header-spacing', '2'),
                ('--footer-left', footer_date_time),
                ('--footer-right', ' '.join((_('Page'), '[page]', _('of'), '[topage]'))),
                ('--footer-line',),
            ],
        })

    def is_open(self,cr, uid, account_move_line):
        move_line_obj = self.pool.get('account.move.line').browse(cr,uid,account_move_line['id'])
    
        if move_line_obj.reconcile_id.id == False:
            return True
        else:
            return False

HeaderFooterTextWebKitParser('report.account_financial_report_webkit.account.account_report_open_invoices_webkit',
                             'account.account',
                             'addons/l10n_cr_account_financial_report_webkit/report/l10n_cr_account_report_open_invoices.mako',
                             parser=l10n_cr_PartnersOpenInvoicesWebkit)
