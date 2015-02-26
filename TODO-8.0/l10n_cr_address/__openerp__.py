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
    'name': 'Costa Rican Addresses',
    'version': '1.0',
    'category': 'Hidden',
    'sequence': 10,
    'summary': 'Costa Rican Locations',
    'description': """
Adds Costa Rican counties, districts and regions.""",
    'author': 'ClearCorp',
    'website': 'http://clearcorp.co.cr',
    'complexity': 'easy',
    'images' : [],
    'depends': ['base'],
    'data': [
             'l10n_cr_address_view.xml',
             'data/l10n_cr_address_data.xml',
             'security/ir.model.access.csv',
             ],
    'test' : [],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'AGPL-3',
}
