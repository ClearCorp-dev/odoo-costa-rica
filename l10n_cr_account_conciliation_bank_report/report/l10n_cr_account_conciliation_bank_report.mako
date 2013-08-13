<!DOCTYPE html SYSTEM "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
    <head>
        <link rel='stylesheet' href='addons/account_webkit_report_library/webkit_headers/main.css' />
        <style>
            ${css}
        </style>
    </head>
    <body>
        <%setLang(user.lang)%>
        <%
            bank_account = get_accounts_ids(cr, uid, data)
        %>
        <div class="table header">
            <div class="table-row">
                <div class="table-cell logo">${helper.embed_logo_by_name('default_logo', height=60)|n}</div>
                <div class="table-cell text">
                    <p class="company">${get_fiscal_year(data).company_id.name}</p>
                    <p class="title">${_('Conciliation Bank Report')}</p>
                    <p class="subtitle">${bank_account.name} - ${(bank_account.currency_id and bank_account.currency_id.name) or bank_account.company_id.currency_id.name}</p>
                </div>
            </div>
        </div>  
        <div class="table list">
            <div class="table-header">
                <div class="table-row labels no-wrap">
                    <div class="table-cell" style="width: 100px">${_('Fiscal Year')}<br/>${get_fiscal_year(data).name}</div>
                    <div class="table-cell" style="width: 100px">
                        %if get_filter(data) == 'filter_date':
                            ${_('Dates Filter')}
                        %elif get_filter(data) == 'filter_period':
                            ${_('Periods Filter')}
                        %else:
                            ${_('No filters')}
                        %endif
                    <br/>
                    %if get_filter(data) != 'filter_no':
                        ${_('To:')}
                        %if get_filter(data) == 'filter_date':
                            ${ formatLang(get_date_to(data), date=True)}
                        %else:
                            ${get_end_period(data).name}
                        %endif
                    %endif
                    </div>
                    <div class="table-cell" style="width: 100px">${_('Target Moves')}<br/>${ display_target_move(data) }</div>
                </div>
            </div>          
        </div>
        <br/><br/>
        <%
            account_id = get_accounts_ids(cr, uid, data).id        
            bank_balance, bank_move_lines, account_is_foreign = get_data(cr, uid, data, account_id)
            input_bank_balance = get_bank_balance(data) or 0.0
        %>
        <div align="center">
            <div class="table result">
                <div class="table-row blank no-wrap">
                   <div class="table-cell" style="width: 70px">&nbsp;</div>
                   <div class="table-cell" style="width: 70px">&nbsp;</div>
                   <div class="table-cell" style="width: 70px">${_('Balance according Bank')}</div>                   
                   %if input_bank_balance == bank_balance['bank_balance']:
                        <div class="act_as_cell amount">
                            ${formatLang(input_bank_balance)}           
                        </div>                     
                    %else:
                    <div class="act_as_cell amount alert">
                        ${formatLang(input_bank_balance)}
                    </div>
                    %endif
                </div>
                <div class="table-row labels no-wrap">
                    <div class="table-cell">${_('Ledger Balance')}</div>
                    <div class="table-cell amount">${formatLang(bank_balance['accounting_balance'])}</div>
                    <div class="table-cell">${_('Bank Balance')}</div>
                    <div class="table-cell amount">${formatLang(bank_balance['bank_balance'])}</div>
                </div>
                <div class="table-row blank no-wrap">
                    <div class="table-cell">${_('+ Incomes to register')}</div>
                    <div class="table-cell amount">${formatLang(bank_balance['incomes_to_register'])}</div>
                    <div class="table-cell">${_('+ Credits to reconcile')}</div>
                    <div class="table-cell amount">${formatLang(bank_balance['credits_to_reconcile'])}</div>
                </div>
                <div class="table-row blank no-wrap">
                    <div class="table-cell">${_('- Expenditures to register')}</div>
                    <div class="table-cell amount">${formatLang(bank_balance['expenditures_to_register'])}</div>
                    <div class="table-cell">${_('- Debits to reconcile')}</div>
                    <div class="table-cell amount">${formatLang(bank_balance['debits_to_reconcile'])}</div>
                </div>
                <div class="table-row labels no-wrap">
                    <div class="table-cell">${_('Ledger reconciled Total')}</div>
                    <div class="table-cell amount">${formatLang(bank_balance['accounting_total'])}</div>
                    <div class="table-cell">${_('Bank reconciled Total')}</div>
                    <div class="table-cell amount">${formatLang(bank_balance['bank_total'])}</div>
                </div>
            </div>  
        </div>        
        <%
            def cmp (first, second):
                list_ = [
                    'incomes_to_register',
                    'expenditures_to_register',
                    'credits_to_reconcile',
                    'debits_to_reconcile',
                ]
                first_index = len(first) > 0 and first[0] in list_ and list_.index(first[0]) or -1
                second_index = len(second) > 0 and second[0] in list_ and list_.index(second[0]) or -1
                
                return first_index - second_index
        %>        
        %for line_group_key, line_group in sorted(bank_move_lines.items(),cmp):
            <br/><br/>
            <div class="table header">
                <div class="table-row">
                   <div class="table-cell text">                                       
                       %if line_group_key == 'credits_to_reconcile':
                            <p class="subtitle">${_('Credits to reconcile')}</p>
                       %elif line_group_key == 'debits_to_reconcile':
                            <p class="subtitle">${_('Debits to reconcile')}</p>
                       %elif line_group_key == 'incomes_to_register':
                            <p class="subtitle">${_('Incomes to register')}</p>
                       %else:
                           <p class="subtitle">${_('Expenditures to register')}</p>
                       %endif
                   </div>        
                </div>
            </div>
            <br/><br/>
            <div class="table list">    
                 <div class="table-header">
                    <div class="table-row labels no-wrap">                       
                        <div class="table-cell first-column" style="width: 55px">${_('Date')}</div>
                        <div class="table-cell" style="width: 70px">${_('Period')}</div>
                        <div class="table-cell" style="width: 70px">${_('Journal')}</div>
                        <div class="table-cell" style="width: 100px">${_('Account')}</div>                    
                        <div class="table-cell" style="width: 100px">${_('Partner')}</div>
                        <div class="table-cell" style="width: 70px">${_('Reference')}</div>
                        <div class="table-cell" style="width: 100px">${_('Label')}</div>
                        <div class="table-cell last_column" style="width: 70px">${_('Amount')}</div>
                    </div>
                </div> 
                <div class="table-body"> 
                    %for line in line_group:
                        <div class="table-row ${row_even and 'even' or 'odd'}">
                            <div class="table-cell first-column">${formatLang(line.date, date=True)}</div>
                            <div class="table-cell">${line.period_id.code or ''}</div>
                            <div class="table-cell">${line.journal_id.code or ''}</div>                                    
                            <div class="table-cell">${line.account_id.code}</div>    
                            <div class="table-cell">
                                %if line.partner_id:
                                    ${(line.partner_id.ref and line.partner_id.ref + ' ') or ''}
                                    ${(line.partner_id.name and line.partner_id.name) or ''}
                                %else:
                                    ${_('-- No partner --')}
                                %endif
                            </div>
                            <div class="table-cell">${line.ref or ''}</div>
                            <div class="table-cell">${line.name}</div>    
                            <div class="act_as_cell last_column amount">
                                %if account_is_foreign:
                                    ${formatLang(line.amount_currency)}
                                %elif line.debit > 0:
                                    ${formatLang(line.debit)}
                                %else:
                                    ${formatLang(line.credit)}
                                %endif
                            </div>
                        </div>
                    %endfor                 
                </div>               
            </div>
            <div class="table-row spacer">
                <div class="table-cell">&nbsp;</div>
           </div>
            <div class="table list">           
               <div class="table-row subtotal">                     
                    <div class="table-cell first-column" style="width: 300px">
                       %if line_group_key == 'credits_to_reconcile':
                            ${_("Total")}&nbsp;${_('Credits to reconcile')}
                       %elif line_group_key == 'debits_to_reconcile':
                            ${_("Total")}&nbsp;${_('Debits to reconcile')}
                       %elif line_group_key == 'incomes_to_register':
                            ${_("Total")}&nbsp;${_('Incomes to register')}
                       %else:
                            ${_("Total")}&nbsp;${_('Expenditures to register')}
                       %endif
                   </div>
                   <div class="table-cell" style="width: 70px">&nbsp;</div>
                   <div class="table-cell" style="width: 70px">&nbsp;</div>
                   <div class="table-cell" style="width: 100px">&nbsp;</div>                    
                   <div class="table-cell" style="width: 100px">&nbsp;</div>
                   <div class="table-cell" style="width: 70px">&nbsp;</div>
                   <div class="table-cell" style="width: 100px">&nbsp;</div>
                   <div class="table-cell last_column amount" style="width: 70px">
                        %if account_is_foreign:
                            ${bank_account.currency_id.symbol}&nbsp;${formatLang(bank_balance[line_group_key]) or 0.0}
                        %else:
                            ${company.currency_id.symbol}&nbsp;${formatLang(bank_balance[line_group_key]) or 0.0}
                        %endif                   
                   </div>                
                </div>
            </div>
         %endfor
         <div class="table-row spacer">
            <div class="table-cell">&nbsp;</div>
         </div>
         <% 
           signatures = get_signatures_report(cr, uid, 'Conciliation Bank Report')
           cont = 0
         %>
         %if len(signatures) > 0:
            <div class="table header">
                <div class="table-row">
                    <div class="table-cell text">
                        <p class="title">${_('Authorized by: ')}</p>
                    </div>
                </div>
           </div>
           <br/><br/>
           <div class="table header">
                <div class="table-row">
                    <div class="table-cell text">
                    %for user_sign in signatures:
                        <div class="table-cell text">_________________________________________________________<br/>
                                                        <p class="subtitle">${user_sign.name}</p>
                                                        <p class="company"><i>${user_sign.job_id.name or ''}</i></p>
                        </div>
                        <br/><br/><br/>
                    </div>
                    %endfor                
                </div>
            </div>
        %endif
        <p style="page-break-after:always"></p>
    </body>
</html>

