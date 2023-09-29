var select = document.getElementById("tarjetas");
var boton = document.getElementById("boton_comprar");
var precio = document.getElementById("precio");

var nombre_2= document.getElementById("nombre_2");
var apellido_2= document.getElementById("apellido_2");
var dni_2= document.getElementById("dni_2");
var año_1= document.getElementById("año_1");
var año_2= document.getElementById("año_2");

date = new Date();
year = date.getFullYear();
 
select.addEventListener("change", function(){
    var tarjeta_1 = document.getElementById("tarjeta_1");
    var tarjeta_2 = document.getElementById("tarjeta_2");

    if (select.value  == 1){
        tarjeta_1.style.display = 'block';
        tarjeta_2.style.display = 'none';
        boton.style.display = 'block';
        precio.innerHTML = '$' + precio_tarjeta;
        nombre_2.removeAttribute("required");
        apellido_2.removeAttribute("required");
        dni_2.removeAttribute("required");
        año_1.value = year;
        año_2.value = '';
        año_1.readOnly ='true'
        
    }
    if (select.value  == 2){
        tarjeta_1.style.display = 'block';
        tarjeta_2.style.display = 'block';
        boton.style.display = 'block';
        precio.innerHTML = '$' + precio_tarjeta*2;
        nombre_2.required = 'true';
        apellido_2.required = 'true';
        dni_2.required = 'true';
        año_1.value = year;
        año_2.value = year;
        año_1.readOnly ='true'
        año_2.readOnly ='true'
        
    }
        
});


