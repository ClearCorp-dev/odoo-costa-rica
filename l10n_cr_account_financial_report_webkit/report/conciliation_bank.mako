<html>
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
<body>
    <% prueba = get_prueba(cr, uid)%>
    <%setLang(user.context_lang)%>
    <%
        input_bank_balance = get_bank_balance(cr, uid, data)
        bank_account = get_bank_account(cr, uid, data)
    %>
    <%
        bank_balance, bank_move_lines, account_is_foreign = get_bank_data(cr, uid, bank_account.id, context)
    %>

    <div style="font-size: 20px; font-weight: bold; text-align: center;"> ${company.partner_id.name | entity} - ${company.currency_id.name | entity}</div>
    <div style="font-size: 25px; font-weight: bold; text-align: center;"> Conciliación de Bancos</div>
    <div style="font-size: 20px; font-weight: bold; text-align: center;"> ${bank_account.name}</div>
    <div align="center">
        <div class="act_as_table data_table" style="margin-top:20px; margin-bottom: 10px; width:500px">
            <div class="act_as_row labels">
                <div class="act_as_cell" style = "width: 150px; text-align: left"></div>
                <div class="act_as_cell amount" style="width: 120px"></div>
                <div class="act_as_cell" style = "width: 150px; font-size: 14px; font-weight: bold; text-align: left">${_('Input Bank Balance')}</div>
                <div class="act_as_cell amount" style = "width: 120px; font-size: 14px; font-weight: bold">${formatLang(bank_balance['input_bank_balance'])}</div>
            </div>
            <div class="act_as_row labels">
                <div class="act_as_cell" style = "font-size: 14px; font-weight: bold; text-align: left">${_('Accounting Balance')}</div>
                <div class="act_as_cell amount" style = "font-size: 14px; font-weight: bold">${formatLang(bank_balance['accounting_balance'])}</div>
                <div class="act_as_cell" style = "font-size: 14px; font-weight: bold; text-align: left">${_('Bank Balance')}</div>
                <div class="act_as_cell amount" style = "font-size: 14px; font-weight: bold">${formatLang(bank_balance['bank_balance'])}</div>
            </div>
            <div class="act_as_row labels">
                <div class="act_as_cell" style = "font-size: 14px; text-align: left">${_('Debits to register')}</div>
                <div class="act_as_cell amount" style = "font-size: 14px">${formatLang(bank_balance['debits_to_register'])}</div>
                <div class="act_as_cell" style = "font-size: 14px; text-align: left">${_('Debits to reconcile')}</div>
                <div class="act_as_cell amount" style = "font-size: 14px">${formatLang(bank_balance['debits_to_reconcile'])}</div>
            </div>
            <div class="act_as_row labels">
                <div class="act_as_cell" style = "font-size: 14px; text-align: left">${_('Credits to register')}</div>
                <div class="act_as_cell amount" style = "font-size: 14px">${formatLang(bank_balance['credits_to_register'])}</div>
                <div class="act_as_cell" style = "font-size: 14px; text-align: left">${_('Credits to reconcile')}</div>
                <div class="act_as_cell amount" style = "font-size: 14px">${formatLang(bank_balance['credits_to_reconcile'])}</div>
            </div>
            <div class="act_as_row labels">
                <div class="act_as_cell" style = "font-size: 14px; font-weight: bold; text-align: left; width: 90px;">${_('Accounting Total')}</div>
                <div class="act_as_cell amount" style = "font-size: 14px; font-weight: bold; width: 90px;">${formatLang(bank_balance['accounting_total'])}</div>
                <div class="act_as_cell" style = "font-size: 14px; font-weight: bold; text-align: left; width: 90px;">${_('Bank Total')}</div>
                <div class="act_as_cell amount" style = "font-size: 14px; font-weight: bold; width: 90px;">${formatLang(bank_balance['bank_total'])}</div>
            </div>
        </div>
    </div>

    <%
        def cmp (first, second):
            list_ = [
                'debits_to_register',
                'credits_to_register',
                'debits_to_reconcile',
                'credits_to_reconcile',
            ]
            first_index = len(first) > 0 and first[0] in list_ and list_.index(first[0]) or -1
            second_index = len(second) > 0 and second[0] in list_ and list_.index(second[0]) or -1
            
            return first_index - second_index
    %>
    %for line_group_key, line_group in sorted(bank_move_lines.items(),cmp):
        <div class="account_title bg" style="width: 100%; margin-top: 15px; font-size: 12px;">
            %if line_group_key == 'debits_to_reconcile':
                ${_('Debits to reconcile')}
            %elif line_group_key == 'credits_to_reconcile':
                ${_('Credits to reconcile')}
            %elif line_group_key == 'debits_to_register':
                ${_('Debits to register')}
            %else:
                ${_('Credits to register')}
            %endif
        </div>
        <div class="act_as_table list_table" style="margin-top: 5px;">
            <div class="act_as_thead">
                <div class="act_as_row labels">
                    ## Account
                    <div class="act_as_cell first_column" style="width: 70px;">${_('Account')}</div>
                    ## Partner
                    <div class="act_as_cell" style="width: 310px;">${_('Partner')}</div>
                    ## date
                    <div class="act_as_cell" style="width: 55px;">${_('Date')}</div>
                    ## period
                    <div class="act_as_cell" style="width: 60px;">${_('Period')}</div>
                    ## journal
                    <div class="act_as_cell" style="width: 120px;">${_('Journal')}</div>
                    ## Reference
                    <div class="act_as_cell" style="width: 50px;">${_('Reference')}</div>
                    ## label
                    <div class="act_as_cell" style="width: 315px;">${_('Label')}</div>
                     ## Amount
                    <div class="act_as_cell amount" style="width: 100px;">${_('Amount')}</div>
                </div>
            </div>
            <div class="act_as_tbody">\
                %for line in line_group:
                    <div class="act_as_row lines">
                        ## Account
                        <div class="act_as_cell first_column">${line.account_id.code}</div>
                        ## Partner
                        <div class="act_as_cell">${line.partner_id.ref} ${line.partner_id.name}</div>
                        ## date
                        <div class="act_as_cell">${formatLang(line.date, date=True)}</div>
                        ## period
                        <div class="act_as_cell">${line.period_id.code}</div>
                        ## journal
                        <div class="act_as_cell">${line.journal_id.code}</div>
                        ## Reference
                        <div class="act_as_cell">${line.ref}</div>
                        ## label
                        <div class="act_as_cell">${line.name}</div>
                        ## Amount
                        <div class="act_as_cell amount">
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
                <div class="act_as_table list_table" style="margin-top:5px;">
                    <div class="act_as_row labels" style="font-weight: bold; font-size: 12px;">
                        ## label
                        <div class="act_as_cell" style="width: 880px;">
                            %if line_group_key == 'debits_to_reconcile':
                                ${_("Total")} ${_('Debits to reconcile')}
                            %elif line_group_key == 'credits_to_reconcile':
                                ${_("Total")} ${_('Credits to reconcile')}
                            %elif line_group_key == 'debits_to_register':
                                ${_("Total")} ${_('Debits to register')}
                            %else:
                                ${_("Total")} ${_('Credits to register')}
                            %endif
                        </div>
                        <div class="act_as_cell amount" style="width: 200px;">
                            %if account_is_foreign:
                                ${account.currency_id.symbol} ${formatLang(bank_balance[line_group_key])}
                            %else:
                                ${company.currency_id.symbol} ${formatLang(bank_balance[line_group_key])}
                            %endif
                        </div>
                    </div>
                </div>
            </div>
        </div>
    %endfor
</body>
</html>
