


function updateAmount() {
    const checkboxes = document.querySelectorAll('#debtsContainer input[type="checkbox"]');
    const amountInput = document.getElementById('amount');
    let total = 0;

    checkboxes.forEach(checkbox => {
        if (checkbox.checked) {
            const amount = parseFloat(checkbox.dataset.amount);
            if (!isNaN(amount)) {
                total += amount;
            }
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
                    checkbox.setAttribute('data-amount', debt[4]); // Assuming debt[4] is the amount
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





document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.image-container').forEach(container => {
        const thumbnail = container.querySelector('.preview-img');
        
        if (!thumbnail) return;
        
        // Crear el overlay dinámicamente
        const overlay = document.createElement('div');
        overlay.style.position = 'fixed';
        overlay.style.top = '0';
        overlay.style.left = '0';
        overlay.style.width = '100%';
        overlay.style.height = '100%';
        overlay.style.background = 'rgba(0, 0, 0, 0.75)';
        overlay.style.display = 'none';
        overlay.style.alignItems = 'center';
        overlay.style.justifyContent = 'center';
        overlay.style.zIndex = '1000';
        
        const largeImage = document.createElement('img');
        largeImage.style.maxWidth = '90%';
        largeImage.style.maxHeight = '90%';
        largeImage.style.borderRadius = '8px';
        
        overlay.appendChild(largeImage);
        document.body.appendChild(overlay);
        
        thumbnail.addEventListener('click', () => {
            largeImage.src = thumbnail.src;
            overlay.style.display = 'flex';
            document.body.style.overflow = 'hidden';
        });
        
        overlay.addEventListener('click', (e) => {
            if (e.target === overlay) {
                overlay.style.display = 'none';
                document.body.style.overflow = '';
            }
        });
        
        document.addEventListener('keydown', (e) => {
            if (overlay.style.display === 'flex' && e.key === 'Escape') {
                overlay.style.display = 'none';
                document.body.style.overflow = '';
            }
        });
    });
});


function downloadInvoice(button) {
    // Obtener el ID desde el atributo data-payment-id
    const paymentId = button.getAttribute('data-payment-id');
    
    // Construir la ruta del archivo
    const filePath = `../../static/uploads/reports/payment_${paymentId}.pdf`;
    
    // Crear un enlace temporal para descargar el archivo
    const a = document.createElement('a');
    a.href = filePath;
    a.download = `payment_${paymentId}.pdf`; // Nombre del archivo al descargar
    document.body.appendChild(a);
    a.click();
    a.remove();
    
    console.log(`Descargando archivo: ${filePath}`);
}



document.addEventListener("DOMContentLoaded", function() {
    document.querySelectorAll("[data-modal-toggle='transfer-modal']").forEach(button => {
        button.addEventListener("click", function() {
            let userId = this.getAttribute("data-user-id");
            let transferId = this.getAttribute("data-transfer-id");
            let modal = document.getElementById("transfer-modal");

            let debtContainer = modal.querySelector("#debt-container"); // Donde se mostrarán las deudas
            let form = modal.querySelector("form"); 
            let submitButton = modal.querySelector("#submitButton"); // Obtener el botón de submit
            let months = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"];
            let userIdInput = modal.querySelector("#user_id");
            let transferIdInput = modal.querySelector("#transfer_id");

            userIdInput.value = userId; 
            transferIdInput.value = transferId; 

            // Limpiar el contenedor de deudas antes de agregar nuevas
            debtContainer.innerHTML = "";

            // Deshabilitar el botón de submit al abrir el modal
            submitButton.disabled = true;

            // Actualizar el `action` del formulario con el ID del usuario
            form.action = `/admin/payments/accept_transfer`;

            // Obtener las deudas del usuario desde el backend
            fetch(`/admin/payments/user_debts/${userId}`)
                .then(response => response.json())
                .then(debts => {
                    if (debts.length > 0) {
                        debts.forEach(debt => {
                            let div = document.createElement("div");
                            div.classList.add("flex", "items-center", "mb-4");

                            div.innerHTML = `
                                <input id="debt-${debt.id}" type="checkbox" name="debts" value="${debt.id}" class="debt-checkbox w-5 h-5 text-green-600 bg-gray-100 border-gray-300 rounded-sm focus:ring-green-500">
                                <label for="debt-${debt.id}" class="ml-2 text-l font-bold text-gray-900">
                                    ${months[debt.month - 1]} ${debt.period} - Monto: ${debt.amount}
                                </label>
                            `;
                            debtContainer.appendChild(div);
                        });

                        // Agregar evento a los checkboxes para habilitar/deshabilitar el botón
                        document.querySelectorAll(".debt-checkbox").forEach(checkbox => {
                            checkbox.addEventListener("change", function() {
                                let anyChecked = document.querySelectorAll(".debt-checkbox:checked").length > 0;
                                submitButton.disabled = !anyChecked;
                            });
                        });
                    } else {
                        debtContainer.innerHTML = `<p class="text-gray-500">No hay deudas pendientes.</p>`;
                    }
                })
                .catch(error => {
                    console.error("Error al obtener las deudas:", error);
                    debtContainer.innerHTML = `<p class="text-red-500">Error al cargar las deudas.</p>`;
                });
        });
    });
});



document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".reject-tr-btn").forEach(button => {
        button.addEventListener("click", function () {
            const trId = this.getAttribute("data-tr-id");
            const userId = this.getAttribute("data-user-id");
            console.log("ID de la transferencia:", trId);
            console.log("ID del user:", userId);
            
            // Aquí puedes pasar el ID al modal
            document.getElementById("reject-tr-input").value = trId;
            document.getElementById("user-id_input").value = userId;
        });
    });
});