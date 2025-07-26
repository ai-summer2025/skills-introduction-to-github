// DOM Elements
const hamburger = document.querySelector('.hamburger');
const navMenu = document.querySelector('.nav-menu');
const bookingForm = document.getElementById('bookingForm');
const modal = document.getElementById('successModal');
const closeModal = document.querySelector('.close');

// Mobile Navigation
hamburger.addEventListener('click', () => {
    hamburger.classList.toggle('active');
    navMenu.classList.toggle('active');
});

// Close mobile menu when clicking on a link
document.querySelectorAll('.nav-link').forEach(n => n.addEventListener('click', () => {
    hamburger.classList.remove('active');
    navMenu.classList.remove('active');
}));

// Smooth Scrolling
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Header Scroll Effect
window.addEventListener('scroll', () => {
    const header = document.querySelector('.header');
    if (window.scrollY > 100) {
        header.style.background = 'rgba(255, 107, 53, 0.95)';
        header.style.backdropFilter = 'blur(10px)';
    } else {
        header.style.background = 'linear-gradient(135deg, #ff6b35, #f7931e)';
        header.style.backdropFilter = 'none';
    }
});

// Set minimum date to today
document.addEventListener('DOMContentLoaded', function() {
    const dateInput = document.getElementById('date');
    const today = new Date().toISOString().split('T')[0];
    dateInput.setAttribute('min', today);
    
    // Set default date to today
    dateInput.value = today;
});

// Select Restaurant Function
function selectRestaurant(name, location) {
    const restaurantSelect = document.getElementById('restaurant');
    const optionValue = `${name} - ${location}`;
    
    // Scroll to booking section
    document.getElementById('booking').scrollIntoView({
        behavior: 'smooth',
        block: 'start'
    });
    
    // Set the restaurant in the dropdown
    setTimeout(() => {
        restaurantSelect.value = optionValue;
        restaurantSelect.style.border = '2px solid #ff6b35';
        setTimeout(() => {
            restaurantSelect.style.border = '2px solid #e0e0e0';
        }, 1000);
    }, 500);
}

// Form Validation
function validateForm(formData) {
    const errors = [];
    
    // Name validation
    if (!formData.name.trim()) {
        errors.push('Please enter your full name');
    } else if (formData.name.trim().length < 2) {
        errors.push('Name must be at least 2 characters long');
    }
    
    // Phone validation
    const phoneRegex = /^[\+]?[0-9\s\-\(\)]{10,}$/;
    if (!formData.phone.trim()) {
        errors.push('Please enter your phone number');
    } else if (!phoneRegex.test(formData.phone.replace(/\s/g, ''))) {
        errors.push('Please enter a valid phone number');
    }
    
    // Email validation
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!formData.email.trim()) {
        errors.push('Please enter your email address');
    } else if (!emailRegex.test(formData.email)) {
        errors.push('Please enter a valid email address');
    }
    
    // Restaurant validation
    if (!formData.restaurant) {
        errors.push('Please select a restaurant');
    }
    
    // Date validation
    if (!formData.date) {
        errors.push('Please select a date');
    } else {
        const selectedDate = new Date(formData.date);
        const today = new Date();
        today.setHours(0, 0, 0, 0);
        
        if (selectedDate < today) {
            errors.push('Please select a future date');
        }
    }
    
    // Time validation
    if (!formData.time) {
        errors.push('Please select a time');
    }
    
    // Guests validation
    if (!formData.guests) {
        errors.push('Please select number of guests');
    }
    
    return errors;
}

