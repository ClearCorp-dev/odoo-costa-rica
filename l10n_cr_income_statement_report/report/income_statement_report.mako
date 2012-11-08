<!DOCTYPE html SYSTEM "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
    <head>
        <style type="text/css">
            .overflow_ellipsis {
                text-overflow: ellipsis;
                overflow: hidden;
                white-space: nowrap;
            }
            ${css}
        </style>
    </head>
    <body class = "data">
        <%setLang(user.context_lang)%>
        <%
            last_period = get_last_period(cr, uid, start_period)
            fiscalyear = get_fiscalyear(cr, uid, start_period)
            balance_data = get_data(cr, uid, data)
        %>
        <div style="font-size: 20px; font-weight: bold; text-align: center;"> ${company.partner_id.name}</div>
        <div style="font-size: 25px; font-weight: bold; text-align: center;"> ${_('Income Statement Report')}</div>
        <div style="font-size: 16px; font-weight: bold; text-align: center;">${_('Income Statement of:')} ${start_period.name}</div>
        <div class="" style="margin-top: 20px; font-size: 14px; width: 1080px;"></div>
        <div class="act_as_table data_table">
            <div class="act_as_thead">
                <div class="act_as_row labels no_wrap">
                    <div class="act_as_cell first_column" style="width: 500px">${_('Name')}</div>
                    <div class="act_as_cell amount" style="width: 100px">${start_period.name}</div>
                    <div class="act_as_cell amount" style="width: 40px">${_('%')}</div>
                    <div class="act_as_cell amount" style="width: 100px">${last_period.name}</div>
                    <div class="act_as_cell amount" style="width: 40px">${_('%')}</div>
                    <div class="act_as_cell amount" style="width: 100px">${fiscalyear.name}</div>
                    <div class="act_as_cell amount" style="width: 40px">${_('%')}</div>
                    <div class="act_as_cell amount" style="width: 100px">${_('Variation')}</div>
                    <div class="act_as_cell last_column amount" style="width: 40px">${_('%')}</div>
                </div>
            </div>
            <div class="act_as_tbody">
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
                    <div class="act_as_row lines">
                        %if account.level > 0:
                            <div class="act_as_cell" style="padding-left:${account.level*10}px">
                                %if account.child_id:
                                    <div class="act_as_row first_column" ><b>${account.code} ${_(account.name)}</b></div>
                                %else:
                                    <div class="act_as_row first_column" >${account.code} ${_(account.name)}</div>
                                %endif
                            </div>
                        %else:
                            <div class="act_as_cell first_column" ><b>${account.code} ${_(account.name)}</b></div>
                        %endif
                        <div class="act_as_cell amount" >${formatLang(account_total_period)}</div>
                        <div class="act_as_cell amount" >${formatLang(account_total_percentage_period)}</div>
                        <div class="act_as_cell amount" >${formatLang(account_total_last_period)}</div>
                        <div class="act_as_cell amount" >${formatLang(account_total_percentage_last_period)}</div>
                        <div class="act_as_cell amount" >${formatLang(account_total_fiscalyear)}</div>
                        <div class="act_as_cell amount" >${formatLang(account_total_percentage_fiscalyear)}</div>
                        <div class="act_as_cell amount" >${formatLang(account_total_variation)}</div>
                        <div class="act_as_cell amount last_column" >${formatLang(account_total_percentage_variation)}</div>
                    </div>
                %endfor
                        
                <div class="" style="margin-top: 20px; font-size: 14px; width: 1080px;"></div>
                <div class="act_as_row lines">
                    <div class="act_as_cell first_column" ><b>${_('ASSET TOTAL')}</b></div>
                    <div class="act_as_cell amount" >${formatLang(income_total_period)}</div>
                    <div class="act_as_cell amount" >${formatLang(income_total_percentage_period)}</div>
                    <div class="act_as_cell amount" >${formatLang(income_total_last_period)}</div>
                    <div class="act_as_cell amount" >${formatLang(income_total_percentage_last_period)}</div>
                    <div class="act_as_cell amount" >${formatLang(income_total_fiscalyear)}</div>
                    <div class="act_as_cell amount" >${formatLang(income_total_percentage_fiscalyear)}</div>
                    <div class="act_as_cell amount" >${formatLang(income_total_variation)}</div>
                    <div class="act_as_cell amount last_column" >${formatLang(income_total_percentage_variation)}</div>
                </div>
                <div class="" style="margin-top: 20px; font-size: 14px; width: 1080px;"></div>
                
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
                    <div class="act_as_row lines">
                        %if account.level > 0:
                            <div class="act_as_cell" style="padding-left:${account.level*10}px">
                                %if account.child_id:
                                    <div class="act_as_row first_column" ><b>${account.code} ${_(account.name)}</b></div>
                                %else:
                                    <div class="act_as_row first_column" >${account.code} ${_(account.name)}</div>
                                %endif
                            </div>
                        %else:
                            <div class="act_as_cell first_column" ><b>${account.code} ${_(account.name)}</b></div>
                        %endif
                        <div class="act_as_cell amount" >${formatLang(account_total_period)}</div>
                        <div class="act_as_cell amount" >${formatLang(account_total_percentage_period)}</div>
                        <div class="act_as_cell amount" >${formatLang(account_total_last_period)}</div>
                        <div class="act_as_cell amount" >${formatLang(account_total_percentage_last_period)}</div>
                        <div class="act_as_cell amount" >${formatLang(account_total_fiscalyear)}</div>
                        <div class="act_as_cell amount" >${formatLang(account_total_percentage_fiscalyear)}</div>
                        <div class="act_as_cell amount" >${formatLang(account_total_variation)}</div>
                        <div class="act_as_cell amount last_column" >${formatLang(account_total_percentage_variation)}</div>
                    </div>
                %endfor
                        
                <div class="" style="margin-top: 20px; font-size: 14px; width: 1080px;"></div>
                <div class="act_as_row lines">
                    <div class="act_as_cell first_column" ><b>${_('ASSET TOTAL')}</b></div>
                    <div class="act_as_cell amount" >${formatLang(income_total_period)}</div>
                    <div class="act_as_cell amount" >${formatLang(income_total_percentage_period)}</div>
                    <div class="act_as_cell amount" >${formatLang(income_total_last_period)}</div>
                    <div class="act_as_cell amount" >${formatLang(income_total_percentage_last_period)}</div>
                    <div class="act_as_cell amount" >${formatLang(income_total_fiscalyear)}</div>
                    <div class="act_as_cell amount" >${formatLang(income_total_percentage_fiscalyear)}</div>
                    <div class="act_as_cell amount" >${formatLang(income_total_variation)}</div>
                    <div class="act_as_cell amount last_column" >${formatLang(income_total_percentage_variation)}</div>
                </div>
                <div class="act_as_row lines">
                    <div class="act_as_cell first_column" ><b>${_('EXPENSE TOTAL')}</b></div>
                    <div class="act_as_cell amount" >${formatLang(expense_total_period)}</div>
                    <div class="act_as_cell amount" >${formatLang(expense_total_percentage_period)}</div>
                    <div class="act_as_cell amount" >${formatLang(expense_total_last_period)}</div>
                    <div class="act_as_cell amount" >${formatLang(expense_total_percentage_last_period)}</div>
                    <div class="act_as_cell amount" >${formatLang(expense_total_fiscalyear)}</div>
                    <div class="act_as_cell amount" >${formatLang(expense_total_percentage_fiscalyear)}</div>
                    <div class="act_as_cell amount" >${formatLang(expense_total_variation)}</div>
                    <div class="act_as_cell amount last_column" >${formatLang(expense_total_percentage_variation)}</div>
                </div>
                <div class="" style="margin-top: 20px; font-size: 14px; width: 1080px;"></div>
                <div class="" style="margin-top: 20px; font-size: 14px; width: 1080px;"></div>
                <div class="act_as_row lines">
                    <div class="act_as_cell first_column" ><b>${_('TOTAL')}</b></div>
                    <div class="act_as_cell amount" >${formatLang(total_period)}</div>
                    <div class="act_as_cell amount" >${formatLang(total_percentage_period)}</div>
                    <div class="act_as_cell amount" >${formatLang(total_last_period)}</div>
                    <div class="act_as_cell amount" >${formatLang(total_percentage_last_period)}</div>
                    <div class="act_as_cell amount" >${formatLang(total_fiscalyear)}</div>
                    <div class="act_as_cell amount" >${formatLang(total_percentage_fiscalyear)}</div>
                    <div class="act_as_cell amount" >${formatLang(total_variation)}</div>
                    <div class="act_as_cell amount last_column" >${formatLang(total_percentage_variation)}</div>
                </div>
            </div>
        </div>
        <p style="page-break-after:always"></p>
    </body>
</html>
