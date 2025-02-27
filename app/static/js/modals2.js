document.addEventListener("DOMContentLoaded", function () {
    const residentCheckbox = document.getElementById("residente-checkbox");
    const dropdownContainer = document.getElementById("Container");
    const propertyType = document.getElementById("Type");
    const propertyList = document.getElementById("List");

    console.log("residentCheckbox:", residentCheckbox);
    console.log("dropdownContainer:", dropdownContainer);
    console.log("propertyType:", propertyType);
    console.log("propertyList:", propertyList);

    residentCheckbox.addEventListener("change", function () {
        console.log("Checkbox changed. Checked:", this.checked);
        if (this.checked) {
            dropdownContainer.classList.remove("hidden");
        } else {
            dropdownContainer.classList.add("hidden");
            propertyType.value = "";
            propertyList.classList.add("hidden");
        }
    });

    propertyType.addEventListener("change", function () {
        console.log("Property Type changed:", this.value);
        const selectedType = this.value;
        const allOptions = propertyList.querySelectorAll("option");

        allOptions.forEach(option => {
            option.hidden = option.value !== "" && !option.classList.contains(selectedType);
        });

        if (selectedType) {
            propertyList.classList.remove("hidden");
        } else {
            propertyList.classList.add("hidden");
        }
    });
});
