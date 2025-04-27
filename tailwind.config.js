/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/templates/**/*.{html,js}",    // TODOS los archivos HTML dentro de templates/
    "./templates/**/*.{html,js}",        // TODOS los archivos HTML en templates/
    "./templates/resident/*.{html,js}",        // TODOS los archivos HTML en templates/
    "./templates/admin/*.{html,js}",        // TODOS los archivos HTML en templates/
    "./templates/includes/*.{html,js}",        // TODOS los archivos HTML en templates/
    "./static/js/**/*.js",               // TODOS los archivos JS en static/js
    "./app/templates/login.html",                      // Página principal
    "./node_modules/flowbite/**/*.js"    // Flowbite (si lo usas)
  ],
  theme: {
    extend: {
      screens: {
        'custom-lg': '800px',            // Nuevo breakpoint personalizado
      },
      colors: {             
       'verde': '#157F3D',             // Nuevo color personalizado1
       'gris': '#212529',
      },
    },
  },
};

