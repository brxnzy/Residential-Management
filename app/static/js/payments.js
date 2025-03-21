


function updateAmount() {
    const checkboxes = document.querySelectorAll('#debtsContainer input[type="checkbox"]');
    const amountInput = document.getElementById('amount');
    let total = 0;

    console.log("Checkboxes found:", checkboxes.length); // Debug
    checkboxes.forEach(checkbox => {
        if (checkbox.checked) {
            total += 1500; // Replace with dynamic value if needed
        }
    });

    amountInput.value = total.toFixed(2);
}

try {
    console.log("Inicializando script...");

    const form = document.getElementById('paymentForm');
    const debtsData = JSON.parse(form.getAttribute('data-debts'));

    console.log("Deudas cargadas desde el dataset:", debtsData);

    function filterDebts() {
        try {
            console.log("Ejecutando filterDebts...");
            const residentSelect = document.getElementById('resident');
            const selectedResidentId = Number(residentSelect.value);
            const btn = form.querySelector('button[type="submit"]');


            console.log("Residente seleccionado:", selectedResidentId);

            const debtsContainer = document.getElementById('debtsContainer');
            debtsContainer.innerHTML = ''; // Clear container

            if (!selectedResidentId) {
                console.warn("Ningún residente seleccionado.");
                return;
            }

            const filteredDebts = debtsData.filter(debt => debt[1] === selectedResidentId);

            console.log("Deudas encontradas:", filteredDebts);

            if (filteredDebts.length > 0) {
                const debtsDiv = document.createElement('div');
                debtsDiv.className = 'mb-4';

                filteredDebts.forEach(debt => {
                    console.log("Procesando deuda:", debt);

                    const debtDiv = document.createElement('div');
                    debtDiv.className = 'flex items-center mb-2';

                    const checkbox = document.createElement('input');
                    checkbox.type = 'checkbox';
                    checkbox.id = `debt-${debt[0]}`; // Assuming debt[0] is the ID
                    checkbox.value = debt[0];
                    checkbox.name = 'deudas'
                    checkbox.className = 'w-5 h-5 text-green-600 bg-gray-100 border-gray-300 rounded-sm focus:ring-green-500 dark:focus:ring-green-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600';
                    checkbox.addEventListener('change', updateAmount); // Add listener here

                    const label = document.createElement('label');
                    label.htmlFor = `debt-${debt[0]}`;
                    label.className = 'ml-2 text-l font-bold text-gray-900 dark:text-gray-300';

                    const date = new Date(debt[2], debt[3] - 1); // Year, Month (0-based)
                    const monthName = date.toLocaleString('es-ES', { month: 'long' });
                    const capitalizedMonth = monthName.charAt(0).toUpperCase() + monthName.slice(1);
                    label.textContent = `${capitalizedMonth}-${debt[2]}`;

                    debtDiv.appendChild(checkbox);
                    debtDiv.appendChild(label);
                    debtsDiv.appendChild(debtDiv);
                });

                debtsContainer.appendChild(debtsDiv);
            } else {
                const noDebtsMessage = document.createElement('p');
                noDebtsMessage.className = ' text-gray-800 font-medium';
                noDebtsMessage.textContent = "El residente no debe.";
                debtsContainer.appendChild(noDebtsMessage)
               
                
                console.warn("No hay deudas para este residente.");
            }

            updateAmount(); // Initial call after rendering
        } catch (error) {
            console.error("Error en filterDebts:", error);
        }
    }

    // Attach event listener to resident select to trigger filterDebts
    document.getElementById('resident').addEventListener('change', filterDebts);

} catch (error) {
    console.error("Error en la inicialización del script:", error);
}

if (document.cookie.indexOf('payment_downloaded=true') !== -1) {
    // Eliminar la cookie
    document.cookie = 'payment_downloaded=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
    // Redirigir a la ruta payment_complete
    window.location.href = "{{ url_for('payment_complete') }}";
}