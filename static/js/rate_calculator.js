// Obtener el modal
var modal = document.getElementById('rate-calculator-modal');

// Obtener el botón que abre el modal
var openBtn = document.getElementById('open-rate-calculator');

// Obtener el elemento <span> que cierra el modal
var closeBtn = document.getElementsByClassName('close')[0];

// Obtener los elementos del formulario
var rateType = document.getElementById('rate-type');
var periodicity = document.getElementById('periodicity');
var inputRate = document.getElementById('input-rate');
var calculateBtn = document.getElementById('calculate-rate');
var calculatedRate = document.getElementById('calculated-rate');
var acceptBtn = document.getElementById('accept-rate');
var interestRateInput = document.getElementById('id_interest_rate');

// Cuando el usuario hace clic en el icono de calculadora, abre el modal
openBtn.onclick = function(event) {
    event.preventDefault();
    modal.style.display = 'block';
}

// Cuando el usuario hace clic en la 'x', cierra el modal
closeBtn.onclick = function() {
    modal.style.display = 'none';
}

// Cuando el usuario hace clic fuera del modal, cierra el modal
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = 'none';
    }
}

// Función para calcular la tasa de interés anual
calculateBtn.onclick = function() {
    var rate = parseFloat(inputRate.value);
    var m = parseInt(periodicity.value);
    if (isNaN(rate) || rate <= 0) {
        alert('Por favor, ingrese una tasa válida.');
        return;
    }

    var annualRate;

    if (rateType.value === 'nominal') {
        // Tasa nominal a tasa efectiva anual
        annualRate = (Math.pow(1 + (rate / 100) / m, m) - 1) * 100;
    } else {
        // Tasa efectiva a anual (si no es anual)
        if (m !== 1) {
            annualRate = (Math.pow(1 + (rate / 100), 1 * m) - 1) * 100;
        } else {
            annualRate = rate;
        }
    }

    calculatedRate.value = annualRate.toFixed(4);
}

// Cuando el usuario hace clic en aceptar, establece la tasa calculada en el campo de tasa de interés
acceptBtn.onclick = function() {
    if (calculatedRate.value === '') {
        alert('Primero calcula la tasa.');
        return;
    }
    interestRateInput.value = calculatedRate.value;
    modal.style.display = 'none';
} 