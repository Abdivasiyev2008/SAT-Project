// Navbar toggle functionality
function toggleMenu() {
    const navLinks = document.querySelector('.nav-links');
    navLinks.classList.toggle('show');
}

// This year - Footer
document.getElementById('year').textContent = new Date().getFullYear();
