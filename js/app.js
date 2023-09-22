// Expandir o achicar el menú lateral

const btn = document.querySelector("#menuBtn");
const menu = document.querySelector("#sidemenu");

btn.addEventListener("click", e =>{
    menu.classList.toggle("menuExpanded");
    menu.classList.toggle("menuCollapsed");

    document.querySelector("body").classList.toggle("bodyExpanded");
})

// Guardar fecha seleccionada en dia de estudio
const estudioForm = document.getElementById("estudioForm");
const fechaInput = document.getElementById("fecha");

estudioForm.addEventListener("submit", function(event) {
    event.preventDefault();
    const fechaSeleccionada = fechaInput.value;
    const fechaHoy = new Date();

    if (fechaSeleccionada < fechaHoy){
        alert("No puedes seleccionar una fecha anterior al día actual.");
        return;
    }

    console.log("Fecha seleccionada:", fechaSeleccionada);

    fechaInput.value = "";

    alert("Fecha guardada.")
})