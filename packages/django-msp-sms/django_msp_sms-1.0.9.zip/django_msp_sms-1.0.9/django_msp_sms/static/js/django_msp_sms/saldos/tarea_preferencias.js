$("#id_period_start_datetime, #id_period_end_datetime").datetimepicker({'dateFormat':'yy-mm-dd'});
var fecha = new Date($("#id_next_execution").val());

countdown.setLabels(
    ' milissegundo| segundo| minuto| hora| dia| semana| mes| ano| década| século| milênio',
    ' milissegundos| segundos| minutos| horas| dias| semanas| meses| anos| décadas| séculos| milênios',
    ' y ',
    ', ',
    'ahora');

function get_next_execution_text(){
    var fecha_inicio = new Date($("#id_period_start_datetime").val());
    var fecha_siguiente = new Date($("#id_next_execution").val());
    
    var fecha_ahora = new Date();
    var html = "";
    if ($("#id_next_execution").val() === ""){
        if (fecha_inicio > fecha_ahora) {
            fecha_siguiente = fecha_inicio;
        }else{
            fecha_siguiente = fecha_ahora;
        }


        if(fecha_siguiente <= fecha_ahora ) {
            html += "Siguiente ejecución programada <strong>ahora</strong><br/>";
        }
        else{
            html += "Siguiente ejecución programada en <strong>"+ countdown(fecha_siguiente).toString() +"</strong><br/>";
        }
    }
    else {
        
        if( fecha_siguiente <= fecha_ahora){
            fecha_siguiente = fecha_ahora;
            html += "Siguiente ejecución programada <strong>ahora</strong><br/>";
        }
        else{
            html += "Siguiente ejecución programada en <strong>"+ countdown(fecha_siguiente).toString() +"</strong><br/>";
        }
    }
    html += "<strong>Se repetira cada "+$("#id_period_quantity").val()+" "+ $("#id_period_unit option:selected").text()+"</strong>";
    return html;
}
if ($("#id_next_execution").val() === ""){
    $("#id_siguiente_ejecucion_alert").hide();
}

$("#id_btnshow_modal").on("click", function(){
    setInterval(function () {
        $(".info_guardar_preview").html(get_next_execution_text());
    }, 1000);
    
    $("#id_modal_seguro").modal();

});

setInterval(function () {
    $("#id_siguiente_ejecucion_text").html(get_next_execution_text());
}, 1000);
