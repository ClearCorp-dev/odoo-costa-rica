<html>
    <head>
        <style type="text/css">
            ${css}

            .list_table .act_as_row {
                margin-top: 10px;
                margin-bottom: 10px;
                font-size:10px;
            }

            .account_line {
                font-weight: bold;
                font-size: 15px;
                background-color:#F0F0F0;
            }
            
            .account_line .act_as_cell {
                height: 30px;
                vertical-align: bottom;
            }

        </style>
    </head>
<body class = "data">
	%for partner in objects :
	<%
	part_by_curr = get_partners_by_curr(cr, uid, partner)
	%>
	<%setLang(user.context_lang)%>
		<%
		total_balance = 0.0
		%>
		<div style="font-size: 20px; font-weight: bold; text-align: center;"> ${company.partner_id.name | entity} - ${company.currency_id.name | entity}</div>
		<div style="font-size: 25px; font-weight: bold; text-align: center;"> Estado de Cuenta</div>
		<div style="font-size: 20px; font-weight: bold; text-align: center;"> ${partner.name}</div>
		 </br></br>
		%for currency in part_by_curr:
		    <%
		    total_debit_curr = 0.0
		    total_credit_curr = 0.0
		    total_balance_curr = 0.0
		    balance_curr = 0.0
		    %>
		    %if currency[0] != None:
                <div class="account_title bg" style="margin-top: 20px; font-size: 12px; width: 1080px;">${_('Estado de Cuenta en ')} ${currency[0]}</div>
		    %else:
                <div class="account_title bg" style="margin-top: 20px; font-size: 12px; width: 1080px;">${_('Estado de Cuenta en ')} ${company.currency_id.name}</div>
		    %endif
		    <div class="act_as_table list_table">
		    <div class="act_as_thead">
			<div class="act_as_row labels" style="font-weight: bold; font-size: 11x;">
			    <div class="act_as_cell first_column" style="vertical-align: middle">${_('Fecha')}</div>
			    <div class="act_as_cell" style="width: 250px;  vertical-align: middle">${_('Detalle')}</div>
			    <div class="act_as_cell">${_('Fecha de Vencimiento')}</div>
			    <div class="act_as_cell amount">${_('Cobros')}</div>
			    <div class="act_as_cell amount">${_('Pagos')}</div>
			</div>
		    </div>
			
			    <div class="act_as_tbody">       
                %for move_line in sorted(currency[1], key=lambda currency: currency.date):
			    <div class="act_as_row lines">           
                              ## Fecha
                              <div class="act_as_cell first_column">${move_line.date or '0'}</div>
                              ## Detalle
                              <div class="act_as_cell">${move_line.name or '-'}</div>
                              ## Fecha de Vencimiento
                              <div class="act_as_cell">${move_line.date_maturity or '-'}</div>
				%if currency[0] != None:
				    %if move_line.amount_currency > 0: 
                        ## Cobros
                        <div class="act_as_cell amount">${formatLang(move_line.amount_currency) or '0'}</div>
                        ## Pagos
                        <div class="act_as_cell amount">${'0.00'}</div>
                        <%total_debit_curr += move_line.amount_currency%>
				    %else:
                        ## Cobros
                        <div class="act_as_cell amount">${'0.00'}</div>
                        ## Pagos
                        <div class="act_as_cell amount">${formatLang(move_line.amount_currency*-1) or '0'}</div>
                        <%total_credit_curr += move_line.amount_currency*-1%>
				    %endif
				%else:
				    ## Pagos
				    <div class="act_as_cell amount">${formatLang(move_line.debit) or '0'}</div>
				    ## Cobros
				    <div class="act_as_cell amount">${formatLang(move_line.credit) or '0'}</div>
				    <%
					## Totales por Moneda
					total_debit_curr += move_line.debit
					total_credit_curr += move_line.credit 
				    %>
				%endif
                    </div>
                %endfor
		</div>
		<%
		    ## Totales
		    total_balance_curr = total_debit_curr - total_credit_curr
		    if currency[0] != None:
                balance_curr = currency_convert(cr, uid, move_line.currency_id.id, company.currency_id.id, total_balance_curr)
		    else:
                balance_curr = total_balance_curr
		    endif

		    total_balance += balance_curr
		%>
		<div class="act_as_tfoot">
		<div class="act_as_row labels"  style="font-weight: bold; font-size: 11px;" >
		    <div class="act_as_cell first_column" style="vertical-align: middle">${_('SALDO')}</div>
		    %if currency[0] != None:
                <div class="act_as_cell" style="width: 250px;  vertical-align: middle">${move_line.currency_id.symbol} ${formatLang(total_balance_curr)}</div>
                <div class="act_as_cell">${_('')}</div>
                <div class="act_as_cell amount">${move_line.currency_id.symbol} ${formatLang(total_debit_curr)}</div>
                <div class="act_as_cell amount">${move_line.currency_id.symbol} ${formatLang(total_credit_curr)}</div>
		    %else:
                <div class="act_as_cell" style="width: 250px;  vertical-align: middle">${company.currency_id.symbol} ${formatLang(total_balance_curr)}</div>
                <div class="act_as_cell">${_('')}</div>
                <div class="act_as_cell amount">${company.currency_id.symbol} ${formatLang(total_debit_curr)}</div>
                <div class="act_as_cell amount">${company.currency_id.symbol} ${formatLang(total_credit_curr)}</div>
		    %endif
		    
		</div>
            </div>
            </div>
                           
         %endfor

	<div class="act_as_table list_table " style="margin-top: 20px;">
	    <div class="act_as_tfoot">
		<div class="act_as_row labels"  style="font-weight: bold; font-size: 11px;">
		    <div class="act_as_cell first_column" style="width: 205px; font-size: 12px; text-align: left">${_('SAlDO TOTAL en ')} ${company.currency_id.name}</div>
		    <div class="act_as_cell" style="text-align: left">${company.currency_id.symbol} ${formatLang(total_balance)}</div>
		</div>
	    </div>
	</div>
	<div>
        <%
            today = get_time_today()
            if currency[0] != None:
                conversion_rate = get_conversion_rate(cr, uid, move_line.currency_id, company.currency_id)
            else:
                from_currency = get_currency(cr, uid, 2)
                conversion_rate = get_conversion_rate(cr, uid, from_currency, company.currency_id)
            endif
        %>
	    <div style="font-family: Helvetica, Arial; font-size: 13px; font-weight: bold; margin-top: 20px;"> ${_('Nota: ')} </div>
        <div style="font-family: Helvetica, Arial; font-size: 12px;"> ${_('En el caso de que hayan monedas extranjeras el Saldo Total se calculó según el cambio de moneda del día ')} ${formatLang( today, date=True)} (${company.currency_id.symbol} ${conversion_rate})</div>
	</div>
	<p style="page-break-after:always"></p>
	
	%endfor
	

</body>
</html>
