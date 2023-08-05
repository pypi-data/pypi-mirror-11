
$("#id_period_start_datetime, #id_period_end_datetime").datetimepicker({'dateFormat':'yy-mm-dd'});
var fecha = new Date($("#id_next_execution").val());

countdown.setLabels(
    ' milissegundo| segundo| minuto| hora| dia| semana| mes| año| década| século| milênio',
    ' milissegundos| segundos| minutos| horas| dias| semanas| meses| años| décadas| séculos| milênios',
    ' y ',
    ', ',
    'ahora');

function dateAdd(date, interval, units) {
  var ret = new Date(date); //don't change original date
  switch(interval.toLowerCase()) {
    case 'ano'   :  ret.setFullYear(ret.getFullYear() + units);  break;
    // case 'quarter':  ret.setMonth(ret.getMonth() + 3*units);  break;
    case 'mes'  :  ret.setMonth(ret.getMonth() + units);  break;
    case 'semana'   :  ret.setDate(ret.getDate() + 7*units);  break;
    case 'dia'    :  ret.setDate(ret.getDate() + units);  break;
    case 'horas'   :  ret.setTime(ret.getTime() + units*3600000);  break;
    case 'minuto' :  ret.setTime(ret.getTime() + units*60000);  break;
    // case 'second' :  ret.setTime(ret.getTime() + units*1000);  break;
    default       :  ret = undefined;  break;
  }
  return ret;
}

function get_next_execution(start, end, interval, units){
    var next_execution = start;
    var fecha_ahora = new Date();
    while(next_execution < fecha_ahora){
        next_execution = dateAdd(next_execution, interval, units);
    }

    return next_execution;
}

function get_next_execution_text(){
    var fecha_inicio = new Date($("#id_period_start_datetime").val());
    var fecha_fin = new Date($("#id_period_end_datetime").val());
    var units = $("#id_period_quantity").val();
    var interval = $("#id_period_unit").val();
    var fecha_ahora = new Date();
    var html = "";
    var fecha_siguiente = get_next_execution(fecha_inicio, fecha_fin, interval, units);
    debugger;
    if( fecha_siguiente <= fecha_ahora){
        fecha_siguiente = fecha_ahora;
        html += "Siguiente ejecución programada <strong>ahora</strong><br/>";
    }
    else{
        html += "Siguiente ejecución programada en <strong>"+ countdown(fecha_siguiente).toString() +"</strong><br/>";
    }
    
    html += "<strong>Se repetira cada "+$("#id_period_quantity").val()+" "+ $("#id_period_unit option:selected").text()+"</strong>";
    return html;
}
if ($("#id_next_execution").val() === ""){
    $("#id_siguiente_ejecucion_alert").hide();
}

$("#id_btnshow_modal").on("click", function(){
    $("#id_modal_seguro").modal();
});

setInterval(function () {
    $("#id_siguiente_ejecucion_text, .info_guardar_preview").html(get_next_execution_text());
}, 1000);
