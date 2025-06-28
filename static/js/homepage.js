document.addEventListener('DOMContentLoaded', function() {
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // Animation for features on scroll
    const animateOnScroll = function() {
        const features = document.querySelectorAll('.feature-card');
        const steps = document.querySelectorAll('.step');
        
        features.forEach((feature, index) => {
            const featurePosition = feature.getBoundingClientRect().top;
            const screenPosition = window.innerHeight / 1.3;
            
            if (featurePosition < screenPosition) {
                feature.style.transitionDelay = `${index * 0.1}s`;
                feature.classList.add('animated');
            }
        });
        
        steps.forEach((step, index) => {
            const stepPosition = step.getBoundingClientRect().top;
            const screenPosition = window.innerHeight / 1.3;
            
            if (stepPosition < screenPosition) {
                step.style.transitionDelay = `${index * 0.2}s`;
                step.classList.add('animated');
            }
        });
    };
    
    // Add animation classes initially
    window.addEventListener('load', animateOnScroll);
    // And on scroll
    window.addEventListener('scroll', animateOnScroll);
    
    // Add animation classes to testimonials when in view
    const testimonialObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animated');
            }
        });
    }, { threshold: 0.1 });
    
    document.querySelectorAll('.testimonial-card').forEach(card => {
        testimonialObserver.observe(card);
    });
});