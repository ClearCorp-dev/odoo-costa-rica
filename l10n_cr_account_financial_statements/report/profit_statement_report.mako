<!DOCTYPE html SYSTEM "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
    <head>
        <link rel='stylesheet' href='addons/account_webkit_report_library/webkit_headers/main.css' />
        <style>
            ${css}
        </style>
    </head>
    <body class="data">
        <%setLang(user.context_lang)%>
        <%
            last_period = get_last_period(cr, uid, start_period)
            fiscalyear = get_fiscalyear(cr, uid, start_period)
            balance_data = get_data(cr, uid, data)
        %>
        <div class="table header">
            <div class="table-row">
                <div class="table-cell logo">${helper.embed_logo_by_name('internal_reports_logo', height=80)|n}</div>
                <div class="table-cell text">
                    <p class="company">${company.partner_id.name}</p>
                    <p class="title">${_('Profit Statement')}</p>
                    <p class="subtitle">${_('Profit Statement of:')} ${start_period.name}</p>
                </div>
            </div>
        </div>
        <div class="table list">
            <div class="table-header">
                <div class="table-row labels no-wrap">
                    <div class="table-cell first-column" style="width: 70px">${_('Account')}<br />${_('Code')}</div>
                    <div class="table-cell" style="width: 430px">${_('Account')}<br />${_('Name')}</div>
                    <div class="table-cell amount" style="width: 100px">${_('Previous period')}<br />${last_period.name}</div>
                    <div class="table-cell amount" style="width: 40px">${_('%')}<br />${_('V')}</div>
                    <div class="table-cell amount" style="width: 100px">${_('Selected period')}<br />${start_period.name}</div>
                    <div class="table-cell amount" style="width: 40px">${_('%')}<br />${_('V')}</div>
                    <div class="table-cell amount" style="width: 100px">${_('Variation')}<br />${_('Prev. vs Sel.')}</div>
                    <div class="table-cell amount" style="width: 40px">${_('Var.')}<br />${_('%')}</div>
                    <div class="table-cell amount" style="width: 100px">${_('Acum. Fiscal Year')}<br />${fiscalyear.name}</div>
                    <div class="table-cell last-column amount" style="width: 40px">${_('%')}<br />${_('V')}</div>
                </div>
            </div>
            <div class="table-body">
                <%
                    income_total_period = balance_data['total_income_balances']['period']
                    income_total_last_period = balance_data['total_income_balances']['last_period']
                    income_total_fiscalyear = balance_data['total_income_balances']['fiscal_year']
                    income_total_variation = income_total_period - income_total_last_period
                    income_total_percentage_period = 100
                    income_total_percentage_last_period = 100
                    income_total_percentage_fiscalyear = 100
                    income_total_percentage_variation = income_total_last_period != 0 and (100 * income_total_variation / income_total_last_period) or 0
                    
                    expense_total_period = balance_data['total_expense_balances']['period']
                    expense_total_last_period = balance_data['total_expense_balances']['last_period']
                    expense_total_fiscalyear = balance_data['total_expense_balances']['fiscal_year']
                    expense_total_variation = expense_total_period - expense_total_last_period
                    expense_total_percentage_period = income_total_period != 0 and (100 * expense_total_period / income_total_period) or 0
                    expense_total_percentage_last_period = income_total_last_period != 0 and (100 * expense_total_last_period / income_total_last_period) or 0
                    expense_total_percentage_fiscalyear = income_total_fiscalyear != 0 and (100 * expense_total_fiscalyear / income_total_fiscalyear) or 0
                    expense_total_percentage_variation = income_total_last_period != 0 and (100 * expense_total_variation / income_total_last_period) or 0
                    
                    total_period = income_total_period + expense_total_period
                    total_last_period = income_total_last_period + expense_total_last_period
                    total_fiscalyear = income_total_fiscalyear + expense_total_fiscalyear
                    total_variation = total_period - total_last_period
                    total_percentage_period = income_total_period != 0 and (100 * total_period / income_total_period) or 0
                    total_percentage_last_period = income_total_last_period != 0 and (100 * total_last_period / income_total_last_period) or 0
                    total_percentage_fiscalyear = income_total_fiscalyear != 0 and (100 * total_fiscalyear / income_total_fiscalyear) or 0
                    total_percentage_variation = income_total_last_period != 0 and (100 * total_variation / income_total_last_period) or 0
                %>
                <% row_even = False %>
                %for account in balance_data['income_accounts']:
                    <%
                        account_total_period = balance_data['income_period_balances'][account.id]['balance']
                        account_total_last_period = balance_data['income_last_period_balances'][account.id]['balance']
                        account_total_fiscalyear = balance_data['income_fiscal_year_balances'][account.id]['balance']
                        account_total_variation = account_total_period - account_total_last_period
                        account_total_percentage_period = income_total_period != 0 and (100 * account_total_period / income_total_period) or 0
                        account_total_percentage_last_period = income_total_last_period != 0 and (100 * account_total_last_period / income_total_last_period) or 0
                        account_total_percentage_fiscalyear = income_total_fiscalyear != 0 and (100 * account_total_fiscalyear / income_total_fiscalyear) or 0
                        account_total_percentage_variation = account_total_last_period != 0 and (100 * account_total_variation / account_total_last_period) or 0
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
                        <div class="table-cell amount" >${formatLang(account_total_last_period)}</div>
                        <div class="table-cell amount" >${formatLang(account_total_percentage_last_period)}</div>
                        <div class="table-cell amount" >${formatLang(account_total_period)}</div>
                        <div class="table-cell amount" >${formatLang(account_total_percentage_period)}</div>
                        <div class="table-cell amount" >${formatLang(account_total_variation)}</div>
                        <div class="table-cell amount" >${formatLang(account_total_percentage_variation)}</div>
                        <div class="table-cell amount" >${formatLang(account_total_fiscalyear)}</div>
                        <div class="table-cell amount last-column" >${formatLang(account_total_percentage_fiscalyear)}</div>
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
                    <div class="table-cell">${_('INCOME TOTAL')}</div>
                    <div class="table-cell amount" >${formatLang(income_total_last_period)}</div>
                    <div class="table-cell amount" >${formatLang(income_total_percentage_last_period)}</div>
                    <div class="table-cell amount" >${formatLang(income_total_period)}</div>
                    <div class="table-cell amount" >${formatLang(income_total_percentage_period)}</div>
                    <div class="table-cell amount" >${formatLang(income_total_variation)}</div>
                    <div class="table-cell amount" >${formatLang(income_total_percentage_variation)}</div>
                    <div class="table-cell amount" >${formatLang(income_total_fiscalyear)}</div>
                    <div class="table-cell amount last-column" >${formatLang(income_total_percentage_fiscalyear)}</div>
                </div>
                
                <% row_even = False %>
                %for account in balance_data['expense_accounts']:
                    <%
                        account_total_period = balance_data['expense_period_balances'][account.id]['balance']
                        account_total_last_period = balance_data['expense_last_period_balances'][account.id]['balance']
                        account_total_fiscalyear = balance_data['expense_fiscal_year_balances'][account.id]['balance']
                        account_total_variation = account_total_period - account_total_last_period
                        account_total_percentage_period = income_total_period != 0 and (100 * account_total_period / income_total_period) or 0
                        account_total_percentage_last_period = income_total_last_period != 0 and (100 * account_total_last_period / income_total_last_period) or 0
                        account_total_percentage_fiscalyear = income_total_fiscalyear != 0 and (100 * account_total_fiscalyear / income_total_fiscalyear) or 0
                        account_total_percentage_variation = account_total_last_period != 0 and (100 * account_total_variation / account_total_last_period) or 0
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
                        <div class="table-cell amount" >${formatLang(account_total_last_period)}</div>
                        <div class="table-cell amount" >${formatLang(account_total_percentage_last_period)}</div>
                        <div class="table-cell amount" >${formatLang(account_total_period)}</div>
                        <div class="table-cell amount" >${formatLang(account_total_percentage_period)}</div>
                        <div class="table-cell amount" >${formatLang(account_total_variation)}</div>
                        <div class="table-cell amount" >${formatLang(account_total_percentage_variation)}</div>
                        <div class="table-cell amount" >${formatLang(account_total_fiscalyear)}</div>
                        <div class="table-cell amount last-column" >${formatLang(account_total_percentage_fiscalyear)}</div>
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
                    <div class="table-cell">${_('INCOME TOTAL')}</div>
                    <div class="table-cell amount" >${formatLang(income_total_last_period)}</div>
                    <div class="table-cell amount" >${formatLang(income_total_percentage_last_period)}</div>
                    <div class="table-cell amount" >${formatLang(income_total_period)}</div>
                    <div class="table-cell amount" >${formatLang(income_total_percentage_period)}</div>
                    <div class="table-cell amount" >${formatLang(income_total_variation)}</div>
                    <div class="table-cell amount" >${formatLang(income_total_percentage_variation)}</div>
                    <div class="table-cell amount" >${formatLang(income_total_fiscalyear)}</div>
                    <div class="table-cell amount last-column" >${formatLang(income_total_percentage_fiscalyear)}</div>
                </div>
                <div class="table-row subtotal">
                    <div class="table-cell first-column">&nbsp;</div>
                    <div class="table-cell">${_('EXPENSE TOTAL')}</div>
                    <div class="table-cell amount" >${formatLang(expense_total_last_period)}</div>
                    <div class="table-cell amount" >${formatLang(expense_total_percentage_last_period)}</div>
                    <div class="table-cell amount" >${formatLang(expense_total_period)}</div>
                    <div class="table-cell amount" >${formatLang(expense_total_percentage_period)}</div>
                    <div class="table-cell amount" >${formatLang(expense_total_variation)}</div>
                    <div class="table-cell amount" >${formatLang(expense_total_percentage_variation)}</div>
                    <div class="table-cell amount" >${formatLang(expense_total_fiscalyear)}</div>
                    <div class="table-cell amount last-column" >${formatLang(expense_total_percentage_fiscalyear)}</div>
                </div>
                <div class="table-row total">
                    <div class="table-cell first-column">&nbsp;</div>
                    <div class="table-cell">${_('TOTAL')}</div>
                    <div class="table-cell amount" >${formatLang(total_last_period)}</div>
                    <div class="table-cell amount" >${formatLang(total_percentage_last_period)}</div>
                    <div class="table-cell amount" >${formatLang(total_period)}</div>
                    <div class="table-cell amount" >${formatLang(total_percentage_period)}</div>
                    <div class="table-cell amount" >${formatLang(total_variation)}</div>
                    <div class="table-cell amount" >${formatLang(total_percentage_variation)}</div>
                    <div class="table-cell amount" >${formatLang(total_fiscalyear)}</div>
                    <div class="table-cell amount last-column" >${formatLang(total_percentage_fiscalyear)}</div>
                </div>
            </div>
        </div>
        <p style="page-break-after:always"></p>
    </body>
</html>
