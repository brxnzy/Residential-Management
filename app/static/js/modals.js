document.addEventListener("DOMContentLoaded", function () {
  const inputCedula = document.getElementById("id_card");
  const inputPhone = document.getElementById("phone");
  const button = document.getElementById("btn");
  const checkboxes = document.querySelectorAll(".checkbox-option"); // Selecciona los checkboxes

  function checkForm() {
    const isCedulaValid = /^\d{3}-\d{7}-\d{1}$/.test(inputCedula?.value || "");
    const isPhoneValid = /^\d{3}-\d{3}-\d{4}$/.test(inputPhone?.value || "");
    const isCheckboxChecked = Array.from(checkboxes).some(
      (checkbox) => checkbox.checked
    ); // Verifica si hay al menos un checkbox marcado

    if (isCedulaValid && isPhoneValid && isCheckboxChecked) {
      button.removeAttribute("disabled");
      button.classList.remove("cursor-not-allowed", "opacity-50");
      button.classList.add("cursor-pointer");
    } else {
      button.disabled = true
      button.classList.add("cursor-not-allowed", "opacity-50");
      button.classList.remove("cursor-pointer");
    }
  }

  if (inputCedula) {
    inputCedula.addEventListener("input", function (e) {
      let value = e.target.value.replace(/\D/g, "");
      if (value.length > 11) value = value.substring(0, 11);

      let formattedValue = "";
      if (value.length > 0) formattedValue += value.substring(0, 3);
      if (value.length > 3) formattedValue += "-" + value.substring(3, 10);
      if (value.length > 10) formattedValue += "-" + value.substring(10, 11);

      e.target.value = formattedValue;
      checkForm();
    });
  }

  if (inputPhone) {
    inputPhone.addEventListener("input", function (e) {
      let value = e.target.value.replace(/\D/g, "");
      if (value.length > 10) value = value.substring(0, 10);

      let formattedValue = "";
      if (value.length > 0) formattedValue += value.substring(0, 3);
      if (value.length > 3) formattedValue += "-" + value.substring(3, 6);
      if (value.length > 6) formattedValue += "-" + value.substring(6, 10);

      e.target.value = formattedValue;
      checkForm();
    });
  }

  // Agregar evento a los checkboxes
  checkboxes.forEach((checkbox) => {
    checkbox.addEventListener("change", checkForm);
  });

  checkForm();
});

document.querySelectorAll(".delete-user-btn").forEach((button) => {
  button.addEventListener("click", function () {
    // Obtener datos del botón
    const userName = this.getAttribute("data-user-name");
    const userLastName = this.getAttribute("data-user-lastname");
    const userImg = this.getAttribute("data-user-img");
    const userId = this.getAttribute("data-user-id");

    // Insertar datos en el modal
    document.getElementById(
      "modal-user-name"
    ).textContent = `${userName} ${userLastName}`;

    // Asignar la ruta correcta a la imagen del usuario
    document.getElementById("modal-user-img").src =
      "/static/uploads/" + userImg;

    // Actualizar la acción del formulario
    document.getElementById(
      "deleteForm"
    ).action = `/admin/delete_user/${userId}`;
  });
});

document.querySelectorAll(".enable-user-btn").forEach((button) => {
  button.addEventListener("click", function () {
    const userId = this.getAttribute("data-user-id");

    document.getElementById(
      "assignForm"
    ).action = `/admin/assign_property/${userId}`;
  });
});

document.addEventListener("DOMContentLoaded", function () {
  const checkbox = document.getElementById("residente-checkbox");
  const dropdownContainer = document.getElementById("Container");
  const propertyType = document.getElementById("Type");
  const propertyList = document.getElementById("List");

  // Guardamos si el usuario era residente al cargar la página
  const wasResidentInitially = checkbox.checked;

  if (checkbox && dropdownContainer && propertyType && propertyList) {
    checkbox.addEventListener("change", function () {
      if (!wasResidentInitially && this.checked) {
        // Solo mostrar dropdown si el usuario NO era residente antes
        dropdownContainer.classList.remove("hidden");
        propertyType.setAttribute("required", "required");
        propertyList.setAttribute("required", "required");
      } else {
        // Si ya era residente, impedir cambios en la vivienda
        dropdownContainer.classList.add("hidden");
        propertyType.removeAttribute("required");
        propertyList.removeAttribute("required");
        propertyType.value = "";
        propertyList.value = "";
        propertyList.classList.add("hidden");
        toggleOptions("");
      }
    });

    propertyType.addEventListener("change", function () {
      propertyList.classList.remove("hidden");
      toggleOptions(this.value);
      propertyList.value = "";
    });

    function toggleOptions(type) {
      const apartments = propertyList.querySelectorAll(".apartamentos");
      const houses = propertyList.querySelectorAll(".casas");

      apartments.forEach((option) => option.classList.add("hidden"));
      houses.forEach((option) => option.classList.add("hidden"));

      if (type === "apartamentos") {
        apartments.forEach((option) => option.classList.remove("hidden"));
      } else if (type === "casas") {
        houses.forEach((option) => option.classList.remove("hidden"));
      }
    }
  }
});

