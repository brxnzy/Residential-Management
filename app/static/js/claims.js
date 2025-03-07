document.addEventListener('DOMContentLoaded', function () {
    const dateInput = document.getElementById('maintenance-date');
    const startTimeInput = document.getElementById('start-time');
    const endTimeInput = document.getElementById('end-time');
    const descriptionInput = document.getElementById('maintenance-description');
    const saveButton = document.getElementById('save-button');
    const form = document.getElementById('maintenance-form');

    // Helper: Get current time as a string (HH:MM format)
    function getCurrentTimeStr() {
        const now = new Date();
        const hours = now.getHours().toString().padStart(2, '0');
        const minutes = (Math.ceil(now.getMinutes() / 5) * 5 % 60).toString().padStart(2, '0');
        return `${hours}:${minutes}`;
    }

    // Helper: Convert time string to Date object for comparison
    function timeToDate(dateStr, timeStr) {
        const [hours, minutes] = timeStr.split(':').map(Number);
        const date = new Date(dateStr);
        date.setHours(hours, minutes, 0, 0);
        return date;
    }

    // Set default values
    function setDefaultValues() {
        const now = new Date();
        const today = now.toISOString().split('T')[0];
        dateInput.value = today;
        dateInput.min = today;

        const currentTimeStr = getCurrentTimeStr();
        startTimeInput.value = currentTimeStr;
        startTimeInput.min = currentTimeStr; // Prevent past times for today

        const endTime = new Date(now);
        endTime.setMinutes(endTime.getMinutes() + 30);
        endTimeInput.value = endTime.toTimeString().slice(0, 5);
        endTimeInput.min = currentTimeStr; // Ensure end time is after start
    }

    // Validate and enforce constraints
    function enforceConstraints() {
        const now = new Date();
        const selectedDate = new Date(dateInput.value);
        const todayStr = now.toISOString().split('T')[0];
        const isToday = selectedDate.toDateString() === new Date(todayStr).toDateString();

        // Validate date (must be today or future)
        if (selectedDate < new Date(todayStr)) {
            dateInput.value = todayStr;
            dateInput.setCustomValidity('La fecha no puede ser anterior a hoy');
        } else {
            dateInput.setCustomValidity('');
        }

        // Validate start time (no past times for today)
        const currentTimeStr = getCurrentTimeStr();
        startTimeInput.min = isToday ? currentTimeStr : '00:00';
        const startDateTime = timeToDate(dateInput.value, startTimeInput.value);
        if (isToday && startDateTime < now) {
            startTimeInput.value = currentTimeStr; // Automatically correct to current time
            startTimeInput.setCustomValidity('La hora de inicio no puede ser anterior a la hora actual');
        } else {
            startTimeInput.setCustomValidity('');
        }

        // Validate end time (must be after start time)
        endTimeInput.min = startTimeInput.value;
        const endDateTime = timeToDate(dateInput.value, endTimeInput.value);
        if (endDateTime <= startDateTime) {
            const newEndTime = new Date(startDateTime);
            newEndTime.setMinutes(newEndTime.getMinutes() + 30);
            endTimeInput.value = newEndTime.toTimeString().slice(0, 5); // Automatically correct
            endTimeInput.setCustomValidity('La hora de fin debe ser posterior a la hora de inicio');
        } else {
            endTimeInput.setCustomValidity('');
        }

        // Optional: Validate description (can be empty, no custom validity needed)
        descriptionInput.setCustomValidity('');
    }

    // Event listeners for real-time validation
    dateInput.addEventListener('input', enforceConstraints);
    startTimeInput.addEventListener('input', enforceConstraints);
    endTimeInput.addEventListener('input', enforceConstraints);
    descriptionInput.addEventListener('input', enforceConstraints); // For consistency, though optional

    // Form submission
    form.addEventListener('submit', function (e) {
        e.preventDefault();
        enforceConstraints(); // Final validation and correction
        console.log('Maintenance scheduled:', {
            date: dateInput.value,
            startTime: startTimeInput.value,
            endTime: endTimeInput.value,
            description: descriptionInput.value
        });
    });

    // Initialize
    setDefaultValues();
    enforceConstraints();
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