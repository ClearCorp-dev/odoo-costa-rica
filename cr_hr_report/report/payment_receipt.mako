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
	<%
	total_hn = 0.0
	total_he = 0.0
	total_fe = 0.0
	total_basic = 0.0
	total_exs = 0.0
	total_fes = 0.0
	total_gross = 0.0
	total_basic = 0.0
	total_rent = 0.0
	total_ccss = 0.0
	total_net = 0.0
	total_emp = 0
	dep = []
	%>
	%for deparments in objects:
	<%
	    dep.append(deparments)

	%>
	%endfor
	%for payslips in objects :
		<div style="font-size: 20px; font-weight: bold; text-align: center;"> ${company.partner_id.name | entity} - ${company.currency_id.name | entity}</div>
		<div style="font-size: 25px; font-weight: bold; text-align: center;"> Reporte de Planilla</div>
		<div style="font-size: 20px; font-weight: bold; text-align: center;"> ${payslips.name}</div>
		<div style="font-size: 16px; font-weight: bold; text-align: center;">Periodo de ${payslips.date_start} a ${payslips.date_end}</div>
		 </br></br>
		    <div class="act_as_table list_table">
		    <div class="act_as_thead">
			<div class="act_as_row labels" style="font-weight: bold; font-size: 11x;">
			    <div class="act_as_cell first_column" style="width: 85px;  vertical-align: middle">${_('Cedula')}</div>
			    <div class="act_as_cell" style="width: 250px;  vertical-align: middle">${_('Nombre')}</div>
			    <div class="act_as_cell amount" style="width: 40px;">${_('Hrs.')}<br />${_('Nor')}</div>
			    <div class="act_as_cell amount" style="width: 40px;">${_('Hrs.')}<br />${_('Ext')}</div>
			    <div class="act_as_cell amount" style="width: 40px;">${_('Hrs.')}<br />${_('Dob')}</div>
			    <div class="act_as_cell amount">${_('Ingr.')}<br />${_('Normal')}</div>
			    <div class="act_as_cell amount">${_('Ingr.')}<br />${_('Extra')}</div>
			    <div class="act_as_cell amount">${_('Ingr.')}<br />${_('Doble')}</div>
			    <div class="act_as_cell amount">${_('Otros')}<br />${_('Ingr.')}</div>
			    <div class="act_as_cell amount">${_('Salario')}<br />${_('Bruto')}</div>
			    <div class="act_as_cell amount">${_('Deducc.')}<br />${_('CCSS/BP')}</div>
			    <div class="act_as_cell amount">${_('Impuesto')}<br />${_('Renta')}</div>
			    <div class="act_as_cell amount">${_('Otras')}<br />${_('Deducc.')}</div>
			    <div class="act_as_cell amount">${_('Salario')}<br />${_('Neto')}</div>
			</div>
			</div>
			
			    <div class="act_as_tbody">       
                %for slip in sorted(payslips.slip_ids, key=lambda slip: slip.employee_id.name):
			    <div class="act_as_row lines">           
                              ## cedula
                              <div class="act_as_cell first_column" style="width: 80px;">${slip.employee_id.identification_id or ''}</div>
                              ## nombre
                              <div class="act_as_cell">${slip.employee_id.name or '0'}</div>
                              ## nh
                              <div class="act_as_cell amount">${get_hn(slip.worked_days_line_ids) or '0'}</div>				
                              ## eh
                              <div class="act_as_cell amount">${get_he(slip.worked_days_line_ids) or '0'}</div>
                              ## ef
                              <div class="act_as_cell amount">${get_fe(slip.worked_days_line_ids) or '0'}</div>
                              ## basic
                              <div class="act_as_cell amount">${formatLang(get_basic(slip.line_ids)) or '0'}</div>
                              ## exs
                              <div class="act_as_cell amount">${formatLang(get_exs(slip.line_ids)) or '0'}</div>
                              ## fes
                              <div class="act_as_cell amount">${formatLang(get_fes(slip.line_ids)) or '0'}</div>
                              ## otros
                              <div class="act_as_cell amount">${ '0'}</div>
                              ## gross
                              <div class="act_as_cell amount ">${formatLang(get_gross(slip.line_ids)) or '0'}</div>
                               ## ccss
                              <div class="act_as_cell amount">${formatLang(get_ccss(slip.line_ids)) or '0'}</div>
                              ## RENTA
                              <div class="act_as_cell amount">${formatLang(get_rent(slip.line_ids)) or '0'}</div>
                              ## otros
                              <div class="act_as_cell amount">${ '0'}</div>
                              ## NETOS
                              <div class="act_as_cell amount">${formatLang(get_net(slip.line_ids)) or '0'}</div>
				<%
				    total_hn += get_hn(slip.worked_days_line_ids)
				    total_he += get_he(slip.worked_days_line_ids)
				    total_fe += get_fe(slip.worked_days_line_ids)
				    total_basic += get_basic(slip.line_ids)
				    total_exs += get_exs(slip.line_ids)
				    total_fes += get_fes(slip.line_ids)
				    total_gross += get_gross(slip.line_ids)
				    total_rent += get_rent(slip.line_ids)
				    total_ccss += get_ccss(slip.line_ids)
				    total_net += get_net(slip.line_ids)
				    total_emp += 1
				%>
                    </div>
                %endfor
		</div>
		<div class="act_as_tfoot">
		<div class="act_as_row labels"  style="font-weight: bold; font-size: 11x">
		    <div class="act_as_cell first_column">${_('Total')}</div>
		    <div class="act_as_cell">${total_emp} Empleados</div>
		    <div class="act_as_cell amount">${total_hn}</div>
		    <div class="act_as_cell amount">${total_he}</div>
		    <div class="act_as_cell amount">${total_fe}</div>
		    <div class="act_as_cell amount">${formatLang(total_basic)}</div>
		    <div class="act_as_cell amount">${formatLang(total_exs)}</div>
		    <div class="act_as_cell amount">${formatLang(total_fes)}</div>
		    <div class="act_as_cell amount">${_('0')}</div>
		    <div class="act_as_cell amount">${formatLang(total_gross)}</div>
		    <div class="act_as_cell amount">${formatLang(total_ccss)}</div>
		    <div class="act_as_cell amount">${formatLang(total_rent)}</div>
		    <div class="act_as_cell amount">${_('0')}</div>
		    <div class="act_as_cell amount">${formatLang(total_net)}</div>
		</div>
            </div>
            </div>
            
		<div class="act_as_table data_table" style="margin-top:20px">
		<div class="act_as_tbody">
		<div class="act_as_row" style="vertical-align: bottom">
		<div class="act_as_cell" style="padding-top:80px;padding-bottom:5px">${'HECHO POR:'}</div>
		<div class="act_as_cell" style="padding-top:80px;padding-bottom:5px">${'REVISADO POR:'}</div>
		<div class="act_as_cell" style="padding-top:80px;padding-bottom:5px">${'APROBADO POR:'}</div>
            </div>
            </div>
            </div>      
               
               
	<p style="page-break-after:always"></p>
	%endfor
	
</body>
</html>