// Show Error Messages
function showErrors(errors) {
    // Remove existing error messages
    document.querySelectorAll('.error-message').forEach(el => el.remove());
    
    errors.forEach(error => {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.style.cssText = `
            background: #ffebee;
            color: #c62828;
            padding: 10px;
            border-radius: 5px;
            margin: 10px 0;
            border-left: 4px solid #c62828;
            font-size: 0.9rem;
        `;
        errorDiv.textContent = error;
        
        bookingForm.insertBefore(errorDiv, bookingForm.firstChild);
    });
    
    // Scroll to first error
    const firstError = document.querySelector('.error-message');
    if (firstError) {
        firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
}

// Show Success Message
function showSuccess(bookingData) {
    const bookingDetails = document.getElementById('bookingDetails');
    
    bookingDetails.innerHTML = `
        <div style="background: #f8f9fa; padding: 1rem; border-radius: 8px; margin-top: 1rem; text-align: left;">
            <h4 style="color: #333; margin-bottom: 0.5rem;">Booking Details:</h4>
            <p><strong>Restaurant:</strong> ${bookingData.restaurant}</p>
            <p><strong>Name:</strong> ${bookingData.name}</p>
            <p><strong>Date:</strong> ${formatDate(bookingData.date)}</p>
            <p><strong>Time:</strong> ${formatTime(bookingData.time)}</p>
            <p><strong>Guests:</strong> ${bookingData.guests}</p>
            <p><strong>Phone:</strong> ${bookingData.phone}</p>
            <p><strong>Email:</strong> ${bookingData.email}</p>
            ${bookingData.occasion ? `<p><strong>Occasion:</strong> ${bookingData.occasion}</p>` : ''}
            ${bookingData.requirements ? `<p><strong>Special Requirements:</strong> ${bookingData.requirements}</p>` : ''}
            <p style="margin-top: 1rem; font-size: 0.9rem; color: #666;">
                <strong>Booking ID:</strong> #CHN${Date.now().toString().slice(-6)}
            </p>
        </div>
    `;
    
    modal.style.display = 'block';
    document.body.style.overflow = 'hidden';
}

// Format Date
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-GB', {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

// Format Time
function formatTime(timeString) {
    const [hours, minutes] = timeString.split(':');
    const hour = parseInt(hours);
    const ampm = hour >= 12 ? 'PM' : 'AM';
    const displayHour = hour % 12 || 12;
    return `${displayHour}:${minutes} ${ampm}`;
}

// Form Submission
bookingForm.addEventListener('submit', function(e) {
    e.preventDefault();
    
    // Get form data
    const formData = {
        restaurant: document.getElementById('restaurant').value,
        name: document.getElementById('name').value,
        phone: document.getElementById('phone').value,
        email: document.getElementById('email').value,
        date: document.getElementById('date').value,
        time: document.getElementById('time').value,
        guests: document.getElementById('guests').value,
        occasion: document.getElementById('occasion').value,
        requirements: document.getElementById('requirements').value
    };
    
    // Validate form
    const errors = validateForm(formData);
    
    if (errors.length > 0) {
        showErrors(errors);
        return;
    }
    
    // Remove any existing error messages
    document.querySelectorAll('.error-message').forEach(el => el.remove());
    
    // Show loading state
    const submitBtn = document.querySelector('.submit-btn');
    const originalText = submitBtn.innerHTML;
    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
    submitBtn.disabled = true;
    
    // Simulate API call
    setTimeout(() => {
        // Reset button
        submitBtn.innerHTML = originalText;
        submitBtn.disabled = false;
        
        // Show success
        showSuccess(formData);
        
        // Reset form
        bookingForm.reset();
        
        // Reset date to today
        const today = new Date().toISOString().split('T')[0];
        document.getElementById('date').value = today;
        
    }, 2000);
});

// Modal Close Functions
function closeModal() {
    modal.style.display = 'none';
    document.body.style.overflow = 'auto';
}

closeModal.onclick = closeModal;

window.onclick = function(event) {
    if (event.target == modal) {
        closeModal();
    }
}

// Input Enhancements
document.querySelectorAll('input, select, textarea').forEach(element => {
    element.addEventListener('focus', function() {
        this.parentElement.classList.add('focused');
    });
    
    element.addEventListener('blur', function() {
        this.parentElement.classList.remove('focused');
        if (this.value) {
            this.parentElement.classList.add('filled');
        } else {
            this.parentElement.classList.remove('filled');
        }
    });
});

// Phone Number Formatting
document.getElementById('phone').addEventListener('input', function(e) {
    let value = e.target.value.replace(/\D/g, '');
    
    if (value.startsWith('91') && value.length > 2) {
        value = '+91 ' + value.slice(2);
    } else if (value.length > 0 && !value.startsWith('91')) {
        value = '+91 ' + value;
    }
    
    // Format as +91 XXXXX XXXXX
    if (value.length > 7) {
        value = value.slice(0, 4) + value.slice(4, 9) + ' ' + value.slice(9, 14);
    }
    
    e.target.value = value;
});

// Restaurant Card Animations
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Observe restaurant cards
document.addEventListener('DOMContentLoaded', () => {
    const cards = document.querySelectorAll('.restaurant-card');
    cards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';
        card.style.transition = `all 0.6s ease ${index * 0.1}s`;
        observer.observe(card);
    });
});

// Auto-update available times based on current time and date
function updateAvailableTimes() {
    const dateInput = document.getElementById('date');
    const timeSelect = document.getElementById('time');
    const selectedDate = new Date(dateInput.value);
    const now = new Date();
    const isToday = selectedDate.toDateString() === now.toDateString();
    
    if (isToday) {
        const currentHour = now.getHours();
        const currentMinute = now.getMinutes();
        
        Array.from(timeSelect.options).forEach(option => {
            if (option.value) {
                const [optionHour, optionMinute] = option.value.split(':').map(Number);
                const optionTime = optionHour * 60 + optionMinute;
                const currentTime = currentHour * 60 + currentMinute + 30; // 30 minutes buffer
                
                if (optionTime <= currentTime) {
                    option.disabled = true;
                    option.style.color = '#ccc';
                } else {
                    option.disabled = false;
                    option.style.color = '';
                }
            }
        });
    } else {
        Array.from(timeSelect.options).forEach(option => {
            option.disabled = false;
            option.style.color = '';
        });
    }
}

// Update times when date changes
document.getElementById('date').addEventListener('change', updateAvailableTimes);

// Initialize on page load
document.addEventListener('DOMContentLoaded', updateAvailableTimes);

// Add loading animation to the page
window.addEventListener('load', () => {
    document.body.classList.add('loaded');
});

// Keyboard navigation for accessibility
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && modal.style.display === 'block') {
        closeModal();
    }
});

// Form field validation on blur
document.querySelectorAll('input[required], select[required]').forEach(field => {
    field.addEventListener('blur', function() {
        if (!this.value.trim()) {
            this.style.borderColor = '#e74c3c';
        } else {
            this.style.borderColor = '#27ae60';
        }
    });
    
    field.addEventListener('input', function() {
        if (this.value.trim()) {
            this.style.borderColor = '#27ae60';
        } else {
            this.style.borderColor = '#e0e0e0';
        }
    });
});

console.log('Chennai Dining website loaded successfully! 🍽️');