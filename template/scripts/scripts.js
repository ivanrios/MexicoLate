var Actual;
var ActualAutor;
var ActualAvatar;
var Siguiente;
var totales = 0;
var Max = 50;
var cnt = 14;



function ValidaCadena(cadena){
	valido = true;
	vetadas = ["Borek", "jonas", "bieber", "estupidez", "futbol", "gol", "ivanrios"];
	for ( var i = 0; i < vetadas.length ; i++ ) {
		valido = ((valido) && ( cadena.indexOf(vetadas[i])  < 0));
		return (valido);
	} 
}

function Recargar(){
	document.location = "/";     	
}
Animalo = function(){
	$(ActualAutor).prependTo($(Actual).find('div'));
	$("<img src='"+ActualAvatar.html()+"'/>").prependTo($(Actual).find('div'));
	$(Actual).find('div').addClass("mensajeado");
	$(Actual).hide().prependTo('#MensajesProcesados').slideDown('slow');
	if (totales<=Max)
	Anima(Siguiente);
	return false;
};
function Anima(elemento){
	totales ++;
	$("#MensajeActual").html('<blockquote></blockquote><p id="autorActual"></p>').slideDown('slow');
	codigoActual = elemento.html();
	$(elemento).remove()
	Siguiente = $("#mensajes .twitt").first();
	Actual  = $("<div></div>");
	$(Actual).html(codigoActual);
	var autor = $(Actual).find('p').next();
	var foto = $(autor).next();
	ActualAutor = autor;
	ActualAvatar = foto;
	$(autor).remove();
	$(foto).remove();
	if ($(Actual).html() !="" ){
		if(ValidaCadena($(Actual).html())){
			$("#MensajeActual blockquote").append($(Actual));
			$("#autorActual").append("<img src='"+foto.html()+"'/>");
			$("#autorActual").append(autor);
			$(Actual).ticker({callback:Animalo}).trigger("play").trigger("stop");
		}
		else
		if (totales<=Max) Anima(Siguiente);
		return false;
	}
	else{
		$("#MensajeActual").fadeOut();
		$("#Recargar").show();
	}
}
$(document).ready(function(){
	$('#ElContador').html((cnt-10));
	var contador = setInterval(function() {
		cnt--;
		if (cnt >= 10) {
			$('#ElContador').html((cnt-10));
		}
		if (cnt == 10){
			$("#ContenedorContador").slideUp();
			Anima($("#mensajes .twitt").first());
		}
		if (cnt == 0){
			$("#Bienvenido").slideUp();
			clearInterval(contador);
		}
		}, 1000);
		$("#Recargar").click(function(){
			$(this).fadeOut();
			Recargar();
		})
	});
