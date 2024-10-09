const openMobileNavButton = document.querySelector('#open-mobile-nav-button');
const closeMobileNavButton = document.querySelector('#close-mobile-nav-button');
const mobileNav = document.querySelector('#mobile-nav-menu');

openMobileNavButton.addEventListener('click', () => {
    mobileNav.style.left = '0';
})

closeMobileNavButton.addEventListener('click', () => {
    mobileNav.style.left = '-100%';
})
