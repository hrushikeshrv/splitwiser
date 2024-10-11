// Had to name this file prompt-utils because naming it popup-utils would cause ad blockers to block it.
const popupContainers = document.querySelectorAll('.floating-popup-container');
const closePopupButtons = document.querySelectorAll('.close-popup-button');
const popupTriggerButtons = document.querySelectorAll('.popup-trigger-button');

popupTriggerButtons.forEach(btn => {
    btn.addEventListener('click', () => {
        const target = document.getElementById(btn.dataset.popupContainerId);
        if (target) {
            target.classList.remove('hidden');
            document.body.style.overflow = 'hidden';
        }
    })
})

popupContainers.forEach(container => {
    container.addEventListener('click', event => {
        if (event.target !== container) return;
        container.classList.add('hidden');
        document.body.style.overflow = 'visible';
    })
})

closePopupButtons.forEach(btn => {
    btn.addEventListener('click', () => {
        btn.closest('.floating-popup-container').classList.add('hidden');
        document.body.style.overflow = 'visible';
    })
})