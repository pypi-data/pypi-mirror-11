var files



function prepareUpload(event)
{
  files = event.target.files;
  debugger;
  for (var i = files.length - 1; i >= 0; i--) {
	  $.ajax({
	  	url:'/diot/xml_to_object',
	  	type:'get',
	  	data:{
	  		'path':files[i].webkitRelativePath ,
	  	},
	  	success:function(data){
	  		console.log("Correcto actualizar repositorio");
	  	},
	  	error:function(data){
	  		console.log("Error");
	  	}
	  });
  	$("#tabla_xmls tbody").append("<tr><td></td><td>"+files[i].name+"</td></tr>");
  };
}
$('#folder').on('change', prepareUpload);