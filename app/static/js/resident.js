function filterNotifications() {
  const filter = document.getElementById('notification-filter').value;
  const notifications = document.querySelectorAll('.notification-item');
  let hasVisible = false;

  notifications.forEach(notification => {
    const status = notification.getAttribute('data-status');
    const isVisible = filter === 'all' || filter === status;
    
    notification.classList.toggle('hidden', !isVisible);
    if (isVisible) hasVisible = true;
  });

  // Mostrar mensaje si no hay notificaciones visibles
  document.getElementById('no-notifications-message').classList.toggle('hidden', hasVisible);
}

document.addEventListener('DOMContentLoaded', function() {
  const filterDropdown = document.getElementById('notification-filter');
  filterDropdown.value = 'unread';
  filterNotifications();
  filterDropdown.addEventListener('change', filterNotifications);
});

// Marcar como leído sin recargar la página


function updateNotificationCounts() {
  const unreadCount = document.querySelectorAll('.notification-item[data-status="unread"]').length;
  const readCount = document.querySelectorAll('.notification-item[data-status="read"]').length;
  const totalCount = unreadCount + readCount;

  document.querySelector('option[value="unread"]').textContent = `Sin leer (${unreadCount})`;
  document.querySelector('option[value="read"]').textContent = `Leídas (${readCount})`;
  document.querySelector('option[value="all"]').textContent = `Todas (${totalCount})`;

  filterNotifications(); // Verificar si se debe mostrar el mensaje de "No hay notificaciones"
}



