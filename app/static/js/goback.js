function goBack() {
    if (document.referrer) {
        window.history.back(); // Si hay una página anterior, regresa
    } else {
        window.location.href = "/"; // Si no hay historial, va al inicio
    }
}
