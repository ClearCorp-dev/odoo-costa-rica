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
    "name" : "l10n_cr_account_voucher",
    "version" : "1.0",
    "author" : 'CLEARCORP S.A.',
    'complexity': "normal",
    "description": """
Localization of Account Voucher
Changed the refence field of account_voucher to required
""",
    "category": 'Accounting & Finance',
    "sequence": 4,
    "website" : "http://clearcorp.co.cr",
    "images" : [],
    "icon" : False,
    "depends" : ["account_voucher"], 
    "init_xml" : [],
    "demo_xml" : [],
    "update_xml" : [
	'l10n_cr_account_voucher_view.xml',
	"l10n_cr_voucher_payment_receipt_view.xml",
	"l10n_cr_voucher_sales_purchase_view.xml"
    ],
    "test" : [],
    'auto_install': False,
    "application": True,
    "installable": True,
    'license': 'AGPL-3',
}

