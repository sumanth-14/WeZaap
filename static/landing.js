// Landing page JavaScript for WeZaap
// Handles FAQ accordion and mobile navigation

document.addEventListener('DOMContentLoaded', function() {
    // Mobile menu functionality
    const mobileMenuButton = document.querySelector('.mobile-menu-button');
    const mobileMenu = document.querySelector('.mobile-menu');
    
    if (mobileMenuButton && mobileMenu) {
        mobileMenuButton.addEventListener('click', function() {
            const isExpanded = this.getAttribute('aria-expanded') === 'true';
            
            // Toggle menu visibility
            mobileMenu.classList.toggle('hidden');
            
            // Update aria-expanded
            this.setAttribute('aria-expanded', !isExpanded);
            
            // Update button icon
            const icon = this.querySelector('svg');
            if (icon) {
                if (isExpanded) {
                    // Show hamburger icon
                    icon.innerHTML = '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />';
                } else {
                    // Show close icon
                    icon.innerHTML = '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />';
                }
            }
        });
        
        // Close mobile menu when clicking outside
        document.addEventListener('click', function(e) {
            if (!mobileMenuButton.contains(e.target) && !mobileMenu.contains(e.target)) {
                mobileMenu.classList.add('hidden');
                mobileMenuButton.setAttribute('aria-expanded', 'false');
                const icon = mobileMenuButton.querySelector('svg');
                if (icon) {
                    icon.innerHTML = '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />';
                }
            }
        });
    }
    
    // FAQ accordion functionality
    const faqButtons = document.querySelectorAll('.faq-button');
    
    faqButtons.forEach(button => {
        button.addEventListener('click', function() {
            const content = this.nextElementSibling;
            const icon = this.querySelector('.faq-icon');
            const isExpanded = this.getAttribute('aria-expanded') === 'true';
            
            // Close all other FAQ items
            faqButtons.forEach(otherButton => {
                if (otherButton !== this) {
                    otherButton.setAttribute('aria-expanded', 'false');
                    otherButton.nextElementSibling.classList.add('hidden');
                    const otherIcon = otherButton.querySelector('.faq-icon');
                    if (otherIcon) {
                        otherIcon.style.transform = 'rotate(0deg)';
                    }
                }
            });
            
            // Toggle current FAQ item
            if (isExpanded) {
                content.classList.add('hidden');
                this.setAttribute('aria-expanded', 'false');
                if (icon) {
                    icon.style.transform = 'rotate(0deg)';
                }
            } else {
                content.classList.remove('hidden');
                this.setAttribute('aria-expanded', 'true');
                if (icon) {
                    icon.style.transform = 'rotate(180deg)';
                }
            }
        });
        
        // Handle keyboard navigation for FAQ
        button.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                this.click();
            }
        });
    });
    
    // Smooth scrolling for anchor links
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    anchorLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                e.preventDefault();
                
                // Check if user prefers reduced motion
                const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
                
                if (prefersReducedMotion) {
                    targetElement.scrollIntoView();
                } else {
                    targetElement.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
                
                // Close mobile menu if open
                if (mobileMenu && !mobileMenu.classList.contains('hidden')) {
                    mobileMenu.classList.add('hidden');
                    mobileMenuButton.setAttribute('aria-expanded', 'false');
                    const icon = mobileMenuButton.querySelector('svg');
                    if (icon) {
                        icon.innerHTML = '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />';
                    }
                }
            }
        });
    });
    
    // Add focus styles for better accessibility
    const focusableElements = document.querySelectorAll('a, button, input, select, textarea');
    focusableElements.forEach(element => {
        element.addEventListener('focus', function() {
            this.style.outline = '2px solid #4f46e5';
            this.style.outlineOffset = '2px';
        });
        
        element.addEventListener('blur', function() {
            this.style.outline = '';
            this.style.outlineOffset = '';
        });
    });
    
    // Handle reduced motion preference
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
    if (prefersReducedMotion.matches) {
        // Disable any animations for users who prefer reduced motion
        document.documentElement.style.setProperty('--animation-duration', '0s');
        document.documentElement.style.setProperty('--transition-duration', '0s');
    }
    
    // Add loading state management
    const ctaButtons = document.querySelectorAll('a[href="/practice"], a[href="/demo"]');
    ctaButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            // Add loading state
            const originalText = this.textContent;
            this.textContent = 'Loading...';
            this.style.pointerEvents = 'none';
            
            // Reset after a short delay (in case of navigation issues)
            setTimeout(() => {
                this.textContent = originalText;
                this.style.pointerEvents = '';
            }, 3000);
        });
    });
});


