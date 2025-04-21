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
  