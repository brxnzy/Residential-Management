const form = document.getElementById('claim-form');
const claimDateInput = document.getElementById('claim-date');
const startTimeInput = document.getElementById('start-time');
const claimDateError = document.getElementById('claim-date-error');
const startTimeError = document.getElementById('start-time-error');
const saveButton = document.getElementById('save-button'); 

// Función para formatear hora a HH:MM
function formatTime(date) {
    return date.toTimeString().slice(0, 5); 
}

// Establecer valores por defecto
function setDefaultValues() {
    const today = new Date(new Date().toLocaleString("en-US", { timeZone: "America/Santo_Domingo" }));
    const year = today.getFullYear();
    const month = String(today.getMonth() + 1).padStart(2, '0');
    const day = String(today.getDate()).padStart(2, '0');
    const currentDate = `${year}-${month}-${day}`; // Formato YYYY-MM-DD

    const currentTime = new Date(today.getTime() + 5 * 60000); // +10 minutos

    claimDateInput.value = currentDate;
    if (claimDateInput.value === currentDate) {
        startTimeInput.value = formatTime(currentTime);
    } else {
        startTimeInput.value = '08:00';
    }
}

// Función para mostrar errores
function showError(element, message) {
    element.textContent = message;
    element.classList.remove('hidden');
}

function hideError(element) {
    element.textContent = '';
    element.classList.add('hidden');
}

// Función de validación
function validateForm() {
    let isValid = true;

    // Obtener la fecha y hora actuales en la zona horaria de Santo Domingo
    const now = new Date().toLocaleString("es-ES", { timeZone: "America/Santo_Domingo" });
    const dateParts = now.split(",")[0].split("/");
    const currentDate = `${dateParts[2]}-${dateParts[1].padStart(2, "0")}-${dateParts[0].padStart(2, "0")}`;
    const today = new Date();
    const currentTime = formatTime(today);

    const claimDate = claimDateInput.value;
    const startTime = startTimeInput.value;

    // Resetear errores
    hideError(claimDateError);
    hideError(startTimeError);

    // Validación 1: La fecha no puede ser anterior a hoy
    if (claimDate < currentDate) {
        showError(claimDateError, 'La fecha no puede ser anterior a hoy.');
        isValid = false;
    }

    // Validación 2: Campos completos y formato válido
    if (!claimDate || !startTime) {
        if (!claimDate) showError(claimDateError, 'Seleccione una fecha.');
        if (!startTime) showError(startTimeError, 'Seleccione una hora de inicio.');
        isValid = false;
    } else {
        // Validación 3: Horario permitido (08:00-20:00)
        const minTime = '08:00';
        const maxTime = '20:00';
        if (startTime < minTime || startTime > maxTime) {
            showError(startTimeError, 'La hora debe estar entre 08:00 y 20:00.');
            isValid = false;
        }

        // Validación 4: Si es hoy, hora de inicio no anterior a la actual
        if (claimDate === currentDate && startTime < currentTime) {
            showError(startTimeError, 'La hora de inicio no puede ser anterior a la actual.');
            isValid = false;
        }
    }

    // Habilitar o deshabilitar el botón según la validez
    saveButton.disabled = !isValid;

    return isValid;
}

// Inicializar valores por defecto al cargar la página
setDefaultValues();
validateForm(); // Validar al cargar para establecer el estado inicial del botón

// Validación y ajustes en tiempo real
claimDateInput.addEventListener('input', () => {
    const today = new Date().toLocaleString("en-US", { timeZone: "America/Santo_Domingo" });
    const currentDate = today.split('T')[0];
    const nowPlus10 = new Date(new Date().getTime() + 10 * 60000);
    if (claimDateInput.value === currentDate) {
        startTimeInput.value = formatTime(nowPlus10);
    } else {
        startTimeInput.value = '08:00';
    }
    validateForm();
});

startTimeInput.addEventListener('input', validateForm);

// Validación al enviar el formulario
form.addEventListener('submit', function (event) {
    event.preventDefault(); // Prevenir el envío por defecto
    if (validateForm()) {
        console.log('Formulario válido, enviando...');
        this.submit(); // Enviar solo si es válido
    } else {
        console.log('Formulario no enviado debido a errores.');
    }
});






