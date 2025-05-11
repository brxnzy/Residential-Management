const input = document.getElementById('logoInput');
const preview = document.getElementById('logoPreview');
const changeBtn = document.getElementById('changeLogoBtn');

input.addEventListener('change', (e) => {
  const file = e.target.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = function (event) {
      preview.src = event.target.result;
      changeBtn.classList.remove('hidden');
    };
    reader.readAsDataURL(file);
  }
});

document.getElementById("dropzone-file").addEventListener("change", function(event) {
    const file = event.target.files[0];
    const button = document.getElementById('bttn');
    button.classList.remove('hidden'); 
  
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            document.getElementById("user-photo").src = e.target.result;
        };
        reader.readAsDataURL(file);
    }
  });
  


function passwordValidation() {
    return {
        password: '',
        lengthValid: false,
        uppercaseValid: false,
        specialCharValid: false,
        isValid: false,
        validate() {
            this.lengthValid = this.password.length >= 10;
            this.uppercaseValid = /[A-Z]/.test(this.password);
            this.specialCharValid = /[!@#?()&$*]/.test(this.password);
            this.isValid = this.lengthValid && this.uppercaseValid && this.specialCharValid;
        }
    }
  }

  document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("myInfoForm");
    const inputs = form.querySelectorAll("input");
    const inputPhone = document.getElementById("phone");
    const submitButton = document.getElementById("submitButton");

    // Store original values
    const originalValues = {};
    inputs.forEach(input => {
        originalValues[input.name] = input.value;
    });

    function checkChanges() {
        let changed = false;

        // Check for changes
        inputs.forEach(input => {
            if (input.value !== originalValues[input.name]) {
                changed = true;
            }
        });

        // Format phone number
        let phoneValue = inputPhone.value.replace(/\D/g, ''); // Remove non-digits
        let formattedPhone = '';
        if (phoneValue.length > 0) formattedPhone += phoneValue.substring(0, 3);
        if (phoneValue.length > 3) formattedPhone += '-' + phoneValue.substring(3, 6);
        if (phoneValue.length > 6) formattedPhone += '-' + phoneValue.substring(6, 10);
        inputPhone.value = formattedPhone;

        // Validate phone (allow empty or complete format)
        let validPhone = phoneValue.length === 0 || /^\d{3}-\d{3}-\d{4}$/.test(formattedPhone);

        // Enable button if there are changes and phone is valid
        submitButton.disabled = !(changed && validPhone);
    }

    // Attach input event listeners
    inputs.forEach(input => {
        input.addEventListener("input", checkChanges);
    });

    // Initialize
    checkChanges();
});