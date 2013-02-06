<!DOCTYPE html SYSTEM "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
    <head>
        <link rel='stylesheet' href='addons/account_webkit_report_library/webkit_headers/main.css' />
        <style>
            ${css}
        </style>
    </head>
    <body>
        <%setLang(user.context_lang)%>
        <%
        filter_type = ''
        filter_data = []
        t_m = target_move(data) 
        %>
        <div class="table header">
           <div class="table-row">
               <div class="table-cell logo">${helper.embed_logo_by_name('internal_reports_logo', height=100)|n}</div>
               <br/>
               <div class="table-cell text">
                    <p class="title">${_('Account Bank Balance Report')}</p>
               </div>
           </div>
       </div>
        <div class="table list">
            <div class="table-header">
                <div class="table-row labels no-wrap">
                    <div class="table-cell first-column" style="width: 70px">${_('Chart of Account')}<br/>${ chart_account.name }</div>
                    <div class="table-cell" style="width: 100px">
                            %if filter_form(data) == 'filter_date':
                                ${_('Dates Filter')}
                            %elif filter_form(data) == 'filter_period': 
                                ${_('Periods Filter')}
                            %elif filter_form(data) == '':
                                ${_('Filter')}
                             %elif filter_form(data) == 'filter_opening':
                                ${_('Opening filter')}
                            %endif
                            <br/>
                            %if filter_form(data) == 'filter_date':
                                ${_('From:')}
                                ${formatLang(start_date, date=True) if start_date else u'' }
                                <% 
                                    filter_data.append(start_date) 
                                    filter_type = 'filter_date'
                                %>
                            %elif filter_form(data) == 'filter_period':
                                ${_('From:')}
                                ${start_period.name if start_period else u''}
                                <% 
                                    filter_data.append(start_period) 
                                    filter_type = 'filter_period'
                                %>
                            %elif filter_form(data) == '':
                                ${_('No filters')}                             
                            %elif filter_form(data) == 'filter_opening':
                                ${_('Opening balance')}
                            %endif                              
                            %if filter_form(data) == 'filter_date':
                                ${_('To:')}
                                ${ formatLang(stop_date, date=True) if stop_date else u'' }
                                <% filter_data.append(stop_date) %>                            
                            %elif filter_form(data) == 'filter_period':
                                ${_('To:')}
                                ${stop_period.name if stop_period else u'' }
                                <% filter_data.append(stop_period) %>                        
                            %endif             
                    </div>
                    <div class="table-cell" style="width: 100px">${_('Fiscal Year')}<br/>${ fiscalyear.name if fiscalyear else '-' }</div>                
                    <div div class="table-cell" style="width: 100px">${_('Target Moves')}<br/>${ display_target_move(data) }</div>
                </div>
            </div>
        </div>
        <%
        
        bank_accounts = get_bank_accounts(cr, uid)
        accounts_currency = accounts_by_currency(cr, uid, bank_accounts)

        %>
        %for currency, accounts in accounts_currency.iteritems():
            <br/><br/>
            <div class="table header">
                <div class="table-row">
                   <div class="table-cell text">
                        <p class="subtitle">${_('Account Bank Balance in: ')} ${currency}</p>
                   </div>
                </div>
            </div>
            <div class="table list">
                <div class="table-header">
                    <div class="table-row labels no-wrap">
                        ## code
                        <div class="table-cell first-column" style="width: 40px;">${_('Code')}</div>
                        ## account name
                        <div class="table-cell" style="width: 80px;">${_('Account')}</div>
                        ## initial balance
                        <div class="table-cell" style="width: 50px;">${_('Initial Balance')}</div>
                        ## TEFS
                        <div class="table-cell" style="width: 50px;">${_('Transfers')}</div>
                        ## Checks
                        <div class="table-cell" style="width: 50px;">${_('Checks')}</div>
                        ## Deposit
                        <div class="table-cell" style="width: 50px;">${_('Deposit')}</div>
                        ## debit
                        <div class="table-cell" style="width: 50px;">${_('Debit')}</div>
                        ## credit
                        <div class="table-cell" style="width: 50px;">${_('Credit')}</div>
                        ## balance
                        <div class="table-cell" style="width: 50px;">${_('Balance')}</div>                        
                    </div>
                </div>
                <div class="table-body">
                    %for account in sorted(set(accounts)):
                        <%
                            move_lines = get_move_lines_account(cr, uid, account.id,filter_type,filter_data,fiscalyear,t_m)
                            total_result = get_total_move_lines(cr, uid, move_lines, account)
                            initial_balance = get_initia_balance_accounts(cr, uid, accounts,filter_type, filter_data,fiscalyear,t_m,data['form']['chart_account_id'])
                        %>
                        <div class="table-row ${row_even and 'even' or 'odd'}">
                            ## code
                            <div class="table-cell first-column">${account.code}</div>
                            ## account name
                            <div class="table-cell">${account.name}</div>
                            <% 
                                foreign_currency = not account.company_id.currency_id.id == account.report_currency_id.id 
                            %>
                            %if foreign_currency:
                                ##foreign_balance
                                <div class="table-cell amount">${formatLang(initial_balance[account.id]['foreign_balance'])}</div>
                            %else:
                                 ##balance
                                <div class="table-cell amount">${formatLang(initial_balance[account.id]['balance'])}</div>
                            %endif
                            ##transfer
                            <div class="table-cell amount">${formatLang(total_result['amount_transf'])}</div>
                            ##check
                            <div class="table-cell amount">${formatLang(total_result['amount_check'])}</div>
                            ##deposit
                            <div class="table-cell amount">${formatLang(total_result['amount_deposit'])}</div>
                            ##debit
                            <div class="table-cell amount">${formatLang(total_result['amount_debit'])}</div>
                            ##credit
                            <div class="table-cell amount">${formatLang(total_result['amount_credit'])}</div> 
                            %if foreign_currency:
                                ##foreign_balance
                                <div class="table-cell amount">${formatLang(initial_balance[account.id]['foreign_balance']+total_result['amount_transf']+total_result['amount_check']+total_result['amount_deposit']+total_result['amount_debit']+total_result['amount_credit'])}</div>
                            %else:                            
                                ##balance
                                <div class="table-cell amount">${formatLang(initial_balance[account.id]['balance']+total_result['amount_transf']+total_result['amount_check']+total_result['amount_deposit']+total_result['amount_debit']+total_result['amount_credit'])}</div>
                           %endif
                        </div>                        
                    %endfor
                </div>
            </div>  
         %endfor  
        <p style="page-break-after:always"></p>         
    </body>
</html>
