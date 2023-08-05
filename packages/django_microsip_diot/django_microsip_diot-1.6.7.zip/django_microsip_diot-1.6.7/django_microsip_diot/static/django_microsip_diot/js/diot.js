var page = 1;
var id_selected=0;
$("#integradas").trigger("change");
var total_importes = 0;
var total_ivas = 0;
// $("#inicio_ext").hide();
// MODAL DE PAGOS PARCIALES
var $tasa_iva_modal = $("#tasa_iva_modal");
var $importe_sin_iva_modal = $("#importe_sin_iva_modal");
var $proporcion_modal = $("#proporcion_modal");
var $iva_acreditable_modal = $("#iva_acreditable_modal");
var $iva_sin_acreditar_modal = $("#iva_sin_acreditar_modal");
var $iva_retenido_modal = $("#iva_retenido_modal");
var $descuento_modal = $("#descuento_modal");
var $tasa0_modal = $("#tasa0_modal");
var $tasa_exento_modal = $("#tasa_exento_modal");
var $id_xml = $("#id_xml");

// MODAL DE CAPTURA MANUAL
var $tasa_iva_manual = $("#tasa_iva_manual");
var $importe_sin_iva_manual = $("#importe_sin_iva_manual");
var $proporcion_manual = $("#proporcion_manual");
var $iva_acreditable_manual = $("#iva_acreditable_manual");
var $iva_sin_acreditar_manual = $("#iva_sin_acreditar_manual");
var $iva_retenido_manual = $("#iva_retenido_manual");
var $descuento_manual = $("#descuento_manual");
function get_totales(){
	$("#tabla_repositorios").find("tbody tr:visible").each(function(){
		var $row = $(this);
		total_importes += parseFloat($row.find("#importe").text().replace(/[^0-9\.]+/g,""));
		total_ivas += parseFloat($row.find("#iva").text().replace(/[^0-9\.]+/g,""));
	});
	$("#id_total_importes").text("$ "+total_importes.toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,'));
	$("#id_total_ivas").text("$ "+total_ivas.toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,'));
}
get_totales();



$("#integradas").on("change",function(){
	if ($(this).is(":checked"))
	{
		$("tr[class='diot_xml']").show();
	}
	else
	{
		$("tr[class='diot_xml']").hide();
		$("tr[class='diot_xml']").find(".chk_repo").attr("checked",false);
	};
	var num_mostrados = String($("#tabla_repositorios").find("tr:visible").length-1);
	$("#paginacion").children().text('Mostrando '+num_mostrados+' de '+String(total))
});

$("#id_repos_ext").on("change",function(){
	if ($(this).is(":checked"))
	{
		$("#inicio_ext").show();
	}
	else
	{
		$("#inicio_ext").hide();
	};
});

$("#integrar").on("change",function(){
	var checked = $(this).is(":checked");
	$(".chk_repo:enabled").each(function(){

		$(this).attr("checked",checked);
		$(this).trigger("change");
	});
});


$("#crear_txt").on("click",function(){
	var checked_repos = $(".chk_repo:checked");
	var dic_diot = {}
	checked_repos.each(function(){

		var $row = $(this).parent().parent();
		var descuento = parseFloat($row.find("#descuento").val());
		var folio = $row.find("#folio").text().trim();
		var id_fiscal = $row.find("#id_fiscal").val();
		var id_repositorio = $(this).val();
		var ieps = parseFloat($row.find("#ieps").val());
		var importe = parseFloat($row.find("#importe").text().replace(/[^0-9\.]+/g,""));
		var iva = parseFloat($row.find("#iva").text().replace(/[^0-9\.]+/g,""));
		var iva_acreditable = parseFloat($row.find("#iva_acreditable").val());
		var iva_descuentos = parseFloat($row.find("#iva_descuentos").val());
		var iva_no_acreditable = parseFloat($row.find("#iva_no_acreditable").val());
		var iva_retenido = parseFloat($row.find("#iva_retenido").val());
		var nombre = $row.find("#nombre").text();
		var pagado = parseFloat($row.find("#pagado").text().replace(/[^0-9\.]+/g,""));
		var pagado_h = parseFloat($row.find("#pagado_h").val());
		var rfc = $row.find("#rfc").text().trim();
		var subtotal = parseFloat($row.find("#subtotal").val());
		var tipo_comprobante = $row.find("#tipo_comprobante").val();
		var tasa_exento = parseFloat($row.find("#tasa_exento").val());
		var tasa0 = parseFloat($row.find("#tasa0").val());

		var iva_pagado = 0;
		var extranjero = 'N'

		
		if (rfc == "None")
		{
			rfc=id_fiscal;
			extranjero = 'S'
		}

		var tasa0_val = 0;
		var tasaexento_val = 0;
		var tasa16_val = 0;
		
		// Calcula tasa0 y tasa iva dependiendo si tiene iva o no
		if (iva == 0)
		{
			// si es pago total
			if ($(this).parent().parent().attr("style") != "background-color: bisque;")
			{
				tasa0_val = subtotal-descuento;
				iva = 0;
				if (tasa_no_iva == 'E')
				{
					tasaexento_val = tasa0_val;
					tasa0_val = 0;
				};
			}
			// Si es pago parcial
			else
			{
				iva = 0;
				tasa0_val = subtotal;
				tasaexento_val = tasa_exento;
				tasa0_val = tasa0;
			}
			
		}
		else
		{
			// si es pago total
			if ($(this).parent().parent().attr("style") != "background-color: bisque;")
			{
				tasa16_val = iva *100/16;
				tasa0_val = importe - iva - tasa16_val;
				if (tasa_no_iva == 'E')
				{
					tasaexento_val = tasa0_val;
					tasa0_val = 0;
				};
			}
			// Si es pago parcial
			else
			{
				tasa16_val = iva_acreditable * 100 / 16;
				tasa0_val = subtotal - tasa16_val;
				iva = tasa16_val * 0.16;
				tasa0_val = tasa0;
				tasaexento_val = tasa_exento;
			}
		};

		if (tasa0_val >= ieps)
		{
			tasa0_val = tasa0_val-ieps;
		};

		if (rfc in dic_diot == false){
			dic_diot[rfc] = {}
			dic_diot[rfc]['extranjero'] = extranjero
			dic_diot[rfc]['nombre'] = nombre
			dic_diot[rfc]['tasa0'] = 0
			dic_diot[rfc]['tasaexento'] = 0
			dic_diot[rfc]['tasa16'] = 0
			dic_diot[rfc]['retenido'] = 0
			dic_diot[rfc]['iva_no_acreditable'] = 0
			dic_diot[rfc]['iva_descuentos'] = 0
			dic_diot[rfc]['detalles'] = []
		}
		
		dic_diot[rfc]['tasa0'] += tasa0_val;
		dic_diot[rfc]['tasaexento'] += tasaexento_val;
		dic_diot[rfc]['tasa16'] += tasa16_val;
		dic_diot[rfc]['retenido'] += iva_retenido;
		dic_diot[rfc]['iva_no_acreditable'] += iva_no_acreditable;
		dic_diot[rfc]['iva_descuentos'] += iva_descuentos;
		
		if ($row.attr("class") != "diot_xml")
		{
			$.ajax({
				url:'/diot/guardar_repositorio',
				type:'get',
				data:{
					'id':id_repositorio ,
					'iva_descuentos':iva_descuentos,
					'iva_retenido': iva_retenido,
					'iva_pagado':iva,
					'iva':parseFloat($row.find("#iva").text().replace(/[^0-9\.]+/g,"")),

				},
				success:function(data){
					console.log("Correcto actualizar repositorio");
				},
				error:function(data){
					console.log("Error");
				}
			});
		};
		dic_diot[rfc]['detalles'].push([String(folio),subtotal,parseFloat(iva).toFixed(2)])
		
	});

	var detallado=false;
	if (confirm("Desea Agregar los detalles por Proveedor al Archivo?")==true)
	{
		detallado = true;
	};
	$("#wait").modal('show');
	checked_repos.each(function(){
		var integrar = 'N';
		var id = $(this).val();
		var row = $(this).parent().parent();
		var fecha_row = row.find("#fecha");
		// SI ES PAGO TOTAL
		if (row.attr("style") != "background-color: bisque;")
		{
			$.ajax({
				url:'/diot/pago_total',
				type:'get',
				data:{
					'id': id,
				},
				success:function(data){
				},
				error:function(data){
				}
			});
		}
		// SI ES PAGO PARCIAL
		else
		{
			var pago = parseFloat($(this).parent().parent().find("#pagado").text().replace(/[^0-9\.]+/g,""));
			$.ajax({
				url:'/diot/pago_parcial',
				type:'get',
				data:{
					'id': id,
					'pago':pago,
				},
				success:function(data){
				},
				error:function(data){
				}
			});
		};

		// SI ES UN XML EXTEMPORANEO
		if (fecha_row.attr("class") == 'extemporanea' )
		{
			$.ajax({
				url:'/diot/genero_ext',
				type:'get',
				data:{
					'id':id,
				},
				success:function(data){
					console.log("genero_ext")
				},
				error:function(data){
					alert("Error Interno en Servidor");
				},
				complete:function(){
				}
			});
		};
	});
	$.ajax({
		url:'/diot/create_file',
		type:'get',
		data:{
			'dic_diot':JSON.stringify(dic_diot),
			'fecha_inicio':fecha_inicio,
			'detallado':detallado,
		},
		success:function(data){

		},
		error:function(data){
			alert("Error.\nSe recomienda Sincronizar el Catalogo de Proveedores antes de generar el archivo.");
		},
		complete:function(){
			window.location.replace(this.url);
			$("#wait").modal('hide');
		}
	});
});

$(window).scroll(function() {
   // if($(window).scrollTop() + $(window).height() == $(document).height()) {
   //     page+=1;
   //     $.ajax({
   //    		url:'/diot/paginacion',
   //    		type:'get',
   //    		data:{
   //    			'page':page,
   //    			'fecha_inicio':fecha_inicio,
   //    			'fecha_fin':fecha_fin,
   //    			'inicio_ext':inicio_ext,
   //    			'repos_ext':repos_ext,
   //    		},
   //    		success:function(data){
   //    			if (!data.error)
   //    			{

   //    				data.pagina.forEach(function(repo){

   //    					var options = { year: "numeric", month: "long",
   //    						day: "numeric" };
   //    					var style = "";
   //    					var fecha = new Date(repo[0].fecha);
   //    					var fecha_ini = new Date(fecha_inicio);
   //    					fecha_string = fecha.toLocaleDateString("es-es",options);

   //    					$('#tabla_repositorios').find('tbody').append( "<tr> <td> <input type='checkbox' class='chk_repo' value='"+repo[0].id+"'>  </td><td id='fecha' "+style+"><small>"+fecha_string+"</small></td> <td id='folio'> "+  repo[0].folio+"<input type='hidden' id='tipo_comprobante' value='"+repo[0].tipo_comprobante+"''></td> <td id='nombre'><small>"+repo[0].nombre+"</small><input type='hidden' id='pagado_h' value='"+repo[0].pagado+"}}'><input type='hidden' id='pago' value='0'></td><td id='rfc'>"+repo[0].rfc+" <input type='hidden' id='id_fiscal' value='"+repo[0].taxid+"'></td><td id='pagado' class='text-right'>$ "+repo[0].pagado+"</td><td id='importe' class='text-right'>$ "+repo[0].importe+"</td> <td id='iva' class='text-right'>$ "+repo[1]+"<input type='hidden' id='subtotal' value='"+repo[2]+"'>  <input type='hidden' id='descuento' value='"+repo[3]+"'> <input type='hidden' id='iva_retenido' value='"+repo[4]+"'></td><td><button class='btn options' data-toggle='modal' data-target='#options_Modal' ><i class='glyphicon glyphicon-usd'></i></button></td></tr>" );
   //    					var $row = $('#tabla_repositorios').find('tbody').find("tr").last();
   //    					if (repo[0].pagado >= repo[0].importe)
   //    					{
   //    						$row.addClass("diot_xml");
   //    						$row.find(".options").remove();
   //    					};

   //    					if (fecha<fecha_ini)
   //    					{
   //    						$row.find("#fecha").addClass("extemporanea");
   //    					};

   //    					if (repo[0].integrar == 'S')
   //    					{

   //    						if (parseFloat(repo[0].pagado < repo[0].importe))
   //    						{
   //    							$row.attr("style","background-color: bisque;");
   //    						};
   //    					};

   //    				});
   //    				var num_mostrados = String($("#tabla_repositorios").find("tr").length-1);
   //    				total = data.total;
   //    				$("#paginacion").children().text('Mostrando '+num_mostrados+' de '+String(total))
   //    			}

   //    		},
   //    		error:function(data){
   //    		}
   //     });

   // }
});

function calc_exento(btn){
	$tr = btn.parent().parent()
	$id_xml = $tr.find(".chk_repo");
	var importe = parseFloat($tr.find("#importe").text().replace(/[^0-9\.]+/g,""));
	var iva = parseFloat($tr.find("#iva").text().replace(/[^0-9\.]+/g,""));
	var iva_retenido = parseFloat($tr.find("#iva_retenido").val());
	var descuento = parseFloat($tr.find("#descuento").val());
	var pagado = parseFloat($tr.find("#pagado").text().replace(/[^0-9\.]+/g,""));
	var subtotal = parseFloat($tr.find("#subtotal").val());
	var tasa0 = parseFloat($tr.find("#tasa0").val());
	var tasa_exento = parseFloat($tr.find("#tasa_exento").val());
	var pagado_h = parseFloat($tr.find("#pagado_h").val());
	var importe_sin_iva;

	// para sacar el resto de lo que se debe
	if (descuento>0)
	{
		if ($(this).parent().parent().attr("style") != "background-color: bisque;")
		{
			importe = subtotal-descuento;
		}
		else
		{
			if (iva == 0)
			{
				importe = importe-pagado_h;
			}
			else
			{
				importe = (importe-pagado_h)/1.16;
			};
		};

	}
	else
	{
		if (iva == 0)
		{
			importe = importe-pagado_h;
		}
		else
		{
			importe = (importe-pagado_h)/1.16;
		};
	};

	if (iva==0)
	{
		importe_sin_iva = importe
		$tasa_iva_modal.val(0);
		$proporcion_modal.attr("disabled",true);
		$iva_acreditable_modal.attr("disabled",true);
		$iva_sin_acreditar_modal.attr("disabled",true);
		$iva_retenido_modal.attr("disabled",true);
	}
	else
	{
		importe_sin_iva = importe
		$tasa_iva_modal.val(16);
		$proporcion_modal.attr("disabled",false);
		$iva_acreditable_modal.attr("disabled",false);
		$iva_sin_acreditar_modal.attr("disabled",false);
		$iva_retenido_modal.attr("disabled",false);
	};

	if (pagado_h>0)
	{
		iva = iva_acreditable;

	};
	$importe_sin_iva_modal.val(parseFloat(importe_sin_iva.toFixed(2)));
	$proporcion_modal.val(1.0);
	var iva_acreditable = ($importe_sin_iva_modal.val()*$proporcion_modal.val()*$tasa_iva_modal.val()/100).toFixed(2);
	$iva_acreditable_modal.val(iva);
	$iva_sin_acreditar_modal.val(0);
	$iva_retenido_modal.val(iva_retenido);
	$descuento_modal.val(0);

	var valor_exento_0 = parseFloat($importe_sin_iva_modal.val())-(parseFloat($iva_acreditable_modal.val())*100/16);
	if (valor_exento_0 < 2) {valor_exento_0 = 0};
	if (tasa_no_iva == 'E')
	{
		tasa_exento =valor_exento_0 
	}
	else
	{
		tasa0 = valor_exento_0
	};
	$tasa_exento_modal.val(tasa_exento.toFixed(2));
	$tasa0_modal.val(tasa0.toFixed(2));
};

$(".chk_repo").on("change",function(){

	var row = $(this).parent().parent();
	if ((row.attr("style") == "background-color: bisque;") && (!$(this).is(":checked")) )
	{
		$(this).attr("disabled",true);
		var pagado_inicial = row.find("#pagado_h").val()
		row.find("#pagado").text("$ "+pagado_inicial);
	}
	
	var integrar = 'S';
	var id = $(this).val();
	if (!$(this).is(":checked"))
	{
		integrar = 'N'
	};
	$.ajax({
		url:'/diot/change_xml_status',
		type:'get',
		data:{
			'integrar':integrar,
			'id': id,
		},
		success:function(data){
		},
		error:function(data){
		}
	})
});

// COMPONENTES DE MODAL DE CAPTURA DE PAGOS PARCIALES
$(".options").on("click",function(){
	calc_exento($(this));
});

$("#tasa_iva_modal").on("change",function(){
	if ($("#tasa_iva_modal").val()==0)
	{
		$proporcion_modal.attr("disabled",true);
		$iva_acreditable_modal.attr("disabled",true);
		$iva_sin_acreditar_modal.attr("disabled",true);
		$iva_retenido_modal.attr("disabled",true);
	}
	else
	{
		
		$proporcion_modal.attr("disabled",false);
		$iva_acreditable_modal.attr("disabled",false);
		$iva_sin_acreditar_modal.attr("disabled",false);
		$iva_retenido_modal.attr("disabled",false);
	};
});

$("#proporcion_modal").on("input",function(){
	$iva_acreditable_modal.val($importe_sin_iva_modal.val()*$proporcion_modal.val()*$tasa_iva_modal.val()/100);
	$iva_sin_acreditar_modal.val($importe_sin_iva_modal.val()*(1-$proporcion_modal.val())*$tasa_iva_modal.val()/100);
});

$("#importe_sin_iva_modal").on("input",function(){
	$proporcion_modal.trigger("input");
	
});

$("#iva_acreditable_modal").on("input",function(){
});

$("#modificar_xml").on("click",function(){
	var pagado = parseFloat($id_xml.parent().parent().find("#pagado").text().replace(/[^0-9\.]+/g,""));
	var importe = parseFloat($id_xml.parent().parent().find("#importe").text().replace(/[^0-9\.]+/g,""));
	var pagado_final;
	var $row = $id_xml.parent().parent();
	
	if ($(tasa_iva_modal).val()!=0)
	{
		var importe_mas_iva = parseFloat(parseFloat($importe_sin_iva_modal.val()) + parseFloat($iva_acreditable_modal.val()));
		pagado_final = importe_mas_iva+pagado;
	}
	else
	{	
		pagado_final = parseFloat($importe_sin_iva_modal.val())+pagado;
	}
	if (pagado_final <= importe)
	{
		$row.attr("style","background-color: bisque;");
		$('.tags-modal-md').modal('hide');
		$row.find(".chk_repo").attr("checked","checked");
		$row.find(".chk_repo").attr("disabled",false);

		$row.find("#iva_descuentos").val($descuento_modal.val());
		$row.find("#iva_no_acreditable").val($iva_sin_acreditar_modal.val());
		$row.find("#iva_retenido").val($iva_retenido_modal.val());
		
		$row.find("#subtotal").val(parseFloat($importe_sin_iva_modal.val()));
		$row.find("#pagado").text("$ "+pagado_final);
		$row.find("#iva_acreditable").val(parseFloat($iva_acreditable_modal.val()));
		$row.find("#tasa_exento").val(parseFloat($tasa_exento_modal.val()));
		$row.find("#tasa0").val(parseFloat($tasa0_modal.val()));
		$row.find("#iva_acreditable").val(parseFloat($iva_acreditable_modal.val()));
	}
	else
	{
		alert("El importe mas el iva no puede ser mayor al importe del XML");
	};
});


// COMPONENTES DE MODAL DE CAPTURA MANUAL
$("#tasa_iva_manual").on("change",function(){
	if ($("#tasa_iva_manual").val()==0)
	{
		$proporcion_manual.attr("disabled",true);
		$proporcion_manual.val(0);
		$proporcion_manual.trigger("input");

		$iva_acreditable_manual.attr("disabled",true);
		$iva_sin_acreditar_manual.attr("disabled",true);
		$iva_retenido_manual.attr("disabled",true);
	}
	else
	{
		
		$proporcion_manual.attr("disabled",false);
		$proporcion_manual.val(1);
		$proporcion_manual.trigger("input");
		$iva_acreditable_manual.attr("disabled",false);
		$iva_sin_acreditar_manual.attr("disabled",false);
		$iva_retenido_manual.attr("disabled",false);
	};
});

$("#proporcion_manual").on("input",function(){
	$iva_acreditable_manual.val($importe_sin_iva_manual.val()*$proporcion_manual.val()*$tasa_iva_manual.val()/100);
	$iva_sin_acreditar_manual.val($importe_sin_iva_manual.val()*(1-$proporcion_manual.val())*$tasa_iva_manual.val()/100);
});

$("#importe_sin_iva_manual").on("input",function(){
	$proporcion_manual.trigger("input");
});

$("#captura_manual").on("click",function(){
	var id = $("#id_proveedor").val();
	var lista = $("#id_fecha_manual").val().split("/");
	var nueva_fecha = lista[1]+"/"+lista[0]+"/"+lista[2]
	var fecha_serv = lista[2]+"-"+lista[1]+"-"+lista[0]
	var fecha = new Date(nueva_fecha);
	var options = { year: "numeric", month: "long",
	day: "numeric" };
	var fecha_string = fecha.toLocaleDateString("es-es",options);
	var folio = $("#folio_manual").val();
	var nombre;
	var rfc;
	var importe = parseFloat($("#importe_sin_iva_manual").val()) + parseFloat($("#iva_acreditable_manual").val())
	$('.tags-modal-md').modal('hide');
	$.ajax({
		url:'/diot/captura_manual',
		type:'get',
		data:{
			'id_proveedor':id,
			'folio':folio,
			'fecha':fecha_serv,
			'importe':importe,
			'subtotal':$("#importe_sin_iva_manual").val(),
			'iva_acreditable':$("#iva_acreditable_manual").val(),
			'iva_no_acreditable':$("#iva_sin_acreditar_manual").val(),
			'iva_retenido':$("#iva_retenido_manual").val(),
			'iva_descuentos':$("#descuento_manual").val(),
		},
		success:function(data){
			nombre = data.nombre;
			rfc = data.proveedor_rfc;
			
			$('#tabla_repositorios').find('tbody').append( "<tr>"+
				"<td> <input type='checkbox' class='chk_repo' value='"+id+"' checked='checked'></td>"+
				"<td id='fecha'><small>"+fecha_string+"</small></td>"+
				"<td id='folio'> "+ folio+"</td>"+
				"<td id='nombre'><small>"+nombre+"</small></td>"+
				"<td id='rfc'>"+rfc+" </td>"+
				"<td id='pagado' class='text-right'>-</td>"+
				"<td id='importe' class='text-right'>$ "+importe+"</td>"+
				"<td id='iva' class='text-right'>$ "+$("#iva_acreditable_manual").val()+""+
				"<input type='hidden' id='subtotal' value='"+$("#importe_sin_iva_manual").val()+"'>"+
				"<input type='hidden' id='descuento' value=''>"+
				"<input type='hidden' id='iva_retenido' value='"+$("#iva_retenido_manual").val()+"'>"+
				"<input type='hidden' id='iva_no_acreditable' value='"+$("#iva_sin_acreditar_manual").val()+"'>"+
				"<input type='hidden' id='iva_descuentos' value='"+$("#descuento_manual").val()+"'>"+
				"</td>"+
				"<td></td>"+
				"<td></td>"+
				"</tr>" );
			$("#id_fecha_manual").val('');
			$("#folio_manual").val('');
			$("#proveedor_manual").find("#id_proveedor-deck").children().children().trigger("click");
			$("#importe_sin_iva_manual").val('');
			$("#proporcion_manual").val(1);
			$("#iva_acreditable_manual").val(0);
			$("#iva_sin_acreditar_manual").val(0);
			$("#iva_retenido_manual").val(0);
			$("#iva_descuentos").val(0);
		},
		error:function(data){
			alert("Error Interno en el servidor");
		}
	});
});

$(".remove").on("click",function(){
	var row = $(this).parent().parent();
	var id = row.find(".chk_repo").val();
	var manual = 0;
	if (row.find("#pagado").text() == '-') {manual = 1};
	if (confirm("Seguro que desea dejar de mostrar este registro?")==true)
	{
		$.ajax({
			url:'/diot/ocultar_repo',
			type:'get',
			data:{
				'id':id,
				'manual':manual,
			},
			success:function(data){
				row.hide();
				row.find(".chk_repo").attr("checked",false);
				row.find(".chk_repo").attr("disabled",true);
				get_totales();
			},
			error:function(data){
				alert("Error Interno en el servidor");
			}
		});
		
	};
});

$("#export_excel").on("click",function(){
	var tabla = [];
	$("#tabla_repositorios").find("tbody tr:visible").each(function(){
		var detalle = [];
		var fecha = $(this).find("#fecha").text().trim();
		var folio = $(this).find("#folio").text().trim();
		var nombre = $(this).find("#nombre").text().trim();
		var rfc = $(this).find("#rfc").text().trim();
		var pagado = $(this).find("#pagado").text().replace(/[^0-9\.]+/g,"").trim();
		var importe = $(this).find("#importe").text().replace(/[^0-9\.]+/g,"").trim();
		var iva = $(this).find("#iva").text().replace(/[^0-9\.]+/g,"").trim();
		var iva_descuentos = $(this).find("#iva_descuentos").val();
		var iva_retenido = $(this).find("#iva_retenido").val();
		
		detalle = [fecha,folio,nombre,rfc,pagado,importe,iva,iva_descuentos,iva_retenido];
		tabla.push(detalle);
	});

	var nombre_doc = prompt("Ingresa el nombre del archivo a guardar", "DIOT");
	if (nombre_doc != null)
	{
		$.ajax({
			url:'/diot/exporta_excel',
			type:'get',
			data:{
				'tabla':JSON.stringify(tabla),
				'nombre_doc':nombre_doc,
			},
			success:function(data){
				window.location.replace(this.url);
			},
			error:function(data){
				alert("Error Interno en el servidor");
			}

		});
	};
});

$("#remove_repo_main").on("change",function(){
	var checked = $(this).is(":checked");
	$(".remove_repo:enabled").each(function(){
		$(this).attr("checked",checked);
	});
});
// ELIMINAR VARIOS REPOS A LA VEZ
$("#remove_repos").on("click",function(){
	if (confirm("Seguro que desea dejar de mostrar estos registros?")==true)
	{
		var checked_repos_remove = $(".remove_repo:checked");
		checked_repos_remove.each(function(){
			var id = $(this).val();
			var row = $(this).parent().parent();
			var manual = 0;
			if (row.find("#pagado").text() == '-') {manual = 1};
			$.ajax({
				url:'/diot/ocultar_repo',
				type:'get',
				data:{
					'id':id,
					'manual':manual,
				},
				success:function(data){
					row.hide();
					row.find(".chk_repo").attr("checked",false);
					row.find(".chk_repo").attr("disabled",true);
					get_totales();
				},
				error:function(data){
					alert("Error Interno en el servidor");
				}
			});
		});
	};
});