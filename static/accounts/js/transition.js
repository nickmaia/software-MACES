// transition.js
function transitionToPage(targetUrl) {
    const container = document.querySelector('.container');
    container.style.transform = 'translateX(-100%)'; // ou outro efeito desejado
    setTimeout(() => {
        window.location.href = targetUrl;
    }, 500); // Corresponde ao tempo da transição CSS
}