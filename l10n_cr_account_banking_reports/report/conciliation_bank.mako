<html>
<head>
    <style type="text/css">${css}</style>
</head>
<body>
    <%setLang(user.context_lang)%>
    <%
        filter_type = ''
        filter_data = []
        bank_account = get_bank_account(cr, uid, data)
    %>

    <div class="header">
        <div style="font-size: 20px; font-weight: bold; text-align: center;"> ${company.partner_id.name | entity} - ${company.currency_id.name | entity}</div>
        <div style="font-size: 25px; font-weight: bold; text-align: center;"> Conciliación de Bancos</div>
        <div style="font-size: 20px; font-weight: bold; text-align: center;"> ${bank_account.name} - ${(bank_account.currency_id and bank_account.currency_id.name) or bank_account.company_id.currency_id.name}</div>
    </div>
    <div class="act_as_table data_table" style="margin-top:10px;">
        <div class="act_as_row labels" style = "font-size: 12px;">
            <div class="act_as_cell">${_('Chart of Account')}</div>
            <div class="act_as_cell">${_('Fiscal Year')}</div>
            <div class="act_as_cell">
                %if filter_form(data) == 'filter_date':
                    ${_('Dates Filter')}
                    <%
                        filter_data.append(start_date)
                        filter_data.append(stop_date)
                        filter_type = 'filter_date'
                    %>
                %elif filter_form(data) == 'filter_period':
                    ${_('Periods Filter')}
                    <% 
                        filter_data.append(start_period)
                        filter_data.append(stop_period)
                        filter_type = 'filter_period'
                    %>
                %else:
                    ${_('No Filter')}
                %endif
            </div>
            <div class="act_as_cell">${_('Target Moves')}</div>
        </div>
        <div class="act_as_row" style = "font-size: 12px;">
            <div class="act_as_cell">${ chart_account.name }</div>
            <div class="act_as_cell">${ fiscalyear.name if fiscalyear else '-' }</div>
            <div class="act_as_cell">
                ${_('To:')}
                %if filter_form(data) == 'filter_date':
                    ${ formatLang(stop_date, date=True) if stop_date else u'' }
                %elif filter_form(data) == 'filter_period':
                    ${stop_period.name if stop_period else u'' }
                %else:
                    ${''}
                %endif
            </div>
            <div class="act_as_cell">${ display_target_move(data) }</div>
        </div>
    </div>
    
    <%
        bank_balance, bank_move_lines, account_is_foreign = get_bank_data(cr, uid, bank_account.id, filter_type, filter_data, fiscalyear, target_move, data['form']['historic_strict'], data['form']['special_period'])
    %>
    <div align="center">
        <div class="act_as_table data_table no_wrap results left" style="margin-top:20px; margin-bottom: 10px; width:500px">
            <div class="act_as_row">
                <div class="act_as_cell" style="border-left:0px; border-right:0px; border-top:0px"></div>
                <div class="act_as_cell" style="column-span:2; -webkit-column-span:2; border-left:0px; border-top:0px"></div>
                <div class="act_as_cell label">${_('Balance according Bank')}</div>
                <div class="act_as_cell amount">
                    %if bank_balance['input_bank_balance'] == bank_balance['bank_balance']:
                        ${formatLang(input_bank_balance)}
                    %else:
                        <span style="color:red; font-weight:bold;">${formatLang(input_bank_balance)}</span>
                    %endif
                </div>
            </div>
            <div class="act_as_row">
                <div class="act_as_cell label">${_('Ledger Balance')}</div>
                <div class="act_as_cell label amount">${formatLang(bank_balance['accounting_balance'])}</div>
                <div class="act_as_cell label">${_('Bank Balance')}</div>
                <div class="act_as_cell label amount">${formatLang(bank_balance['bank_balance'])}</div>
            </div>
            <div class="act_as_row">
                <div class="act_as_cell">${_('+ Incomes to register')}</div>
                <div class="act_as_cell amount">${formatLang(bank_balance['incomes_to_register'])}</div>
                <div class="act_as_cell">${_('+ Credits to reconcile')}</div>
                <div class="act_as_cell amount">${formatLang(bank_balance['credits_to_reconcile'])}</div>
            </div>
            <div class="act_as_row">
                <div class="act_as_cell">${_('- Expenditures to register')}</div>
                <div class="act_as_cell amount">${formatLang(bank_balance['expenditures_to_register'])}</div>
                <div class="act_as_cell">${_('- Debits to reconcile')}</div>
                <div class="act_as_cell amount">${formatLang(bank_balance['debits_to_reconcile'])}</div>
            </div>
            <div class="act_as_row">
                <div class="act_as_cell label">${_('Ledger reconciled Total')}</div>
                <div class="act_as_cell label amount">${formatLang(bank_balance['accounting_total'])}</div>
                <div class="act_as_cell label">${_('Bank reconciled Total')}</div>
                <div class="act_as_cell label amount">${formatLang(bank_balance['bank_total'])}</div>
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
        <div class="account_title bg" style="width: 100%; margin-top: 15px; font-size: 12px;">
            %if line_group_key == 'credits_to_reconcile':
                ${_('Credits to reconcile')}
            %elif line_group_key == 'debits_to_reconcile':
                ${_('Debits to reconcile')}
            %elif line_group_key == 'incomes_to_register':
                ${_('Incomes to register')}
            %else:
                ${_('Expenditures to register')}
            %endif
        </div>
        <div class="act_as_table list_table" style="margin-top: 5px;">
            <div class="act_as_thead">
                <div class="act_as_row labels no_wrap">
                    ## date
                    <div class="act_as_cell first_column">${_('Date')}</div>
                    ## period
                    <div class="act_as_cell">${_('Period')}</div>
                    ## journal
                    <div class="act_as_cell">${_('Journal')}</div>
                    ## Account
                    <div class="act_as_cell">${_('Account')}</div>
                    ## Partner
                    <div class="act_as_cell" style="width: 40%;">${_('Partner')}</div>
                    ## Reference
                    <div class="act_as_cell" style="width: 20%;">${_('Reference')}</div>
                    ## label
                    <div class="act_as_cell" style="width: 40%;">${_('Label')}</div>
                     ## Amount
                    <div class="act_as_cell last_column amount">${_('Amount')}</div>
                </div>
            </div>
            <div class="act_as_tbody">\
                %for line in line_group:
                    <div class="act_as_row lines">
                        ## date
                        <div class="act_as_cell first_column no_wrap">${formatLang(line.date, date=True)}</div>
                        ## period
                        <div class="act_as_cell no_wrap">${line.period_id.code}</div>
                        ## journal
                        <div class="act_as_cell no_wrap">${line.journal_id.code}</div>
                        ## Account
                        <div class="act_as_cell no_wrap">${line.account_id.code}</div>
                        ## Partner
                        <div class="act_as_cell">
                            %if line.partner_id:
                                ${(line.partner_id.ref and line.partner_id.ref + ' ') or ''}
                                ${(line.partner_id.name and line.partner_id.name) or ''}
                            %else:
                                ${_('-- No partner --')}
                            %endif
                        </div>
                        ## Reference
                        <div class="act_as_cell">${line.ref}</div>
                        ## label
                        <div class="act_as_cell">${line.name}</div>
                        ## Amount
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
        <div class="act_as_table list_table" style="margin-top:5px;">
            <div class="act_as_row labels" style="font-weight: bold; font-size: 12px;">
                ## label
                <div class="act_as_cell" style="width: 880px;">
                    %if line_group_key == 'credits_to_reconcile':
                        ${_("Total")} ${_('Credits to reconcile')}
                    %elif line_group_key == 'debits_to_reconcile':
                        ${_("Total")} ${_('Debits to reconcile')}
                    %elif line_group_key == 'incomes_to_register':
                        ${_("Total")} ${_('Incomes to register')}
                    %else:
                        ${_("Total")} ${_('Expenditures to register')}
                    %endif
                </div>
                <div class="act_as_cell amount" style="width: 200px;">
                    %if account_is_foreign:
                        ${bank_account.currency_id.symbol} ${formatLang(bank_balance[line_group_key])}
                    %else:
                        ${company.currency_id.symbol} ${formatLang(bank_balance[line_group_key])}
                    %endif
                </div>
            </div>
        </div>
    %endfor
</body>
</html>
