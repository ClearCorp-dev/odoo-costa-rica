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
        'account_voucher',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/paperformat.xml',
        'views/adime_percentage_view.xml',
        'views/res_partner_view.xml',
        'views/account_invoice_view.xml',
        'views/report_adime_payment.xml',
        'wizard/pay_adime_invoices_view.xml',
        'views/l10n_cr_adime_menu.xml',
    ],
}
