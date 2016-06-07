# -*- coding: utf-8 -*-
# © 2016 ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Costa Rica ADIME Management',
    'version': '8.0.1.0',
    'category': 'Accounting & Finance',
    'website': 'http://clearcorp.cr',
    'author': 'ClearCorp',
    'license': 'AGPL-3',
    'sequence': 10,
    'application': False,
    'installable': True,
    'auto_install': False,
    'depends': [
        'account',
        'stock',
        'purchase',
    ],
    'data': [
        'views/adime_view.xml',
        'views/account_invoice_view.xml',
        'views/partner_view.xml',
        'views/product_view.xml',
        'views/adime_assigned_view.xml',
        'views/adime_sequence.xml',
        'views/adime_workflow.xml',
    ],
}
