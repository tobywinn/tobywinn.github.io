const primaryNav = document.querySelector(".primary-navigation");
const navToggle = document.querySelector(".mobile-nav-toggle");
const hamburger = document.querySelector(".hamburger");
const cross = document.querySelector(".cross")

navToggle.addEventListener("click", () => {
    const visibility = primaryNav.getAttribute("data-visible");
    
    if (visibility === "false") {
        primaryNav.setAttribute("data-visible", "true");
        hamburger.setAttribute("data-visible", "true");
        cross.setAttribute("data-visible", "true");
    } else {
        primaryNav.setAttribute("data-visible", "false");   
        hamburger.setAttribute("data-visible", "false");  
        cross.setAttribute("data-visible", "false");  
    }
});