# -*- encoding: utf-8 -*-
##############################################################################
#
#    __terp__.py
#    l10n_cr_base
#    First author: Carlos Vásquez <carlos.vasquez@clearcorp.co.cr> (ClearCorp S.A.)
#    Copyright (c) 2010-TODAY ClearCorp S.A. (http://clearcorp.co.cr). All rights reserved.
#    
#    Redistribution and use in source and binary forms, with or without modification, are
#    permitted provided that the following conditions are met:
#    
#       1. Redistributions of source code must retain the above copyright notice, this list of
#          conditions and the following disclaimer.
#    
#       2. Redistributions in binary form must reproduce the above copyright notice, this list
#          of conditions and the following disclaimer in the documentation and/or other materials
#          provided with the distribution.
#    
#    THIS SOFTWARE IS PROVIDED BY <COPYRIGHT HOLDER> ``AS IS'' AND ANY EXPRESS OR IMPLIED
#    WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
#    FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> OR
#    CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
#    CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
#    SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
#    ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
#    NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
#    ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#    
#    The views and conclusions contained in the software and documentation are those of the
#    authors and should not be interpreted as representing official policies, either expressed
#    or implied, of ClearCorp S.A..

{
    'name': 'Costa Rica localisation: Base',
    'version': '0.1',
    'url': 'http://launchpad.net/openerp-costa-rica',
    'author': 'ClearCorp S.A.',
    'website': 'http://clearcorp.co.cr',
    'category': 'Localisation/Generic Modules',
    'description': """Base module localization for Costa Rica
    Includes:
      * res.bank: Costa Rican banks
      * res.country.state: Costa Rican provinces with official codes
      * res.partner.function: Commonly used functions in Costa Rica
      * res.partner.title: Commontly used partner titles in Costa Rica
    
    Everything is in English with Spanish translation. Further translations are welcome, please go to
    http://translations.launchpad.net/openerp-costa-rica
    """,
    'depends': ['base','base_currency_symbol'],
    'init_xml': [
        ],
    'demo_xml': [
        'l10n_cr_base_demo.xml',
        ],
    'update_xml': [
        #'res.bank.csv',
        'l10n_cr_base_data.xml',
        'l10n_cr_base_view.xml',
        'l10n_cr_base.sql',
        'l10n_cr_base_demo.sql',
        ],
    'license': 'Other OSI approved licence',
    'installable': True,
    'active': True,
}
