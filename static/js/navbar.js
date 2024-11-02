const openMobileNavButton = document.querySelector('#open-mobile-nav-button');
const closeMobileNavButton = document.querySelector('#close-mobile-nav-button');
const mobileNav = document.querySelector('#mobile-nav-menu');

openMobileNavButton.addEventListener('click', () => {
    mobileNav.style.left = '0';
    document.body.style.overflow = 'hidden';
})

closeMobileNavButton.addEventListener('click', () => {
    mobileNav.style.left = '-100%';
    document.body.style.overflow = 'visible';
})
