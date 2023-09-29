var select = document.getElementById("tarjetas");
var boton = document.getElementById("boton_comprar");
var precio = document.getElementById("precio");
 
select.addEventListener("change", function(){
    var tarjeta_1 = document.getElementById("tarjeta_1");
    var tarjeta_2 = document.getElementById("tarjeta_2");

    if (select.value  == 1){
        tarjeta_1.style.display = 'block';
        tarjeta_2.style.display = 'none';
        boton.style.display = 'block';
        precio.innerHTML = "<h4><b>$3.000</b></h4>";
    }
    if (select.value  == 2){
        tarjeta_1.style.display = 'block';
        tarjeta_2.style.display = 'block';
        boton.style.display = 'block';
        precio.innerHTML = "<h4><b>$6.000</b></h4>";
    }
        
});


