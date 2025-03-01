document.getElementById("dropzone-file").addEventListener("change", function(event) {
    const file = event.target.files[0];
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