document.addEventListener('DOMContentLoaded', () => {
    const tabButtons = document.querySelectorAll('.tab-button');
    const tabContents = document.querySelectorAll('.tab-content');
    
    tabButtons.forEach(button => {
    button.addEventListener('click', () => {
      // Remove active class from all buttons and contents
      tabButtons.forEach(btn => btn.classList.remove('active'));
      tabContents.forEach(content => content.classList.remove('active'));
    
      // Add active class to clicked button and corresponding content
      button.classList.add('active');
      const tabId = button.getAttribute('data-tab');
      document.getElementById(tabId).classList.add('active');
    });
    });
    
    // New complaint form toggle
    const newComplaintBtn = document.getElementById('new-complaint-btn');
    const complaintForm = document.getElementById('complaint-form');
    const cancelComplaintBtn = document.getElementById('cancel-complaint-btn');
    
    if (newComplaintBtn && complaintForm && cancelComplaintBtn) {
    newComplaintBtn.addEventListener('click', () => {
      complaintForm.classList.remove('hidden');
    });
    
    cancelComplaintBtn.addEventListener('click', () => {
      complaintForm.classList.add('hidden');
    });
    }
    });
    
    
    
    
    document.getElementById("dropzone-file").addEventListener("change", function(event) {
      const file = event.target.files[0];
      const button = document.getElementById('btn');
      button.classList.remove('hidden'); 
    
      if (file) {
          const reader = new FileReader();
          reader.onload = function(e) {
              document.getElementById("user-photo").src = e.target.result;
          };
          reader.readAsDataURL(file);
      }
    });
    
    
    
    
    document.addEventListener("DOMContentLoaded", function () {
      const form = document.getElementById("myInfoForm");
      const inputs = form.querySelectorAll("input");
      const inputPhone = document.getElementById("phone");
      const submitButton = document.getElementById("submitButton");
    
      // Guarda los valores originales usando el atributo "name"
      const originalValues = {};
      inputs.forEach(input => {
          originalValues[input.name] = input.value;
      });
    
      function checkChanges() {
          let changed = false;
    
          // Verifica si algún input ha cambiado
          inputs.forEach(input => {
              if (input.value !== originalValues[input.name]) {
                  changed = true;
              }
          });
    
          // Formatea el número de teléfono
          let phoneValue = inputPhone.value.replace(/\D/g, '');
          let formattedPhone = '';
          if (phoneValue.length > 0) formattedPhone += phoneValue.substring(0, 3);
          if (phoneValue.length > 3) formattedPhone += '-' + phoneValue.substring(3, 6);
          if (phoneValue.length > 6) formattedPhone += '-' + phoneValue.substring(6, 10);
          inputPhone.value = formattedPhone;
    
          // Validar que el teléfono tenga el formato correcto
          let validPhone = /^\d{3}-\d{3}-\d{4}$/.test(formattedPhone);
    
          // Habilita el botón solo si hay cambios y el teléfono es válido
          submitButton.disabled = !(changed && validPhone);
      }
    
      // Agrega eventos de escucha a cada input
      inputs.forEach(input => {
          input.addEventListener("input", checkChanges);
      });
    
      // Al cargar la página, el botón está deshabilitado
      checkChanges();
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
    
    
    document.addEventListener('DOMContentLoaded', () => {
        const fileInput = document.getElementById('file_input');
        const previewContainer = document.getElementById('previewContainer');
        const form = document.getElementById('uploadForm');
  
        fileInput.addEventListener('change', function(event) {
          const files = event.target.files;
          console.log('Selected files:', files.length, Array.from(files).map(f => f.name));
  
          // Validación para no cargar más de 3 imágenes
          if (previewContainer.children.length + files.length > 3) {
            console.log('Limit exceeded, stopping at 3');
            checkFileInputVisibility();
            return;
          }
  
          // Mostrar imágenes en el contenedor de vista previa
          for (const file of files) {
            if (previewContainer.children.length >= 3) break;
  
            const reader = new FileReader();
            reader.onload = function(e) {
              const imgContainer = document.createElement('div');
              imgContainer.classList.add('relative', 'group');
  
              const img = document.createElement('img');
              img.src = e.target.result;
              img.classList.add('w-20', 'h-20', 'border', 'rounded', 'object-cover', 'transition-opacity', 'duration-300', 'hover:opacity-50');
  
              const deleteBtn = document.createElement('button');
              deleteBtn.classList.add('absolute', 'top-1', 'right-1', 'bg-red-600', 'text-white', 'rounded-full', 'p-1', 'opacity-0', 'group-hover:opacity-100', 'transition-opacity', 'duration-300');
              deleteBtn.innerHTML = `
                <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke-width="2.0" stroke="#fff">
                  <path stroke-linecap="round" stroke-linejoin="round" d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0" />
                </svg>
              `;
  
              deleteBtn.addEventListener('click', function() {
                imgContainer.remove();
                updateFileInput();
                checkFileInputVisibility();
              });
  
              imgContainer.appendChild(img);
              imgContainer.appendChild(deleteBtn);
              previewContainer.appendChild(imgContainer);
              updateFileInput(); // Actualizar después de cada imagen añadida
            };
            reader.readAsDataURL(file);
          }
  
          checkFileInputVisibility();
        });
  
        function checkFileInputVisibility() {
          fileInput.disabled = previewContainer.children.length >= 3;
          console.log('Input disabled:', fileInput.disabled);
        }
  
        async function updateFileInput() {
          const dataTransfer = new DataTransfer();
          const imgContainers = Array.from(previewContainer.children);
  
          console.log('Updating files, preview count:', imgContainers.length);
  
          const promises = imgContainers.map(async (imgContainer, index) => {
            const imgSrc = imgContainer.querySelector('img').src;
            const response = await fetch(imgSrc);
            const blob = await response.blob();
            const extension = blob.type.split('/')[1] || 'jpg';
            const fileName = `evidence_${Date.now()}_${index}.${extension}`;
            const file = new File([blob], fileName, { type: blob.type });
            dataTransfer.items.add(file);
            console.log(`Added file ${index + 1}: ${fileName} (${blob.type})`);
          });
  
          await Promise.all(promises);
          fileInput.files = dataTransfer.files;
          console.log('Files assigned to input:', fileInput.files.length, Array.from(fileInput.files).map(f => f.name));
        }
  
        // Interceptar el envío del formulario para asegurar que updateFileInput termine
        form.addEventListener('submit', async (e) => {
          e.preventDefault(); // Prevenir envío inmediato
          await updateFileInput(); // Asegurar que los archivos estén actualizados
          console.log('Submitting with files:', fileInput.files.length, Array.from(fileInput.files).map(f => f.name));
          form.submit(); // Enviar el formulario manualmente
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




