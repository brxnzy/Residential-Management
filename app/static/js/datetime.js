document.addEventListener('DOMContentLoaded', function () {
    // Get elements
    const dateInput = document.getElementById('maintenance-date');
    const startTimeInput = document.getElementById('start-time');
    const endTimeInput = document.getElementById('end-time');
    const saveButton = document.getElementById('save-button');
    const form = document.getElementById('maintenance-form');

    // Set default values
    function setDefaultValues() {
        const now = new Date();

        // Set today's date
        const today = now.toISOString().split('T')[0];
        dateInput.value = today;
        dateInput.min = today;

        // Set current time as start time (rounded to nearest 5-minute interval)
        let hours = now.getHours().toString().padStart(2, '0');
        let minutes = Math.ceil(now.getMinutes() / 5) * 5;
        if (minutes === 60) {
            hours = (parseInt(hours) + 1).toString().padStart(2, '0');
            minutes = '00';
        }
        startTimeInput.value = `${hours}:${minutes}`;
        startTimeInput.min = `${hours}:${minutes}`;

        // Set end time 30 minutes later
        now.setMinutes(now.getMinutes() + 30);
        hours = now.getHours().toString().padStart(2, '0');
        minutes = Math.ceil(now.getMinutes() / 5) * 5;
        if (minutes === 60) {
            hours = (parseInt(hours) + 1).toString().padStart(2, '0');
            minutes = '00';
        }
        endTimeInput.value = `${hours}:${minutes}`;
        endTimeInput.min = startTimeInput.value;
    }

    // Validation function
    function validateInputs() {
        const now = new Date();
        const selectedDate = new Date(dateInput.value);
        const [startHours, startMinutes] = startTimeInput.value.split(':').map(Number);
        const [endHours, endMinutes] = endTimeInput.value.split(':').map(Number);

        // Convert to comparable dates
        const startDateTime = new Date(selectedDate);
        startDateTime.setHours(startHours, startMinutes, 0, 0);

        const endDateTime = new Date(selectedDate);
        endDateTime.setHours(endHours, endMinutes, 0, 0);

        let isValid = true;

        // Check if date is not in the past or unreasonably far in the future
        const todayStart = new Date(now.setHours(0, 0, 0, 0));
        const maxFutureDate = new Date();
        maxFutureDate.setFullYear(todayStart.getFullYear() + 10); // Limit to 10 years in future

        if (selectedDate < todayStart || selectedDate > maxFutureDate) {
            dateInput.value = todayStart.toISOString().split('T')[0]; // Reset to today immediately
            dateInput.setCustomValidity('La fecha debe estar entre hoy y 10 años en el futuro');
            isValid = false;
        } else {
            dateInput.setCustomValidity('');
        }

        // Validate start time (prevent past times on today)
        if (selectedDate.toDateString() === todayStart.toDateString()) {
            const currentTime = new Date();
            currentTime.setSeconds(0, 0); // Normalize to avoid second-level discrepancies
            if (startDateTime < currentTime) {
                const hours = currentTime.getHours().toString().padStart(2, '0');
                const minutes = Math.ceil(currentTime.getMinutes() / 5) * 5;
                startTimeInput.value = `${hours}:${minutes.toString().padStart(2, '0')}`;
                startTimeInput.setCustomValidity('La hora de inicio no puede ser anterior a la hora actual');
                isValid = false;
            } else {
                startTimeInput.setCustomValidity('');
            }
        } else {
            startTimeInput.setCustomValidity('');
        }

        // Validate end time (must be after start time)
        if (endDateTime <= startDateTime) {
            const newEndTime = new Date(startDateTime);
            newEndTime.setMinutes(newEndTime.getMinutes() + 30);
            endTimeInput.value = newEndTime.toTimeString().slice(0, 5);
            endTimeInput.setCustomValidity('La hora de fin debe ser posterior a la hora de inicio');
            isValid = false;
        } else {
            endTimeInput.setCustomValidity('');
        }

        // Update min attributes dynamically
        dateInput.min = todayStart.toISOString().split('T')[0];
        if (selectedDate.toDateString() === todayStart.toDateString()) {
            const currentTime = new Date();
            const hours = currentTime.getHours().toString().padStart(2, '0');
            const minutes = Math.ceil(currentTime.getMinutes() / 5) * 5;
            startTimeInput.min = `${hours}:${minutes.toString().padStart(2, '0')}`;
        } else {
            startTimeInput.min = '00:00';
        }
        endTimeInput.min = startTimeInput.value;

        saveButton.disabled = !isValid;
        return isValid;
    }

    // Add input event listeners
    dateInput.addEventListener('input', validateInputs);
    startTimeInput.addEventListener('input', validateInputs);
    endTimeInput.addEventListener('input', validateInputs);

    // Form submission
    form.addEventListener('submit', function (e) {
        e.preventDefault();
        if (validateInputs()) {
            console.log('Maintenance scheduled:', {
                date: dateInput.value,
                startTime: startTimeInput.value,
                endTime: endTimeInput.value,
            });
        }
    });

    // Initialize
    setDefaultValues();
    validateInputs();
});