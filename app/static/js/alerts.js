document.addEventListener("DOMContentLoaded", function() {
    const flashMessagesElement = document.getElementById("flash-messages");
    if (flashMessagesElement) {
        const messages = JSON.parse(flashMessagesElement.getAttribute("data-messages"));
        messages.forEach(([category, message]) => {
            showAlert(message, category);
        });
    }
});

function showAlert(message, type = "success") {
    const alertContainer = document.getElementById("alert-container");

    // Crear la alerta
    const alert = document.createElement("div");
    alert.className = `flex items-center space-x-3 px-4 py-3 rounded-lg shadow-lg transition-all duration-300 transform 
                       translate-x-4 opacity-0 text-white ${
                         type === "success" ? "bgverde" :
                         type === "error" ? "bg-red-500" :
                         type === "warning" ? "bg-yellow-500 text-black" :
                         "bg-blue-500" // info
                       }`;

    // Iconos SVG dinámicos según el tipo de alerta
    const iconSVG = {
      success: `<svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" stroke-width="2"
                     viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                     <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"></path>
                 </svg>`,
      error: `<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6 text-red-500">
                <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
              </svg>`,
      warning: `<svg class="w-6 h-6 text-black" fill="none" stroke="currentColor" stroke-width="2"
                     viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                     <path stroke-linecap="round" stroke-linejoin="round" d="M12 8v4m0 4h.01"></path>
                     <path stroke-linecap="round" stroke-linejoin="round" d="M5 12h14M12 3l7 7-7 7-7-7 7-7z"></path>
                 </svg>`,
      info: `<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6 text-blue-500">
               <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v3.75M12 15h.008v.008H12V15ZM12 3a9 9 0 1 1-9 9 9 9 0 0 1 9-9Z" />
             </svg>`
    };
    

    alert.innerHTML = `
      ${iconSVG[type]}
      <span>${message}</span>
      <button onclick="this.parentElement.remove()" class="ml-2 text-lg font-bold">&times;</button>
    `;

    // Agregar la alerta al contenedor
    alertContainer.appendChild(alert);

    // Mostrar con animación
    setTimeout(() => {
      alert.classList.remove("translate-x-4", "opacity-0");
    }, 100);

    // Eliminar la alerta después de 3 segundos
    setTimeout(() => {
      alert.classList.add("opacity-0", "translate-x-4");
      setTimeout(() => alert.remove(), 300);
    }, 3000);
}
