<html>
<head>
	<style style="text/css">
		${css}
	</style>
</head>
<body class = "data">
	%for payslips in objects :
		<div class="act_as_tbody">			
				<div class="act_as_table data_table">
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
