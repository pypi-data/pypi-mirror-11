$("#btnEnviar-estadosCuenta").on("click", function(){
    clientes_ids = $("#id_clientes").val();
	if (clientes_ids== null) {
		alert("Por favor selecciona al menos un cliente.")
	}
	else{
    	sendMessages(clientes_ids)
	}
});