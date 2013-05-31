<!DOCTYPE html SYSTEM "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
    <head>
        <link rel='stylesheet' href='addons/report_webkit_lib/webkit_headers/main.css' />
        <style>
            ${css}
        </style>
    </head>
    <body class="data">
        <%setLang(user.lang)%>
        <%
            fiscalyear = get_fiscalyear(data)
            start_period = get_start_period(data)
            balance_data = get_data(cr, uid, data)
        %>
        <div class="table header">
            <div class="table-row">
                <div class="table-cell logo">${helper.embed_logo_by_name('default_logo', height=80)|n}</div>
                <div class="table-cell text">
                    <p class="company">${fiscalyear.company_id.partner_id.name}</p>
                    <p class="title">${_('Situation Balance at ')}${formatLang(start_period.date_stop, date=True)}</p>
                    <p class="subtitle">&nbsp;</p>
                </div>
            </div>
        </div>
        <br/><br/>
        <div class="table list">
            <div class="table-header">
                <div class="table-row labels no-wrap">
                    <div class="table-cell first-column" style="width: 70px">${_('Account<br />Code')}</div>
                    <div class="table-cell" style="width: 650px">${_('Account<br />Name')}</div>
                    <div class="table-cell" style="width: 100px">${_('Fiscal Year Opening')}<br />${fiscalyear.name}</div>
                    <div class="table-cell" style="width: 100px">${_('Selected period')}<br />${start_period.name}</div>\
                    <div class="table-cell" style="width: 100px">${_('Variation')}<br />${_('Per. vs. FY Open.')}</div>
                    <div class="table-cell last-column" style="width: 40px">${_('Var.')}<br />${_('%')}</div>
                </div>
            </div>
            <div class="table-body">
                <%
                    asset_total_period = balance_data['total_asset_balances']['period']
                    asset_total_fiscalyear = balance_data['total_asset_balances']['fiscal_year']
                    asset_total_variation = asset_total_period - asset_total_fiscalyear
                    asset_total_percentage_variation = asset_total_fiscalyear != 0 and (100 * asset_total_variation / asset_total_fiscalyear) or 0
                    
                    liability_total_period = balance_data['total_liability_balances']['period']
                    liability_total_fiscalyear = balance_data['total_liability_balances']['fiscal_year']
                    liability_total_variation = liability_total_period - liability_total_fiscalyear
                    liability_total_percentage_variation = liability_total_fiscalyear != 0 and (100 * liability_total_variation / liability_total_fiscalyear) or 0
                    
                    equity_total_period = balance_data['total_equity_balances']['period']
                    equity_total_fiscalyear = balance_data['total_equity_balances']['fiscal_year']
                    equity_total_variation = equity_total_period - equity_total_fiscalyear
                    equity_total_percentage_variation = equity_total_fiscalyear != 0 and (100 * equity_total_variation / equity_total_fiscalyear) or 0
                    
                    income_total_period = balance_data['total_income_balance']['period']
                    income_total_fiscalyear = balance_data['total_income_balance']['fiscal_year']
                    income_total_variation = income_total_period - income_total_fiscalyear
                    income_total_percentage_variation = income_total_fiscalyear != 0 and (100 * income_total_variation / income_total_fiscalyear) or 0
                    
                    expense_total_period = balance_data['total_expense_balance']['period']
                    expense_total_fiscalyear = balance_data['total_expense_balance']['fiscal_year']
                    expense_total_variation = expense_total_period - expense_total_fiscalyear
                    expense_total_percentage_variation = expense_total_fiscalyear != 0 and (100 * expense_total_variation / expense_total_fiscalyear) or 0
                    
                    profit_total_period = income_total_period + expense_total_period
                    profit_total_fiscalyear = income_total_fiscalyear + expense_total_fiscalyear
                    profit_total_variation = profit_total_period - profit_total_fiscalyear
                    profit_total_percentage_variation = profit_total_fiscalyear != 0 and (100 * profit_total_variation / profit_total_fiscalyear) or 0
                    
                    liability_equity_total_period = liability_total_period + equity_total_period
                    liability_equity_total_fiscalyear = liability_total_fiscalyear + equity_total_fiscalyear
                    liability_equity_total_variation = liability_equity_total_period - liability_equity_total_fiscalyear
                    liability_equity_total_percentage_variation = liability_equity_total_fiscalyear != 0 and (100 * liability_equity_total_variation / liability_equity_total_fiscalyear) or 0
                    
                    liability_equity_profit_total_period = liability_total_period + equity_total_period + profit_total_period
                    liability_equity_profit_total_fiscalyear = liability_total_fiscalyear + equity_total_fiscalyear + profit_total_fiscalyear
                    liability_equity_profit_total_variation = liability_equity_profit_total_period - liability_equity_profit_total_fiscalyear
                    liability_equity_profit_total_percentage_variation = liability_equity_profit_total_fiscalyear != 0 and (100 * liability_equity_profit_total_variation / liability_equity_profit_total_fiscalyear) or 0
                %>
                <% row_even = False %>
                %for account in balance_data['asset_accounts']:
                    <%
                        account_total_period = balance_data['asset_period_balances'][account.id]['balance']
                        account_total_fiscalyear = balance_data['asset_fiscal_year_balances'][account.id]['balance']
                        account_total_variation = account_total_period - account_total_fiscalyear
                        account_total_percentage_variation = account_total_fiscalyear != 0 and (100 * account_total_variation / account_total_fiscalyear) or 0
                    %>
                    %if account.level == 0:
                    <div class="table-row bold ${row_even and 'even' or 'odd'}">
                    %elif account.child_id:
                    <div class="table-row bold ${row_even and 'even' or 'odd'}">
                    %else:
                    <div class="table-row ${row_even and 'even' or 'odd'}">
                    %endif
                        <div class="table-cell first-column">${account.code}</div>
                        <div class="table-cell" style="padding-left:${account.level*10}px">${_(account.name)}</div>
                        <div class="table-cell amount" >${formatLang(account_total_fiscalyear)}</div>
                        <div class="table-cell amount" >${formatLang(account_total_period)}</div>
                        <div class="table-cell amount" >${formatLang(account_total_variation)}</div>
                        <div class="table-cell amount last-column" >${formatLang(account_total_percentage_variation)}</div>
                    </div>
                    <%
                        if row_even:
                            row_even = False
                        else:
                            row_even = True
                    %>
                %endfor
                <div class="table-row subtotal">
                    <div class="table-cell first-column">&nbsp;</div>
                    <div class="table-cell">${_('ASSET TOTAL')}</div>
                    <div class="table-cell amount" >${formatLang(asset_total_fiscalyear)}</div>
                    <div class="table-cell amount" >${formatLang(asset_total_period)}</div>
                    <div class="table-cell amount" >${formatLang(asset_total_variation)}</div>
                    <div class="table-cell amount last-column" >${formatLang(asset_total_percentage_variation)}</div>
                </div>
                <div class="table-row spacer">
                    <div class="table-cell">&nbsp;</div>
                </div>
                
                <% row_even = False %>
                %for account in balance_data['liability_accounts']:
                    <%
                        account_total_period = balance_data['liability_period_balances'][account.id]['balance']
                        account_total_fiscalyear = balance_data['liability_fiscal_year_balances'][account.id]['balance']
                        account_total_variation = account_total_period - account_total_fiscalyear
                        account_total_percentage_variation = account_total_fiscalyear != 0 and (100 * account_total_variation / account_total_fiscalyear) or 0
                    %>
                    %if account.level == 0:
                    <div class="table-row bold ${row_even and 'even' or 'odd'}">
                    %elif account.child_id:
                    <div class="table-row bold ${row_even and 'even' or 'odd'}">
                    %else:
                    <div class="table-row ${row_even and 'even' or 'odd'}">
                    %endif
                        <div class="table-cell first-column">${account.code}</div>
                        <div class="table-cell" style="padding-left:${account.level*10}px">${_(account.name)}</div>
                        <div class="table-cell amount" >${formatLang(account_total_fiscalyear)}</div>
                        <div class="table-cell amount" >${formatLang(account_total_period)}</div>
                        <div class="table-cell amount" >${formatLang(account_total_variation)}</div>
                        <div class="table-cell amount last-column" >${formatLang(account_total_percentage_variation)}</div>
                    </div>
                    <%
                        if row_even:
                            row_even = False
                        else:
                            row_even = True
                    %>
                %endfor
                <div class="table-row subtotal">
                    <div class="table-cell first-column">&nbsp;</div>
                    <div class="table-cell">${_('LIABILITY TOTAL')}</div>
                    <div class="table-cell amount" >${formatLang(liability_total_fiscalyear)}</div>
                    <div class="table-cell amount" >${formatLang(liability_total_period)}</div>
                    <div class="table-cell amount" >${formatLang(liability_total_variation)}</div>
                    <div class="table-cell amount last-column" >${formatLang(liability_total_percentage_variation)}</div>
                </div>
                <div class="table-row spacer">
                    <div class="table-cell">&nbsp;</div>
                </div>
                
                <% row_even = False %>
                %for account in balance_data['equity_accounts']:
                    <%
                        account_total_period = balance_data['equity_period_balances'][account.id]['balance']
                        account_total_fiscalyear = balance_data['equity_fiscal_year_balances'][account.id]['balance']
                        account_total_variation = account_total_period - account_total_fiscalyear
                        account_total_percentage_variation = account_total_fiscalyear != 0 and (100 * account_total_variation / account_total_fiscalyear) or 0
                    %>
                    %if account.level == 0:
                    <div class="table-row bold ${row_even and 'even' or 'odd'}">
                    %elif account.child_id:
                    <div class="table-row bold ${row_even and 'even' or 'odd'}">
                    %else:
                    <div class="table-row ${row_even and 'even' or 'odd'}">
                    %endif
                        <div class="table-cell first-column">${account.code}</div>
                        <div class="table-cell" style="padding-left:${account.level*10}px">${_(account.name)}</div>
                        <div class="table-cell amount" >${formatLang(account_total_fiscalyear)}</div>
                        <div class="table-cell amount" >${formatLang(account_total_period)}</div>
                        <div class="table-cell amount" >${formatLang(account_total_variation)}</div>
                        <div class="table-cell amount last-column" >${formatLang(account_total_percentage_variation)}</div>
                    </div>
                    <%
                        if row_even:
                            row_even = False
                        else:
                            row_even = True
                    %>
                %endfor
                <div class="table-row subtotal">
                    <div class="table-cell first-column">&nbsp;</div>
                    <div class="table-cell">${_('EQUITY TOTAL')}</div>
                    <div class="table-cell amount" >${formatLang(equity_total_fiscalyear)}</div>
                    <div class="table-cell amount" >${formatLang(equity_total_period)}</div>
                    <div class="table-cell amount" >${formatLang(equity_total_variation)}</div>
                    <div class="table-cell amount last-column" >${formatLang(equity_total_percentage_variation)}</div>
                </div>
                
                <div class="table-row spacer">
                    <div class="table-cell">&nbsp;</div>
                </div>
                <div class="table-row spacer">
                    <div class="table-cell">&nbsp;</div>
                </div>
                <div class="table-row subtotal">
                    <div class="table-cell first-column">&nbsp;</div>
                    <div class="table-cell">${_('LIABITLITY + EQUITY TOTAL')}</div>
                    <div class="table-cell amount" >${formatLang(liability_equity_total_fiscalyear)}</div>
                    <div class="table-cell amount" >${formatLang(liability_equity_total_period)}</div>
                    <div class="table-cell amount" >${formatLang(liability_equity_total_variation)}</div>
                    <div class="table-cell amount last-column" >${formatLang(liability_equity_total_percentage_variation)}</div>
                </div>
                <div class="table-row subtotal">
                    <div class="table-cell first-column">&nbsp;</div>
                    <div class="table-cell">${_('PROFIT TOTAL')}</div>
                    <div class="table-cell amount" >${formatLang(profit_total_fiscalyear)}</div>
                    <div class="table-cell amount" >${formatLang(profit_total_period)}</div>
                    <div class="table-cell amount" >${formatLang(profit_total_variation)}</div>
                    <div class="table-cell amount last-column" >${formatLang(profit_total_percentage_variation)}</div>
                </div>
                <div class="table-row total">
                    <div class="table-cell first-column">&nbsp;</div>
                    <div class="table-cell">${_('LIABITLITY + EQUITY + PROFIT TOTAL')}</div>
                    <div class="table-cell amount" >${formatLang(liability_equity_profit_total_fiscalyear)}</div>
                    <div class="table-cell amount" >${formatLang(liability_equity_profit_total_period)}</div>
                    <div class="table-cell amount" >${formatLang(liability_equity_profit_total_variation)}</div>
                    <div class="table-cell amount last-column" >${formatLang(liability_equity_profit_total_percentage_variation)}</div>
                </div>
                <div class="table-row total">
                    <div class="table-cell first-column">&nbsp;</div>
                    <div class="table-cell">${_('ASSET TOTAL')}</div>
                    <div class="table-cell amount" >${formatLang(asset_total_fiscalyear)}</div>
                    <div class="table-cell amount" >${formatLang(asset_total_period)}</div>
                    <div class="table-cell amount" >${formatLang(asset_total_variation)}</div>
                    <div class="table-cell amount last-column" >${formatLang(asset_total_percentage_variation)}</div>
                </div>
            </div>
        </div>
        <div class="table-row spacer">
            <div class="table-cell">&nbsp;</div>
        </div>
        <% 
           signatures = get_signatures_report(cr, uid, 'Situation Balance Report')
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
