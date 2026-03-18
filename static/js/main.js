// JavaScript for navigation interactions
const navToggle = document.querySelector('.nav-toggle');
const navLinks = document.querySelectorAll('nav a');

navToggle.addEventListener('click', () => {
    document.body.classList.toggle('nav-open');
});

navLinks.forEach(link => {
    link.addEventListener('click', () => {
        document.body.classList.remove('nav-open');
    });
});

// Smooth scrolling
const scrollLinks = document.querySelectorAll('a[href^="#"]');

scrollLinks.forEach(link => {
    link.addEventListener('click', (e) => {
        e.preventDefault();
        const target = document.querySelector(link.getAttribute('href'));
        target.scrollIntoView({ behavior: 'smooth' });
    });
});

// Dynamic content loading for API endpoints
async function loadContent(url, container) {
    try {
        const response = await fetch(url);
        const data = await response.json();
        document.querySelector(container).innerHTML = JSON.stringify(data, null, 2);
    } catch (error) {
        console.error('Error loading content:', error);
    }
}

// Example usage
// loadContent('/api/users', '#user-data');

// Form validation
const forms = document.querySelectorAll('form');

forms.forEach(form => {
    form.addEventListener('submit', (e) => {
        const inputs = form.querySelectorAll('input, select, textarea');
        inputs.forEach(input => {
            if (!input.checkValidity()) {
                e.preventDefault();
                input.classList.add('invalid');
            } else {
                input.classList.remove('invalid');
            }
        });
    });
});