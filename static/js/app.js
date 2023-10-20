// Expandir o achicar el menú lateral

const btn = document.querySelector("#menuBtn");
const menu = document.querySelector("#sidemenu");


btn.addEventListener("click", e =>{
    menu.classList.toggle("menuExpanded");
    menu.classList.toggle("menuCollapsed");

    document.querySelector("body").classList.toggle("bodyExpanded");
})

//Expandir el menú para solicitar dias
document.addEventListener('DOMContentLoaded', function() {
    let solicitarDiasLink = document.querySelector('.solicitarDias');
    let solicitarDiasItems = document.querySelector('.solicitarDiasItems');

    solicitarDiasLink.addEventListener('click', function() {
        if (solicitarDiasItems.style.display === 'none') {
            solicitarDiasItems.style.display = 'block';
        } else {
            solicitarDiasItems.style.display = 'none';
        }
    });
});