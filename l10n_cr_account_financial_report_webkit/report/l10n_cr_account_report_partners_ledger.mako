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
<body>
    <%!
        def amount(text):
            return text.replace('-', '&#8209;')  # replace by a non-breaking hyphen (it will not word-wrap between hyphen and numbers)
    %>
    <%
        setLang(user.context_lang)

        initial_balance_text = {'initial_balance': _('Computed'), 'opening_balance': _('Opening Entries'), False: _('No')}
        filter_type = ''
        filter_data = []
    %>

    <div class="act_as_table data_table">
        <div class="act_as_row labels">
            <div class="act_as_cell">${_('Chart of Account')}</div>
            <div class="act_as_cell">${_('Fiscal Year')}</div>
            <div class="act_as_cell">
                %if filter_form(data) == 'filter_date':
                    ${_('Dates Filter')}
                %else:
                    ${_('Periods Filter')}
                %endif
            </div>
            <div class="act_as_cell">${_('Accounts Filter')}</div>
            <div class="act_as_cell">${_('Target Moves')}</div>
            <div class="act_as_cell">${_('Initial Balance')}</div>
        </div>
        <div class="act_as_row">
            <div class="act_as_cell">${ chart_account.name }</div>
            <div class="act_as_cell">${ fiscalyear.name if fiscalyear else '-' }</div>
            <div class="act_as_cell">
                ${_('From:')}
                %if filter_form(data) == 'filter_date':
                    ${formatLang(start_date, date=True) if start_date else u'' }
                    <%
                        filter_data.append(start_date)
                        filter_type = 'filter_date'
                    %>
                %else:
                    ${start_period.name if start_period else u''}
                    <% 
                        filter_data.append(start_period)
                        filter_type = 'filter_period'
                    %>
                %endif
                ${_('To:')}
                %if filter_form(data) == 'filter_date':
                    ${ formatLang(stop_date, date=True) if stop_date else u'' }
                    <% filter_data.append(stop_date) %>
                %else:
                    ${stop_period.name if stop_period else u'' }
                    <% filter_data.append(stop_period) %>
                %endif
            </div>
            <div class="act_as_cell">
                %if partner_ids:
                    ${_('Custom Filter')}
                %else:
                    ${ display_partner_account(data) }
                %endif
            </div>
            <div class="act_as_cell">${ display_target_move(data) }</div>
            <div class="act_as_cell">${ initial_balance_text[initial_balance_mode] }</div>
        </div>
    </div>
    <%
    account_by_curr = get_accounts_by_curr(cr, uid, objects)
    %>
    %for currency in account_by_curr:
		%if currency[0] != 'CRC':
			<%currency_symbol = get_currency_symbol(cr, uid, currency[0]) %>
		%endif
        <%
            currency_total_invoice = 0.0
            currency_total_payment = 0.0
            currency_total_debit = 0.0
            currency_total_credit = 0.0
            currency_total_manual_move = 0.0
            currency_balance_accumulated = 0.0
        %>

        <div class="account_title bg" style="margin-top: 20px; font-size: 14px; width: 100%;">${_('Accounts in ')} ${currency[0]}</div>

        %for account in currency[1]:
            %if account.ledger_lines or account.init_balance:
                <%
                    if not account.partners_order:
                        continue
                    account_total_invoice = 0.0
                    account_total_payment = 0.0
                    account_total_debit = 0.0
                    account_total_credit = 0.0
                    account_total_manual_move = 0.0
                    account_balance_accumulated = 0.0
                    account_balance_accumulated_curr = 0.0
                %>

                <div class="account_title bg" style="width: 100%; margin-top: 15px; font-size: 12px;">${account.code} - ${account.name} - ${account.report_currency_id.name or account.company_id.currency_id.name}</div>

                %for partner_name, p_id, p_ref, p_name in account.partners_order:
                <%
                    total_invoice = 0.0
                    total_payment = 0.0
                    total_debit = 0.0
                    total_credit = 0.0
                    total_manual_move = 0.0
                    accumulated_balance = 0.0
                    accumulated_balance_curr = 0.0
                    total_accumulated_balance = 0.0

                    partner_accumulated_balance = 0.0
                    partner_accumulated_balance_curr = 0.0 

                    partner_accumulated_balance = account.init_balance.get(p_id, {}).get('init_balance') or 0.0
                    init_balance = 0.0
                    init_balance = get_initial_balance(cr, uid, p_id, account, filter_type, filter_data, fiscal_year, currency[0])
                    accumulated_balance = init_balance
                %>
                <div class="act_as_table list_table" style="margin-top: 5px;">
                    <div class="act_as_caption account_title">
                        ${ get_partner_name(cr, uid, partner_name, p_id, p_ref, p_name)  or _('No Partner')}
                    </div>
                    <div class="act_as_thead">
                        <div class="act_as_row labels">
                            ## date
                            <div class="act_as_cell first_column" style="width: 50px;">${_('Date')}</div>
                            ## period
                            <div class="act_as_cell" style="width: 70px;">${_('Period')}</div>
                            ## move
                            <div class="act_as_cell" style="width: 70px;">${_('Entry')}</div>
                            ## journal
                            <div class="act_as_cell" style="width: 70px;">${_('Journal')}</div>
                            ## partner
                            <!--div class="act_as_cell" style="width: 60px;">${_('Partner')}</div-->
                            ## label
                            <div class="act_as_cell" style="width: 270px;">${_('Label')}</div>
                            ## reconcile
                            <div class="act_as_cell" style="width: 70px;">${_('Rec.')}</div>
                             ## Invoices
                            <div class="act_as_cell amount" style="width: 100px;">${_('Invoice')}</div>
                            ## credit
                            <div class="act_as_cell amount" style="width: 100px;">${_('Payments')}</div>
                            ## debit
                            <div class="act_as_cell amount" style="width: 100px;">${_('Credit')}</div>
                            ## Payments
                            <div class="act_as_cell amount" style="width: 100px;">${_('Debit')}</div>
                            ## Manual Move
                            <div class="act_as_cell amount" style="width: 115px;">${_('Manual Move')}</div>
                            ## balance cumulated
                            <div class="act_as_cell amount" style="width: 115px;">${_('Cumul. Bal.')}</div>
                            %if amount_currency(data):
                                ## currency balance
                                <div class="act_as_cell amount sep_left" style="width: 80px;">${_('Curr. Balance')}</div>
                                ## curency code
                                <div class="act_as_cell amount" style="width: 30px; text-align: right;">${_('Curr.')}</div>
                            %endif
                        </div>
                    </div>
                    <div class="act_as_tbody">
                          %if initial_balance_mode and (total_debit or total_credit):
                            <%
                              #partner_accumulated_balance = account.init_balance.get(p_id, {}).get('init_balance') or 0.0
                              #partner_accumulated_balance_curr = account.init_balance.get(p_id, {}).get('init_balance_currency') or 0.0
                              #balance_forward_currency = account.init_balance.get(p_id, {}).get('currency_name') or ''

                              #accumulated_balance += partner_accumulated_balance
                              #accumulated_balance_curr += partner_accumulated_balance_curr
                            %>
                          %endif
                        <div class="act_as_cell first_column" style="width: 50px;">${_('')}</div>
                        ## period
                        <div class="act_as_cell" style="width: 70px;">${_('')}</div>
                        ## move
                        <div class="act_as_cell" style="width: 70px;">${_('')}</div>
                        ## journal
                        <div class="act_as_cell" style="width: 70px;">${_('')}</div>
                        <div class="act_as_cell" style="width: 270px;">${_('Initial Balance')}</div>
                        <div class="act_as_cell" style="width: 70px;">${_('')}</div>
                        <div class="act_as_cell amount" style="width: 100px;">${_('')}</div>
                        <div class="act_as_cell amount" style="width: 100px;">${_('')}</div>
                        <div class="act_as_cell amount" style="width: 100px;">${_('')}</div>
                        <div class="act_as_cell amount" style="width: 100px;">${_('')}</div>
                        <div class="act_as_cell amount" style="width: 115px;">${_('')}</div>
                        <div class="act_as_cell amount" style="width: 115px;">${formatLang(init_balance)}</div>
                        
                        <%total_accumulated_balance = init_balance %>
                        
                        %for line in account.ledger_lines.get(p_id, []):
                          <%
                              label_elements = [line.get('lname') or '']
                              if line.get('invoice_number'):
                                label_elements.append("(%s)" % (line['invoice_number'],))
                              label = ' '.join(label_elements)

                              invoice_amount = 0.0
                              payment_amount = 0.0
                              credit_amount = 0.0
                              debit_amount = 0.0
                              MM_amount = 0.0

                              amount = get_amount(cr, uid, line, currency[0])
                          %>
                          <div class="act_as_row lines">
                              ## date
                              <div class="act_as_cell first_column">${formatLang(line.get('ldate') or '', date=True)}</div>
                              ## period
                              <div class="act_as_cell">${line.get('period_code') or ''}</div>
                              ## move
                              <div class="act_as_cell">${line.get('move_name') or ''}</div>
                              ## journal
                              <div class="act_as_cell">${line.get('jcode') or ''}</div>
                              ## partner
                              <!--div class="act_as_cell overflow_ellipsis">${line.get('partner_name') or ''}</div-->
                              ## label
                              <div class="act_as_cell">${label}</div>
                              ## reconcile
                              <div class="act_as_cell">${line.get('rec_name') or ''}</div>
                              ## Invoice
                              <div class="act_as_cell amount">
                              %if amount[0] == 'invoice':
                                <%
                                invoice_amount = amount[1]
                                total_invoice += invoice_amount
                                %>
                                ${ formatLang(invoice_amount or 0.0) }
                              %else:
                                ${'0.0'}
                              %endif
                              %if amount[2] != None and amount[0] == 'invoice':
                                ${' ('}${ formatLang(amount[2]) }${')'}
                              %endif
                              </div>
                              ## Payment
                              <div class="act_as_cell amount">
                              %if amount[0] == 'payment':
                                <%
                                payment_amount = amount[1]
                                total_payment += payment_amount
                                %>
                                ${ formatLang(payment_amount or 0.0) }
                              %else:
                                ${'0.0'}
                              %endif
                              %if amount[2] != None and amount[0] == 'payment':
                                ${' ('}${ formatLang(amount[2]) }${')'}
                              %endif
                              </div>
                              ## Credit
                              <div class="act_as_cell amount">
                              %if amount[0] == 'credit':
                                <%
                                credit_amount = amount[1]
                                total_credit += credit_amount
                                %>
                                ${ formatLang(credit_amount or 0.0) }
                              %else:
                                ${'0.0'}
                              %endif
                              %if amount[2] != None and amount[0] == 'credit':
                                ${' ('}${ formatLang(amount[2]) }${')'}
                              %endif
                              </div>
                              ## Debit
                              <div class="act_as_cell amount">
                              %if amount[0] == 'debit':
                                <%
                                debit_amount = amount[1]
                                total_debit += debit_amount
                                %>
                                ${ formatLang(debit_amount or 0.0) }
                              %else:
                                ${'0.0'}
                              %endif
                              %if amount[2] != None and amount[0] == 'debit':
                                ${' ('}${ formatLang(amount[2]) }${')'}
                              %endif
                              </div>
                              ## Manual move
                              <div class="act_as_cell amount">
                              %if amount[0] == 'manual':
                                <%
                                MM_amount = amount[1]
                                total_manual_move += MM_amount
                                %>
                                ${ formatLang(MM_amount or 0.0) }
                              %else:
                                ${'0.0'}
                              %endif
                              %if amount[2] != None and amount[0] == 'manual':
                                ${' ('}${ formatLang(amount[2]) }${')'}
                              %endif
                              </div>
                              ## balance cumulated
                              <% 
                                accumulated_balance = (invoice_amount+payment_amount+credit_amount+debit_amount+MM_amount) or 0.0
                                total_accumulated_balance += accumulated_balance 
                              %>
                              <div class="act_as_cell amount" style="padding-right: 1px;">${formatLang(total_accumulated_balance) }</div>
                              %if amount_currency(data):
                                  ## currency balance
                                  <div class="act_as_cell sep_left amount">${formatLang(line.get('amount_currency') or 0.0) }</div>
                                  ## curency code
                                  <div class="act_as_cell" style="text-align: right; ">${line.get('currency_code') or ''}</div>
                              %endif
                        </div>
                        %endfor
                        <div class="act_as_row lines labels">
                          ## date
                          <div class="act_as_cell first_column"></div>
                          ## period
                          <div class="act_as_cell"></div>
                          ## move
                          <div class="act_as_cell"></div>
                          ## journal
                          <div class="act_as_cell"></div>
                          ## partner
                          <div class="act_as_cell"></div>
                          ## label
                          <div class="act_as_cell">${_('Saldo')}</div>
                          ## reconcile
                          <!--div class="act_as_cell"></div-->
                          %if currency[0] != 'CRC':
                               ## invoice
                              <div class="act_as_cell amount">${currency_symbol} ${formatLang(total_invoice) }</div>
                              ## payment
                              <div class="act_as_cell amount">${currency_symbol} ${formatLang(total_payment) }</div>
                              ## credit
                              <div class="act_as_cell amount">${currency_symbol} ${formatLang(total_credit) }</div>
                              ## debit
                              <div class="act_as_cell amount">${currency_symbol} ${formatLang(total_debit) }</div>
                              ## manual move
                              <div class="act_as_cell amount">${currency_symbol} ${formatLang(total_manual_move) }</div>
                              ## balance cumulated
                              <div class="act_as_cell amount" style="padding-right: 1px;">${currency_symbol} ${formatLang(total_accumulated_balance) }</div>
                          %else:
                              ## invoice
                              <div class="act_as_cell amount">${company.currency_id.symbol} ${formatLang(total_invoice) }</div>
                              ## payment
                              <div class="act_as_cell amount">${company.currency_id.symbol} ${formatLang(total_payment) }</div>
                              ## credit
                              <div class="act_as_cell amount">${company.currency_id.symbol} ${formatLang(total_credit) }</div>
                              ## debit
                              <div class="act_as_cell amount">${company.currency_id.symbol} ${formatLang(total_debit) }</div>
                              ## manual move
                              <div class="act_as_cell amount">${company.currency_id.symbol} ${formatLang(total_manual_move) }</div>
                              ## balance cumulated
                              <div class="act_as_cell amount" style="padding-right: 1px;">${company.currency_id.symbol} ${formatLang(total_accumulated_balance) }</div>
                          %endif
                          %if amount_currency(data):
                              ## currency balance
                              %if account.report_currency_id:
                                  <!--div class="act_as_cell amount sep_left">${formatLang(accumulated_balance_curr) | amount }</div-->
                              %else:
                                  <div class="act_as_cell sep_left amount">${ u'-' }</div>
                              %endif
                              ## currency code
                              <div class="act_as_cell" style="text-align: right; padding-right: 1px;">${ account.report_currency_id.name if account.report_currency_id else u'' }</div>
                          %endif
                      </div>
                    </div>
                </div>
                <%
                    account_total_invoice += total_invoice
                    account_total_payment += total_payment
                    account_total_debit += total_debit
                    account_total_credit += total_credit
                    account_total_manual_move += total_manual_move
                    account_balance_accumulated +=  total_accumulated_balance
                    account_balance_accumulated_curr += account_balance_accumulated
                    
                    currency_total_invoice += total_invoice
                    currency_total_payment += total_payment
                    currency_total_debit += total_debit
                    currency_total_credit += total_credit
                    currency_total_manual_move += total_manual_move
                    currency_balance_accumulated +=  total_accumulated_balance
                %>
                %endfor

                    <div class="act_as_table list_table" style="margin-top:5px;">
                        <div class="act_as_row labels" style="font-weight: bold; font-size: 12px;">
                            <div class="act_as_cell first_column" style="width: 300px;">${account.code} - ${account.name}</div>
                            ## label
                            <div class="act_as_cell" style="width: 302px;">${_("Saldo")}</div>
                            %if currency[0] != 'CRC':
                                ## invoice
                                <div class="act_as_cell amount" style="width: 100px;">${currency_symbol} ${ formatLang(account_total_invoice) }</div>
                                ## payment
                                <div class="act_as_cell amount" style="width: 100px;">${currency_symbol} ${ formatLang(account_total_payment) }</div>
                                ## credit
                                <div class="act_as_cell amount" style="width: 100px;">${currency_symbol} ${ formatLang(account_total_credit) }</div>
                                ## debit
                                <div class="act_as_cell amount" style="width: 100px;">${currency_symbol} ${ formatLang(account_total_debit) }</div>
                                ## manual move
                                <div class="act_as_cell amount" style="width: 115px;">${currency_symbol} ${ formatLang(account_total_manual_move) }</div>
                                ## balance cumulated
                                <div class="act_as_cell amount" style="width: 115px; padding-right: 1px;">${currency_symbol} ${ formatLang(account_balance_accumulated) }</div>
                            %else:
                                ## invoice
                                <div class="act_as_cell amount" style="width: 100px;">${company.currency_id.symbol} ${ formatLang(account_total_invoice) }</div>
                                ## payment
                                <div class="act_as_cell amount" style="width: 100px;">${company.currency_id.symbol} ${ formatLang(account_total_payment) }</div>
                                ## credit
                                <div class="act_as_cell amount" style="width: 100px;">${company.currency_id.symbol} ${ formatLang(account_total_credit) }</div>
                                ## debit
                                <div class="act_as_cell amount" style="width: 100px;">${company.currency_id.symbol} ${ formatLang(account_total_debit) }</div>
                                ## manual move
                                <div class="act_as_cell amount" style="width: 115px;">${company.currency_id.symbol} ${ formatLang(account_total_manual_move) }</div>
                                ## balance cumulated
                                <div class="act_as_cell amount" style="width: 115px; padding-right: 1px;">${company.currency_id.symbol} ${ formatLang(account_balance_accumulated) }</div>
                            %endif
                            %if amount_currency(data):
                                ## currency balance
                                %if account.report_currency_id:
                                    <!--div class="act_as_cell amount sep_left" style="width: 80px;">${ formatLang(account_balance_accumulated_curr) | amount }</div-->
                                %else:
                                    <div class="act_as_cell amount sep_left" style="width: 80px;">${ u'-' }</div>
                                %endif
                                ## curency code
                                <div class="act_as_cell amount" style="width: 30px; text-align: right; padding-right: 1px;">${ account.report_currency_id.name if account.report_currency_id else u'' }</div>
                            %endif
                        </div>
                    </div>
                </div>
            %endif
        %endfor
        <div class="act_as_table list_table" style="margin-top:5px;">
            <div class="act_as_row labels" style="font-weight: bold; font-size: 12px;">
                %if currency[0] != 'CRC':
                    <div class="act_as_cell first_column" style="width: 300px;">${_('Total for Accounts in ')} ${currency[0]}</div>
                %else:
                    <div class="act_as_cell first_column" style="width: 300px;">${_('Total for Accounts in ')} ${company.currency_id.name}</div>
                %endif
                ## label
                <div class="act_as_cell" style="width: 302px;"></div>
                %if currency[0] != 'CRC':
                    ## invoice
                    <div class="act_as_cell amount" style="width: 100px;">${currency_symbol} ${ formatLang(currency_total_invoice) }</div>
                    ## payment
                    <div class="act_as_cell amount" style="width: 100px;">${currency_symbol} ${ formatLang(currency_total_payment) }</div>
                    ## credit
                    <div class="act_as_cell amount" style="width: 100px;">${currency_symbol} ${ formatLang(currency_total_credit) }</div>
                    ## debit
                    <div class="act_as_cell amount" style="width: 100px;">${currency_symbol} ${ formatLang(currency_total_debit) }</div>
                    ## manual move
                    <div class="act_as_cell amount" style="width: 115px;">${currency_symbol} ${ formatLang(currency_total_manual_move) }</div>
                    ## balance cumulated
                    <div class="act_as_cell amount" style="width: 115px; padding-right: 1px;">${currency_symbol} ${ formatLang(currency_balance_accumulated) }</div>
                %else:
                    ## invoice
                    <div class="act_as_cell amount" style="width: 100px;">${company.currency_id.symbol} ${ formatLang(currency_total_invoice) }</div>
                    ## payment
                    <div class="act_as_cell amount" style="width: 100px;">${company.currency_id.symbol} ${ formatLang(currency_total_payment) }</div>
                    ## credit
                    <div class="act_as_cell amount" style="width: 100px;">${company.currency_id.symbol} ${ formatLang(currency_total_credit) }</div>
                    ## debit
                    <div class="act_as_cell amount" style="width: 100px;">${company.currency_id.symbol} ${ formatLang(currency_total_debit) }</div>
                    ## manual move
                    <div class="act_as_cell amount" style="width: 115px;">${company.currency_id.symbol} ${ formatLang(currency_total_manual_move) }</div>
                    ## balance cumulated
                    <div class="act_as_cell amount" style="width: 115px; padding-right: 1px;">${company.currency_id.symbol} ${ formatLang(currency_balance_accumulated) }</div>
                %endif
            </div>
        </div>
    %endfor
</body>
</html>
