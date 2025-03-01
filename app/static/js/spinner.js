function showLoader() {
    const loader = document.getElementById('loading-container');

    if (loader.style.display === 'flex') {
        console.log('⚠️ Loader ya está activo.');
        return;
    }

    console.log('✅ Mostrando Loader...');
    loader.style.display = 'flex';
    document.body.classList.add('disable-interaction'); // Bloquear interacciones
}

function hideLoader() {
    console.log('⏳ Ocultando Loader...');
    document.getElementById('loading-container').style.display = 'none';
    document.body.classList.remove('disable-interaction');
}

document.addEventListener("DOMContentLoaded", function() { 
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function(event) {
            event.preventDefault(); // Evitar envío inmediato
            showLoader();

            setTimeout(() => {
                console.log('✅ Enviando formulario...');
                form.submit(); // Enviar el formulario después de 5 segundos
            }, 500);
        });
    });
});

window.addEventListener("load", function () {
    setTimeout(hideLoader, 1000);
});