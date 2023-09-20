const btn = document.querySelector("#menuBtn");
const menu = document.querySelector("#sidemenu");

btn.addEventListener("click", e =>{
    menu.classList.toggle("menuExpanded");
    menu.classList.toggle("menuCollapsed");

    document.querySelector("body").classList.toggle("bodyExpanded");
})