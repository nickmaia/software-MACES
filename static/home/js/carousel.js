let currentIndex = 0;
const members = document.querySelector('.team-members');
const dotsContainer = document.querySelector('.carousel-indicators.team-dots');
const membersCount = document.querySelectorAll('.team-members .member').length;

function updateDots() {
    dotsContainer.innerHTML = ''; // Limpa os dots existentes
    const screenWidth = window.innerWidth;

    let dotsCount = screenWidth <= 768 ? membersCount : Math.ceil(membersCount / 3); 

    for (let i = 0; i < dotsCount; i++) {
        const dot = document.createElement('span');
        dot.classList.add('dot');
        if (i === 0) dot.classList.add('active');
        dotsContainer.appendChild(dot);
    }

    const dots = document.querySelectorAll('.carousel-indicators .dot');
    dots.forEach((dot, index) => {
        dot.addEventListener('click', () => {
            showSlide(index);
        });
    });
}

function showSlide(index) {
    if (index >= dotsContainer.children.length) {
        currentIndex = 0;
    } else if (index < 0) {
        currentIndex = dotsContainer.children.length - 1;
    } else {
        currentIndex = index;
    }

    members.style.transform = `translateX(-${currentIndex * 100}%)`;
    document.querySelectorAll('.carousel-indicators .dot').forEach(dot => dot.classList.remove('active'));
    dotsContainer.children[currentIndex].classList.add('active');
}

window.addEventListener('resize', () => {
    updateDots();
    showSlide(0); // Reset to first slide on resize
});

updateDots(); // Initial setup
showSlide(0);

setInterval(() => {
    showSlide(currentIndex + 1);
}, 5000); // Troca automática a cada 5 segundos
