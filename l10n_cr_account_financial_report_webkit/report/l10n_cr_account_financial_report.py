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
from account_financial_report_webkit.report.common_reports import CommonReportHeaderWebkit
from account.report.account_financial_report import report_account_common

class l10n_cr_account_financial_report_parser(report_sxw.rml_parse,CommonReportHeaderWebkit):

    def __init__( self, cr, uid, name, context = None ):
        super(l10n_cr_account_financial_report_parser, self).__init__(cr, uid, name, context=context)
        account = report_account_common(cr,uid,name,context=context)
       
        self.localcontext.update( {           
            'get_lines': account.get_lines,
            'filter_form': self._get_filter,
            'get_fiscalyear': self._get_fiscalyear,
            'get_account': self._get_account,
            'get_start_period': self.get_start_period,
            'get_end_period': self.get_end_period,
            'get_filter': self._get_filter,
            'get_start_date':self._get_start_date,
            'get_end_date':self._get_end_date,
        })        
        self.context = context        
    
#the parameters are the report name and module name 
report_sxw.report_sxw( 'report.account_financial_report_webkit', 'account.financial.report',
                       'addons/l10n_cr_account_financial_report_webkit/report/l10n_cr_account_financial_report.mako', parser = l10n_cr_account_financial_report_parser, header = 'internal' )

#vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
