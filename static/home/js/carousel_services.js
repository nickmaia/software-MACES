let currentIndex = 0;
const members = document.querySelector('.service-list');
const dots = document.querySelectorAll('.carousel-indicators.service-dots .dot');
const totalSlides = members.children.length; // Cada serviço é um slide

function showSlide(index) {
    if (index >= totalSlides) {
        currentIndex = 0;
    } else if (index < 0) {
        currentIndex = totalSlides - 1;
    } else {
        currentIndex = index;
    }
    
    members.style.transform = `translateX(-${currentIndex * 100}%)`;
    dots.forEach(dot => dot.classList.remove('active'));
    dots[currentIndex].classList.add('active');
}

dots.forEach((dot, index) => {
    dot.addEventListener('click', () => {
        showSlide(index);
    });
});

setInterval(() => {
    showSlide(currentIndex + 1);
}, 5000);
