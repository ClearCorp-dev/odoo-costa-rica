##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>).
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
from openerp.addons.account_financial_report_webkit.report.common_reports import CommonReportHeaderWebkit
from addons.account.report import report_account_common

class l10n_cr_account_financial_report_parser( report_sxw.rml_parse, CommonReportHeaderWebkit ):

    def __init__( self, cr, uid, name, context = None ):
        super( l10n_cr_account_financial_report_parser, self ).__init__( cr, uid, name, context = context )
        self.localcontext.update( { 
            #'get_lines' : report_account_common.get_lines,
        })

#the parameters are the report name and module name 
report_sxw.report_sxw( 'report.account_financial_report_webkit', 'account.financial.report',
                       'addons/l10n_cr_account_financial_report_webkit/report/l10n_cr_account_financial_report.mako', parser = l10n_cr_account_financial_report_parser, header = 'internal' )


#vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