document.addEventListener("DOMContentLoaded", function () {
  const propertyType = document.getElementById("propertyType");
  const propertyList = document.getElementById("propertyList");

  if (propertyType && propertyList) {
    console.log("Elementos encontrados correctamente en el DOM.");

    propertyType.addEventListener("change", function () {
      const selectedType = this.value;
      console.log(`Tipo de propiedad seleccionado: ${selectedType}`);

      const allOptions = propertyList.querySelectorAll("option");
      let hasVisibleOption = false;

      // Resetear selección
      propertyList.value = "";
      console.log("Reseteando opciones del segundo select...");

      allOptions.forEach((option) => {
        if (option.classList.contains(selectedType)) {
          option.style.display = "block"; // Asegurar que se muestra
          hasVisibleOption = true;
          console.log(`Mostrando opción: ${option.textContent}`);
        } else if (option.value !== "") {
          option.style.display = "none"; // Ocultar la opción
          console.log(`Ocultando opción: ${option.textContent}`);
        }
      });

      // Mostrar u ocultar el select
      if (hasVisibleOption) {
        propertyList.classList.remove("hidden");
        console.log("Se muestran opciones disponibles.");
      } else {
        propertyList.classList.add("");
        console.log("No hay opciones disponibles, ocultando select.");
      }
    });
  } else {
    console.error("Error: No se encontraron los elementos en el DOM.");
  }
});




document.addEventListener("DOMContentLoaded", function () {
  let checkboxes = document.querySelectorAll(".checkbox-opt");
  let residentCheckbox = document.querySelector("#role-resident");
  let dropdownContainer = document.querySelector("#dropdownContainer");
  let submitButton = document.querySelector("#submitButton");
  let propertyType = document.querySelector("#propertyType");
  let propertyList = document.querySelector("#propertyList");

  function toggleDropdown() {
      let wasResident = residentCheckbox.getAttribute("data-original-resident") === "true";
      if (!wasResident && residentCheckbox.checked) {
          dropdownContainer.classList.remove("hidden");
      } else {
          dropdownContainer.classList.add("hidden");
      }
  }

  function toggleSubmitButton() {
      let anyChecked = Array.from(checkboxes).some(checkbox => checkbox.checked);
      submitButton.disabled = !anyChecked;
      submitButton.classList.toggle("cursor-not-allowed", !anyChecked);
      submitButton.classList.toggle("opacity-50", !anyChecked);
      submitButton.classList.toggle("cursor-pointer", anyChecked);
  }

  function updatePropertyList() {
      let selectedType = propertyType.value;
      let options = propertyList.querySelectorAll("option:not(:disabled)"); // Excluir la opción fija
      let hasAvailable = false;

      // Si no ha seleccionado nada, ocultar el segundo select
      if (!selectedType) {
          propertyList.classList.add("hidden");
          return;
      }

      // Ocultar todas las opciones primero
      options.forEach(option => {
          if (option.classList.contains(selectedType)) {
              option.classList.remove("hidden");
              hasAvailable = true;
          } else {
              option.classList.add("hidden");
          }
      });

      // Mostrar el select solo si hay una selección válida
      propertyList.classList.remove("hidden");

      // Asegurar que la opción "Residencias Disponibles" siempre esté presente
      propertyList.selectedIndex = 0;

      // Si no hay propiedades disponibles, mantener la opción por defecto

  }

  residentCheckbox.addEventListener("change", function () {
      toggleDropdown();
      toggleSubmitButton();
  });

  checkboxes.forEach(checkbox => {
      checkbox.addEventListener("change", toggleSubmitButton);
  });

  propertyType.addEventListener("change", updatePropertyList);

  // Ocultar el segundo select al cargar la página
  propertyList.classList.add("hidden");

  toggleDropdown();
  toggleSubmitButton();

  document.querySelector("form").addEventListener("submit", function (event) {
      if (submitButton.disabled) {
          event.preventDefault();
      }
  });
});



document.querySelectorAll(".vacate-btn").forEach((button) => {
  button.addEventListener("click", function () {
      const residenceId = this.getAttribute("data-residence-id");
      const residentId = this.getAttribute("data-resident-id");

      console.log("ID Capturado:", residenceId); 
      console.log("ID Capturado:", residentId); 

     
      document.getElementById("residenceId").value = residenceId;
      document.getElementById("residentId").value = residentId;
  });
});