document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".attend-claim-btn").forEach(button => {
        button.addEventListener("click", function () {
            const claimId = this.getAttribute("data-claim-id");
            console.log("ID del reclamo:", claimId);
            
            // Aquí puedes pasar el ID al modal
            document.getElementById("claim-id-input").value = claimId;
        });
    });
});

document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".reject-claim-btn").forEach(button => {
        button.addEventListener("click", function () {
            const claimId = this.getAttribute("data-claim-id");
            console.log("ID del reclamo:", claimId);
            
            // Aquí puedes pasar el ID al modal
            document.getElementById("reject-id-input").value = claimId;
        });
    });
});


document.addEventListener('DOMContentLoaded', () => {
    // Crear overlay para imagen grande
    const showMoreBtn = document.getElementById("show-more-btn");
    if (showMoreBtn) {
        showMoreBtn.addEventListener("click", () => {
            const hiddenClaims = document.querySelectorAll(".additional-claim");
            const isHidden = hiddenClaims[0].classList.contains("hidden");

            hiddenClaims.forEach(claim => {
                claim.classList.toggle("hidden");
            });

            showMoreBtn.textContent = isHidden ? "Ocultar Historial" : "Ver Historial";
        });
    }
    const overlay = document.createElement('div');
    overlay.id = 'imageOverlay';
    overlay.style.cssText = `
        display: none;
        position: fixed;
        inset: 0;
        background-color: rgba(0, 0, 0, 0.8);
        z-index: 1000;
        align-items: center;
        justify-content: center;
        flex-direction: column;
    `;

    // Imagen ampliada
    const largeImage = document.createElement('img');
    largeImage.style.cssText = `
        max-width: 90%;
        max-height: 90%;
        object-fit: contain;
    `;

    // Botones de navegación
    const prevBtn = document.createElement('button');
    const nextBtn = document.createElement('button');

    [prevBtn, nextBtn].forEach(btn => {
        btn.style.cssText = `
            position: absolute;
            top: 50%;
            transform: translateY(-50%);
            background: rgba(0, 0, 0, 0.5);
            color: white;
            border: none;
            padding: 10px 15px;
            font-size: 18px;
            cursor: pointer;
            border-radius: 5px;
        `;
    });

    prevBtn.textContent = '←';
    nextBtn.textContent = '→';
    prevBtn.style.left = '20px';
    nextBtn.style.right = '20px';

    overlay.appendChild(prevBtn);
    overlay.appendChild(largeImage);
    overlay.appendChild(nextBtn);
    document.body.appendChild(overlay);

    let currentIndex = 0;
    let currentImages = [];

    // Mostrar imagen grande al hacer clic
    document.querySelectorAll('.thumbnails').forEach(thumbnailContainer => {
        const images = Array.from(thumbnailContainer.querySelectorAll('.thumbnail-img'));

        images.forEach((img, index) => {
            img.addEventListener('click', () => {
                currentIndex = index;
                currentImages = images.map(img => img.src);
                updateImage();
                overlay.style.display = 'flex';
                document.body.style.overflow = 'hidden';
            });
        });
    });

    function updateImage() {
        largeImage.src = currentImages[currentIndex];
        prevBtn.style.display = currentIndex > 0 ? 'block' : 'none';
        nextBtn.style.display = currentIndex < currentImages.length - 1 ? 'block' : 'none';
    }

    // Navegar entre imágenes
    prevBtn.addEventListener('click', () => {
        if (currentIndex > 0) {
            currentIndex--;
            updateImage();
        }
    });

    nextBtn.addEventListener('click', () => {
        if (currentIndex < currentImages.length - 1) {
            currentIndex++;
            updateImage();
        }
    });

    // Cerrar overlay
    overlay.addEventListener('click', (e) => {
        if (e.target === overlay) {
            overlay.style.display = 'none';
            document.body.style.overflow = '';
        }
    });

    // Navegar con el teclado
    document.addEventListener('keydown', (e) => {
        if (overlay.style.display === 'flex') {
            if (e.key === 'Escape') {
                overlay.style.display = 'none';
                document.body.style.overflow = '';
            } else if (e.key === 'ArrowLeft' && currentIndex > 0) {
                currentIndex--;
                updateImage();
            } else if (e.key === 'ArrowRight' && currentIndex < currentImages.length - 1) {
                currentIndex++;
                updateImage();
            }
        }
    });
});