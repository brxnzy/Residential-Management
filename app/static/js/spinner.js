function showLoader() {
    const spinner = document.getElementById('loading-spinner');
    if (spinner.style.display === 'none') {
        spinner.style.display = 'flex';
        document.body.classList.add('disable-interaction'); // Bloquea interacciones
    }
}

function hideLoader() {
    setTimeout(() => {
        const spinner = document.getElementById('loading-spinner');
        if (spinner.style.display !== 'none') {
            spinner.style.display = 'none';
            document.body.classList.remove('disable-interaction'); // Restaura interacciones
        }
    }, 500); // Agregar retraso de 500ms para no quitarlo tan rápido
}

// Mostrar el loader al cargar la página
window.addEventListener("load", function () {
    setTimeout(hideLoader, 1000); // Agregar retraso para evitar ocultarlo demasiado rápido
});

// Mostrar el loader al enviar formularios
document.querySelectorAll('form').forEach(form => {
    form.addEventListener('submit', function () {
        showLoader();
    });
});
