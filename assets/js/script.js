document.querySelector('.go-to-top').addEventListener('click', function (e) {
    e.preventDefault(); // Prevents default jump
    window.scrollTo({ top: 0, behavior: 'smooth' });
});
