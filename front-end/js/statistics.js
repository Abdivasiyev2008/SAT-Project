// Function to animate number counting with smooth transition
function animateNumbers() {
    const stats = document.querySelectorAll('.stat-number');
    stats.forEach((stat, index) => {
        const endValue = parseInt(stat.getAttribute('data-value'));
        let currentValue = 0;
        const duration = 2000; // Animation duration
        const increment = endValue / 50; // Increment based on steps

        const updateNumber = () => {
            currentValue += increment;
            if (currentValue >= endValue) {
                currentValue = endValue;
                stat.innerText = Math.floor(currentValue);
            } else {
                stat.innerText = Math.floor(currentValue);
                requestAnimationFrame(updateNumber);
            }
        };
        updateNumber();
    });
}

// Trigger animation on scroll
function handleScrollAnimation() {
    const statsSection = document.querySelector('.statistics-card');
    const rect = statsSection.getBoundingClientRect();
    if (rect.top >= 0 && rect.bottom <= window.innerHeight) {
        animateNumbers();
        window.removeEventListener('scroll', handleScrollAnimation); // Avoid repeating
    }
}

window.addEventListener('scroll', handleScrollAnimation);
