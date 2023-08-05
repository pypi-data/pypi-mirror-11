$("#crear_paises").on("click",function(){
	$("#wait").modal('show');
	$("#crear_paises").attr("disabled",true);
	$.ajax({
		url:'/diot/crear_paises',
		type:'get',
		data:{
		},
		success:function(data){
			if (data.nuevos > 0)
			{
				alert("se agregaron "+data.nuevos+" Paises nuevos.");
			}
			else
			{
				alert("Proceso Terminado.\nNo se agregaron nuevos paises.");
			};
			$("#crear_paises").attr("disabled",false);
		},
		error:function(data){
			$("#crear_paises").attr("disabled",false);
			alert("Error Interno en el servidor");
		},
		complete:function(){
			$("#wait").modal('hide');
		}
	})
});

$("#sincronizar_catalogo").on("click",function(){
	$("#wait").modal('show');
	$("#sincronizar_catalogo").attr("disabled",true);
	$.ajax({
		url:'/diot/exporta_proveedores',
		type:'get',
		data:{
		},
		success:function(data){
			if (data.nuevos > 0)
			{
				alert("se agregaron "+data.nuevos+" Proveedores nuevos.");
			}
			else
			{
				alert("Proceso Terminado.\nNo se agregaron nuevos proveedores.");
			};
			$("#sincronizar_catalogo").attr("disabled",false);
		},
		error:function(data){
			$("#sincronizar_catalogo").attr("disabled",false);
			alert("Error Interno en el servidor");
		},
		complete:function(){
			$("#wait").modal('hide');
		}
	})
});