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
	%for payslips in objects :
		<div class="act_as_tbody">			
		    <div class="act_as_table data_table">
			<div class="act_as_row labels">
			    <div class="act_as_cell">${_('Cedula')}</div>
			    <div class="act_as_cell">${_('Nombre')}</div>
			    <div class="act_as_cell">${_('Hrs.')}<br />${_('Nor')}</div>
			    <div class="act_as_cell">${_('Hrs.')}<br />${_('Ext')}</div>
			    <div class="act_as_cell">${_('Hrs.')}<br />${_('Dob')}</div>
			    <div class="act_as_cell">${_('Ingr.')}<br />${_('Normal')}</div>
			    <div class="act_as_cell">${_('Ingr.')}<br />${_('Extra')}</div>
			    <div class="act_as_cell">${_('Ingr.')}<br />${_('Doble')}</div>
			    <div class="act_as_cell">${_('Otros')}<br />${_('Ingr.')}</div>
			    <div class="act_as_cell">${_('Salario')}<br />${_('Bruto')}</div>
			    <div class="act_as_cell">${_('Deducc.')}<br />${_('CCSS/BP')}</div>
			    <div class="act_as_cell">${_('Impuesto')}<br />${_('Renta')}</div>
			    <div class="act_as_cell">${_('Otras')}<br />${_('Deducc.')}</div>
			    <div class="act_as_cell">${_('Salario')}<br />${_('Neto')}</div>
			</div>
                %for slip in payslips.slip_ids:
			    <div class="act_as_row lines" style="vertical-align: top;">           
                              ## cedula
                              <div class="act_as_cell first_column" style="width: 80px;">${slip.employee_id.identification_id or ''}</div>
                              ## nombre
                              <div class="act_as_cell">${slip.employee_id.name or '0'}</div>
                              ## nh
                              <div class="act_as_cell">${get_hn(slip.worked_days_line_ids) or '0'}</div>
                              ## eh
                              <div class="act_as_cell">${get_he(slip.worked_days_line_ids) or '0'}</div>
                              ## ef
                              <div class="act_as_cell">${get_fe(slip.worked_days_line_ids) or '0'}</div>
                              ## basic
                              <div class="act_as_cell">${get_basic(slip.line_ids) or '0'}</div>
                              ## exs
                              <div class="act_as_cell">${get_exs(slip.line_ids) or '0'}</div>
                              ## fes
                              <div class="act_as_cell">${get_fes(slip.line_ids) or '0'}</div>
                              ## otros
                              <div class="act_as_cell">${ '0'}</div>
                              ## fes
                              <div class="act_as_cell">${get_gross(slip.line_ids) or '0'}</div>
                               ## ccss
                              <div class="act_as_cell">${get_ccss(slip.line_ids) or '0'}</div>
                              ## RENTA
                              <div class="act_as_cell">${ '0'}</div>
                              ## otros
                              <div class="act_as_cell">${ '0'}</div>
                              ## NETOS
                              <div class="act_as_cell">${ get_net(slip.line_ids) or '0'}</div>
                    </div>
                %endfor
            </div>
            
            </br></br>
            <div>Fecha desde: ${payslips.date_start}</div></br>
			<div>Fecha hasta: ${payslips.date_end}</div>
            
            </br></br></br></br>
            <div>${'HECHO POR: ___________________________________'   } </div> 
            </br></br></br></br>
            <div> ${'REVISADO POR: ___________________________________'} </div>
            </br></br></br></br>
            <div> ${'APROBADO POR: ___________________________________'} </div>          
          
         </div>           
               
	<p style="page-break-after:always"></p>
	%endfor
</body>
</html>
