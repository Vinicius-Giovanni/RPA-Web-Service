const carousel = document.querySelector('.carousel');
const nextButton = document.querySelector('.carousel-btn.next');
const prevButton = document.querySelector('.carousel-btn.prev');

if (carousel && nextButton && prevButton) {
    const getScrollDistance = () => {
        const card = carousel.querySelector('.card');
        if (!card) {
            return 0;
        }

        const cardWidth = card.getBoundingClientRect().width;
        const gap = parseFloat(window.getComputedStyle(carousel).columnGap || window.getComputedStyle(carousel).gap || '0');
        return cardWidth + gap;
    };

    const updateButtons = () => {
        const maxScrollLeft = carousel.scrollWidth - carousel.clientWidth;
        prevButton.disabled = carousel.scrollLeft <= 0;
        nextButton.disabled = carousel.scrollLeft >= maxScrollLeft - 1;
    };

    nextButton.addEventListener('click', () => {
        carousel.scrollBy({
            left: getScrollDistance(),
            behavior: 'smooth'
        });
    });

    prevButton.addEventListener('click', () => {
        carousel.scrollBy({
            left: -getScrollDistance(),
            behavior: 'smooth'
        });
    });

    carousel.addEventListener('scroll', updateButtons);
    window.addEventListener('resize', updateButtons);

    updateButtons();
}