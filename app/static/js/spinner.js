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
        // Verificar si es el formulario de pago en efectivo
        const isPaymentForm = form.getAttribute('action') && 
                             form.getAttribute('action').includes('/admin/payments/cash_payment');
        
        form.addEventListener('submit', function(event) {
            event.preventDefault(); // Evitar envío inmediato
            showLoader();

            // Si es el formulario de pago, configurar un temporizador para verificar la cookie
            if (isPaymentForm) {
                // Guardar el formulario para usarlo en el intervalo
                const paymentForm = this;
                
                // Enviar el formulario normalmente
                setTimeout(() => {
                    console.log('✅ Enviando formulario de pago...');
                    paymentForm.submit();
                    
                    // Configurar un intervalo para verificar la cookie después de enviar el formulario
                    const checkCookie = setInterval(() => {
                        if (document.cookie.indexOf('payment_downloaded=true') !== -1) {
                            // Limpiar la cookie
                            document.cookie = 'payment_downloaded=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
                            clearInterval(checkCookie);
                            
                            // Ocultar el loader inmediatamente
                            hideLoader();
                            
                            // Pequeña pausa antes de redirigir para asegurar que el spinner desaparezca
                            setTimeout(() => {
                                window.location.href = '/admin/payments';
                            },1);
                        }
                    }, 500); // Verificar cada medio segundo en lugar de cada segundo
                    
                    // Reducir el tiempo máximo de espera a 8 segundos
                    setTimeout(() => {
                        clearInterval(checkCookie);
                        hideLoader();
                    }, 8000);
                }, 500);
            } else {
                // Para otros formularios, comportamiento normal
                setTimeout(() => {
                    console.log('✅ Enviando formulario...');
                    form.submit();
                }, 500);
            }
        });
    });
});

window.addEventListener("load", function () {
    setTimeout(hideLoader, 1000);
});