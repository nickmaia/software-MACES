/* Muda a cor de fundo ao rolar */
window.onscroll = function() {
    var header = document.querySelector('header');
    if (window.scrollY > 50) {
        header.style.backgroundColor = '#FFFFFF';
    } else {
        header.style.backgroundColor = 'transparent';
    }
};
