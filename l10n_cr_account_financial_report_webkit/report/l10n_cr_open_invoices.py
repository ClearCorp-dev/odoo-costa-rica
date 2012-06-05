# -*- encoding: utf-8 -*-
##############################################################################
#
#    Author: Nicolas Bessi, Guewen Baconnier
#    Copyright Camptocamp SA 2011
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

from openerp.addons.account_financial_report_webkit.report.open_invoices import PartnersOpenInvoicesWebkit
from openerp.addons.account_financial_report_webkit.report.webkit_parser_header_fix import HeaderFooterTextWebKitParser

class l10n_cr_PartnersOpenInvoicesWebkit(PartnersOpenInvoicesWebkit):

    def __init__(self, cursor, uid, name, context):
        super(l10n_cr_PartnersOpenInvoicesWebkit, self).__init__(cursor, uid, name, context=context)
        self.pool = pooler.get_pool(self.cr.dbname)
        self.cursor = self.cr



HeaderFooterTextWebKitParser('report.account_financial_report_webkit.account.account_report_open_invoices_webkit',
                             'account.account',
                             'addons/l10n_cr_account_financial_report_webkit/report/l10n_cr_account_report_open_invoices.mako',
                             parser=l10n_cr_PartnersOpenInvoicesWebkit)
