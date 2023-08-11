var form_1 = document.querySelector(".form_1");
var form_2 = document.querySelector(".form_2");
var form_3 = document.querySelector(".form_3");
var form_4 = document.querySelector(".form_4");
var form_5 = document.querySelector(".form_5");

var form = document.querySelector("form")

var form_1_btns = document.querySelector(".form_1_btns");
var form_2_btns = document.querySelector(".form_2_btns");
var form_3_btns = document.querySelector(".form_3_btns");
var form_4_btns = document.querySelector(".form_4_btns");
var form_5_btns = document.querySelector(".form_5_btns");


var form_1_next_btn = document.querySelector(".form_1_btns .btn_next");
var form_2_back_btn = document.querySelector(".form_2_btns .btn_back");
var form_2_next_btn = document.querySelector(".form_2_btns .btn_next");
var form_3_back_btn = document.querySelector(".form_3_btns .btn_back");
var form_3_next_btn = document.querySelector(".form_3_btns .btn_next");
var form_4_back_btn = document.querySelector(".form_4_btns .btn_back");
var form_4_next_btn = document.querySelector(".form_4_btns .btn_next");
var form_5_back_btn = document.querySelector(".form_5_btns .btn_back");

var form_2_progessbar = document.querySelector(".form_2_progessbar");
var form_3_progessbar = document.querySelector(".form_3_progessbar");
var form_4_progessbar = document.querySelector(".form_4_progessbar");
var form_5_progessbar = document.querySelector(".form_5_progessbar");

var btn_done = document.querySelector(".btn_done");
var modal_wrapper = document.querySelector(".modal_wrapper");
var shadow = document.querySelector(".shadow");

function validate(){
	if (!form.checkValidity()) {
		event.preventDefault()
		event.stopPropagation()
		}
	form.classList.add('was-validated')
}

form_1_next_btn.addEventListener("click", function(){
	validate()
	var inputtnom = document.getElementById('nombrePrograma').value
	var selectcat = document.getElementById('categorias').value
	var selectgen = document.getElementById('genero').value
	var selectviv = document.getElementById('vivo').value
	var inputlocal= document.getElementById('localidadEmision').value
	var inputdate= document.getElementById('input_date').value
	var inputtime= document.getElementById('input_time').value
	var inputtarea= document.getElementById('input_tarea').value
	
	if (inputtnom.length == 0 || selectcat  == 0 || selectgen == 0 || selectviv == 0 || 
		inputlocal.length == 0 || inputdate.length == 0 || inputtime.length == 0 || inputtarea.length == 0){
		alert ("Complete los campos")
	}
	else{
		form_1.style.display = "none";
		form_2.style.display = "block";
		form_1_btns.style.display = "none";
		form_2_btns.style.display = "flex"; 
		form_2_progessbar.classList.add("active");}
});

form_2_back_btn.addEventListener("click", function(){
	validate()
	form_1.style.display = "block";
	form_2.style.display = "none";
	form_1_btns.style.display = "flex";
	form_2_btns.style.display = "none";
	form_2_progessbar.classList.remove("active");
});

form_2_next_btn.addEventListener("click", function(){
	validate()
	var inputrutina = document.getElementById('linkRutina').value
	var inputvideo1 = document.getElementById('linkVideo1').value
	var inputvideo2 = document.getElementById('linkVideo2').value
	var inputvideo3 = document.getElementById('linkVideo3').value
	var inputcover= document.getElementById('linkCover').value

	if (inputrutina.length == 0 || inputvideo1.length  == 0 || inputvideo2.length == 0 || 
		inputvideo3.length == 0 || inputcover.length == 0 ){
		alert ("Complete los campos")
	}
	else{
		form_2.style.display = "none";
		form_3.style.display = "block";
		form_3_btns.style.display = "flex";
		form_2_btns.style.display = "none";
		form_3_progessbar.classList.add("active");}
});

form_3_back_btn.addEventListener("click", function(){
	validate()
	form_2.style.display = "block";
	form_3.style.display = "none";
	form_2_btns.style.display = "flex";
	form_3_btns.style.display = "none";
	form_3_progessbar.classList.remove("active");
});

form_3_next_btn.addEventListener("click", function(){
	validate()
	var inputproductor = document.getElementById('nombreProductor').value
	var inputcoproductor = document.getElementById('nombreCoproductor').value
	var inputautor = document.getElementById('nombreAutor').value
	var inputeditor = document.getElementById('nombreEditor').value
	var inputdirector = document.getElementById('nombreDirector').value
	var inputcamara = document.getElementById('nombreCamara').value
	var inputsonido = document.getElementById('nombreSonido').value
	var inputconductor = document.getElementById('nombreConductor').value
	var inputprotagonista = document.getElementById('nombreProtagonista').value
	var inputcronista = document.getElementById('nombreCronista').value

	if (inputproductor.length == 0 || inputcoproductor.length  == 0 || inputautor.length == 0 || 
		inputeditor.length == 0 || inputdirector.length  == 0 || inputcamara.length  == 0 || 
		inputsonido.length == 0 || inputconductor.length  == 0 || inputprotagonista.length  == 0 || 
		inputcronista.length == 0){
		alert ("Complete los campos")
	}
	else{
		form_3.style.display = "none";
		form_4.style.display = "block";
		form_4_btns.style.display = "flex";
		form_3_btns.style.display = "none";
		form_4_progessbar.classList.add("active");
	}
});


form_4_back_btn.addEventListener("click", function(){
	validate()
	form_3.style.display = "block";
	form_4.style.display = "none";
	form_4_btns.style.display = "none";
	form_3_btns.style.display = "flex";
	form_4_progessbar.classList.remove("active");
});

form_4_next_btn.addEventListener("click", function(){
	var correo= /^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$/;

	validate()
	var inputnombrec= document.getElementById('nombreCanal').value
	var inputdireccionc = document.getElementById('direccionCanal').value
	var inputlocalidadc = document.getElementById('localidadCanal').value
	var inputcontactoc = document.getElementById('contactoCanal').value
	var inputtelefonoc = document.getElementById('telefonoCanal').value
	var inputemailc = document.getElementById('emailCanal').value
	var selectsos = document.getElementById('socioAet').value
	var correovalido = correo.test(inputemailc);

	if (inputnombrec.length == 0 || inputdireccionc.length == 0 || inputlocalidadc.length == 0 ||
		inputcontactoc .length == 0 || inputtelefonoc < 1000000 || correovalido == false ||
		selectsos == 0){
		alert ("Complete los campos")
	}
	else{
		form_4.style.display = "none";
		form_5.style.display = "block";
		form_5_btns.style.display = "flex";
		form_4_btns.style.display = "none";
		form_5_progessbar.classList.add("active");}
});

form_5_back_btn.addEventListener("click", function(){
	
	form_4.style.display = "block";
	form_5.style.display = "none";
	form_5_btns.style.display = "none";
	form_4_btns.style.display = "flex";
	form_5_progessbar.classList.remove("active");
});

btn_done.addEventListener("click", function(){
	var inputrazons = document.getElementById('razonSocial').value
	var inputcuit = document.getElementById('numeroCuit').value

	if (inputrazons.length == 0 || inputcuit < 20000000000){
		alert ("Complete los campos")
	}
	else{
		document.getElementById('form1').submit();
	}
})

shadow.addEventListener("click", function(){
	modal_wrapper.classList.remove("active");
})