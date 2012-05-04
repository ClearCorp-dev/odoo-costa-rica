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
                              <div class="act_as_cell">${slip.employee_id.name or ''}</div>
                              ## nh
                              <div class="act_as_cell">${get_nh(slip.worked_days_line_ids) or ''}</div>
                              ## eh
                              <div class="act_as_cell">${get_eh(slip.worked_days_line_ids) or ''}</div>
                              ## ef
                              <div class="act_as_cell">${get_ef(slip.worked_days_line_ids) or ''}</div>
                              ## basic
                              <div class="act_as_cell amount">${get_basic(slip.line_ids) or '0'}</div>
                              ## exs
                              <div class="act_as_cell amount">${get_exs(slip.line_ids) or '0'}</div>
                              ## fes
                              <div class="act_as_cell amount">${get_fes(slip.line_ids) or '0'}</div>
                              ## otros
                              <div class="act_as_cell amount">${ '0'}</div>
                              ## fes
                              <div class="act_as_cell amount">${get_gross(slip.line_ids) or '0'}</div>
                               ## ccss
                              <div class="act_as_cell amount">${get_ccss(slip.line_ids) or '0'}</div>
                              ## RENTA
                              <div class="act_as_cell amount">${ '0'}</div>
                              ## otros
                              <div class="act_as_cell amount">${ '0'}</div>
                              ## NETOS
                              <div class="act_as_cell amount">${ get_net(slip.line_ids) or '0'}</div>
                    </div>
                %endfor
            </div>
            
            </br>
            <div>${'HECHO POR: ___________________________________'   } </div> 
            </br>
            <div> ${'REVISADO POR: ___________________________________'} </div>
            </br>
            <div> ${'APROBADO POR: ___________________________________'} </div> 
            
            
        
                    
         </div>           
            
            
            
	<p style="page-break-after:always"></p>
	%endfor
</body>
</html>
