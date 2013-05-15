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
{
	"name"        : "Voucher Check BCR",
	"author"      : "ClearCorp S.A.",
	"version"     : "0.1",
	"depends"     : ["base","account","account_report_lib","base_currency_symbol"],
	"init_xml"    : [],
	"update_xml"  : ['webkit_report/l10n_cr_account_voucher_check_bcr_webkit_header.xml',
					'l10n_cr_account_voucher_check_bcr_view.xml',
					'l10n_cr_account_voucher_check_bcr_report.xml',],
	"category"    : "Accounting",
	"active"      : False,
	"instalable"  : True,
}
