function togglePassword() {
    const passwordInput = document.getElementById('password');
    const eyeOpen = document.getElementById('eye-open');
    const eyeClosed = document.getElementById('eye-closed');

    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        eyeOpen.classList.add('hidden');
        eyeClosed.classList.remove('hidden');
    } else {
        passwordInput.type = 'password';
        eyeOpen.classList.remove('hidden');
        eyeClosed.classList.add('hidden');
    }
}



const inputCedula = document.getElementById('id_card');
const button = document.getElementById('btn');

if (inputCedula) {
    inputCedula.addEventListener('input', function (e) {
        // Eliminar caracteres no numéricos
        let value = e.target.value.replace(/\D/g, '');

        // Aplicar el formato: 123 - 4567891 - 1
        let formattedValue = '';

        if (value.length > 0) formattedValue += value.substring(0, 3);
        if (value.length > 3) formattedValue += '-' + value.substring(3, 10);
        if (value.length > 10) formattedValue += '-' + value.substring(10, 11);

        e.target.value = formattedValue;
        button.disabled = !/^\d{3}-\d{7}-\d{1}$/.test(formattedValue);
    });
    console.log(`Verificacion cedula: ${input.value}`);
}



    // Validar formato completo: XXX-XXXXXXX-X 

const inputPhone = document.getElementById('phone');


function validarTelefono() {
    // Eliminar caracteres no numéricos
    let value = inputPhone.value.replace(/\D/g, '');
    let formattedValue = '';

    if (value.length > 0) formattedValue += value.substring(0, 3);
    if (value.length > 3) formattedValue += '-' + value.substring(3, 6);
    if (value.length > 6) formattedValue += '-' + value.substring(6, 10);

    inputPhone.value = formattedValue;

    // Validar formato completo: XXX-XXX-XXXX
    button.disabled = !/^\d{3}-\d{3}-\d{4}$/.test(formattedValue);
}


inputPhone.addEventListener('input', validarTelefono);
inputCedula.addEventListener('input', validarCedula);

