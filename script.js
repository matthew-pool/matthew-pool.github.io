/*
    Project: Portfolio
    File: script.js
    @author: Matthew Pool
    
    MODAL POPUP VERSION: Click card → popup window with details
*/

/* Email */
function copyEmail(button) {
    navigator.clipboard.writeText('mathyou.me@gmail.com').then(() => {
        showToast(button);
    });
}

/* Directions popup */
function showDirections() {
    document.getElementById('directionsPopup').classList.add('show');
}

function hideDirections() {
    document.getElementById('directionsPopup').classList.remove('show');
}

function showToast(button) {
    const container = button.parentElement.querySelector('.toast-container');
    if (!container) return;

    const existingToast = container.querySelector('.toast');
    if (existingToast) {
        existingToast.remove();
    }

    const toast = document.createElement('span');
    toast.className = 'toast';
    toast.textContent = 'copied';

    container.appendChild(toast);

    setTimeout(() => toast.classList.add('show'), 10);

    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 200);
    }, 500);
}

// Bird animation variables
let birdHasFlown = false;
let isPositioned = false;
let isReady = false;
const bird = document.getElementById('bird');

// Reset bird state on page load
window.addEventListener('load', function() {
    birdHasFlown = false;
    isPositioned = false;
    isReady = false;

    bird.classList.remove('flying', 'idle', 'landed');
    positionBird();

    setTimeout(() => {
        isReady = true;
    }, 1000);
});


// Dark mode toggle
const themeToggle = document.getElementById('themeToggle');
const body = document.body;

const savedTheme = localStorage.getItem('theme');
if (savedTheme === 'light') {
    document.body.classList.remove('dark-mode');
}

themeToggle.addEventListener('click', () => {
    document.body.classList.toggle('dark-mode');
    const currentTheme = document.body.classList.contains('dark-mode') ? 'dark' : 'light';
    localStorage.setItem('theme', currentTheme);
});

function openTab(evt, tabName) {
    const tabContents = document.getElementsByClassName('tab-content');
    for (let i = 0; i < tabContents.length; i++) {
        tabContents[i].classList.remove('active');
    }

    const tabButtons = document.getElementsByClassName('tab-button');
    for (let i = 0; i < tabButtons.length; i++) {
        tabButtons[i].classList.remove('active');
    }

    document.getElementById(tabName).classList.add('active');
    evt.currentTarget.classList.add('active');

    window.scrollTo(0, 0);

    if (tabName !== 'home') {
        flyBirdBack();
    }
}

function flyBirdBack() {
    if (!birdHasFlown) return;

    bird.classList.remove('idle', 'landed');
    bird.classList.add('flying');

    const currentLeft = parseFloat(bird.style.left);
    const currentTop = parseFloat(bird.style.top);

    const refactorTab = document.querySelector('.tab-button:nth-child(3)');
    const heroSection = document.querySelector('.hero-section');
    if (!refactorTab || !heroSection) return;

    const tabRect = refactorTab.getBoundingClientRect();
    const heroRect = heroSection.getBoundingClientRect();
    const targetLeft = tabRect.left + window.scrollX + (tabRect.width / 2) - 30;
    const targetTop = heroRect.bottom + window.scrollY - 48; 

    const cpX = (currentLeft + targetLeft) / 2;
    const cpY = Math.min(currentTop, targetTop) - 300; 

    const duration = 2500; 
    const startTime = performance.now();

    function animateReturn(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        
        const t = 1 - Math.pow(1 - progress, 3); 
        const invT = 1 - t;

        const x = (invT * invT * currentLeft) + (2 * invT * t * cpX) + (t * t * targetLeft);
        const y = (invT * invT * currentTop) + (2 * invT * t * cpY) + (t * t * targetTop);

        const dx = 2 * invT * (cpX - currentLeft) + 2 * t * (targetLeft - cpX);
        const dy = 2 * invT * (cpY - currentTop) + 2 * t * (targetTop - cpY);
        
        let angle = Math.atan2(dy, dx) * (180 / Math.PI);
        
        const scaleX = (Math.abs(angle) > 90) ? -1 : 1;
        
        let visualRotation = angle;
        if (scaleX === -1) {
            visualRotation = angle - 180;
            if (visualRotation < -180) visualRotation += 360;
        }

        if (dy > 0) {
             visualRotation = visualRotation * 0.3; 
        }

        if (progress > 0.6) {
            const landingProgress = (progress - 0.6) / 0.4;
            visualRotation = visualRotation * (1 - landingProgress);
        }

        visualRotation = Math.max(-25, Math.min(25, visualRotation));

        bird.style.left = x + 'px';
        bird.style.top = y + 'px';
        bird.style.transform = `scaleX(${scaleX}) rotate(${visualRotation}deg)`;

        if (progress < 1) {
            requestAnimationFrame(animateReturn);
        } else {
            bird.classList.remove('flying');
            bird.classList.add('landed');
            
            bird.style.transform = 'scaleX(1) rotate(0deg)'; 
            bird.style.position = 'absolute';
            bird.style.left = targetLeft + 'px';
            bird.style.top = targetTop + 'px';
            
            birdHasFlown = false;
            isReady = false;

            setTimeout(() => {
                bird.classList.remove('landed');
                bird.classList.add('idle');
            }, 500);

            setTimeout(() => {
                isReady = true;
            }, 1000);
        }
    }

    requestAnimationFrame(animateReturn);
}

function positionBird() {
    if (birdHasFlown) return;

    const refactorTab = document.querySelector('.tab-button:nth-child(3)');
    const heroSection = document.querySelector('.hero-section');

    if (refactorTab && heroSection) {
        const tabRect = refactorTab.getBoundingClientRect();
        const heroRect = heroSection.getBoundingClientRect();

        const leftPos = tabRect.left + window.scrollX + (tabRect.width / 2) - 30;
        const topPos = heroRect.bottom + window.scrollY - 48;

        bird.dataset.initialLeft = leftPos;
        bird.dataset.initialTop = topPos;

        bird.style.left = leftPos + 'px';
        bird.style.top = topPos + 'px';
        bird.style.position = 'absolute';
        bird.style.opacity = '1';

        bird.classList.add('landed');

        setTimeout(() => {
            bird.classList.remove('landed');
            bird.classList.add('idle');
        }, 500);

        isPositioned = true;
    }
}

setTimeout(positionBird, 100);
setTimeout(positionBird, 500);
window.addEventListener('load', positionBird);

setTimeout(() => {
    isReady = true;
}, 1000);

window.addEventListener('scroll', function() {
    const homeTab = document.getElementById('home');
    const isHomeActive = homeTab && homeTab.classList.contains('active');
    
    // 1. Find the destination element
    const flickLogo = document.querySelector('.flick-logo');

    // 2. Check if everything is valid before calculating positions
    if (!birdHasFlown && isPositioned && isReady && isHomeActive && flickLogo) {
        
        // 3. Get the logo's position relative to the viewport
        const rect = flickLogo.getBoundingClientRect();
        
        // 4. TRIGGER: When the top of the logo enters the bottom of the screen
        // (rect.top represents the distance from the top of the viewport to the element)
        if (rect.top < window.innerHeight) {

            birdHasFlown = true;

            bird.classList.remove('landed', 'idle');
            bird.classList.add('flying');

            const startLeft = parseFloat(bird.dataset.initialLeft);
            const startTop = parseFloat(bird.dataset.initialTop);

            // Recalculate end positions based on the now-visible logo
            // (This logic remains the same as your previous code)
            const flickRect = flickLogo.getBoundingClientRect();
            const endLeft = flickRect.left + window.scrollX + (flickRect.width / 2) - 30;
            const endTop = flickRect.top + window.scrollY - 36;

            const duration = 2800;
            const startTime = performance.now();

            function animateBird(currentTime) {
                const elapsed = currentTime - startTime;
                const progress = Math.min(elapsed / duration, 1);

                let x, y, rotation, scaleX;

                if (progress < 0.15) {
                    const flapProgress = progress / 0.15;
                    x = startLeft - (20 * flapProgress);
                    y = startTop - (80 * flapProgress);

                    scaleX = flapProgress < 0.2 ? 1 : -1;
                    rotation = -20 * flapProgress;

                } else {
                    const flightProgress = (progress - 0.15) / 0.85;
                    
                    const p0x = startLeft - 20;
                    const p0y = startTop - 80;

                    const p3x = endLeft;
                    const p3y = endTop;

                    const p1x = startLeft - 50; 
                    const p1y = startTop + 500; 

                    const p2x = endLeft - 100;
                    const p2y = endTop - 80;

                    const t = flightProgress;
                    const invT = 1 - t;

                    x = (Math.pow(invT, 3) * p0x) + 
                        (3 * Math.pow(invT, 2) * t * p1x) + 
                        (3 * invT * Math.pow(t, 2) * p2x) + 
                        (Math.pow(t, 3) * p3x);

                    y = (Math.pow(invT, 3) * p0y) + 
                        (3 * Math.pow(invT, 2) * t * p1y) + 
                        (3 * invT * Math.pow(t, 2) * p2y) + 
                        (Math.pow(t, 3) * p3y);

                    scaleX = -1;
                    
                    if (flightProgress < 0.3) {
                        rotation = -20 + (110 * (flightProgress / 0.3));
                    } else if (flightProgress < 0.7) {
                        const curveP = (flightProgress - 0.3) / 0.4; 
                        rotation = 90 - (120 * curveP); 
                    } else {
                        const landP = (flightProgress - 0.7) / 0.3;
                        rotation = -30 + (30 * landP);
                    }
                }

                bird.style.left = x + 'px';
                bird.style.top = y + 'px';
                bird.style.transform = `scaleX(${scaleX}) rotate(${rotation}deg)`;

                if (progress < 1) {
                    requestAnimationFrame(animateBird);
                } else {
                    bird.classList.remove('flying');
                    bird.classList.add('landed');
                    bird.style.position = 'absolute';
                    bird.style.left = endLeft + 'px';
                    bird.style.top = endTop + 'px';
                    bird.style.transform = 'scaleX(-1) rotate(0deg)';

                    setTimeout(() => {
                        bird.classList.remove('landed');
                        bird.classList.add('idle');
                    }, 500);
                }
            }

            requestAnimationFrame(animateBird);
        }
    }
});

window.addEventListener('resize', function() {
    if (!birdHasFlown) {
        positionBird();
    }
});

// Project filter functionality
function filterProjects(category) {
    const filterButtons = document.querySelectorAll('.filter-btn');
    filterButtons.forEach(btn => btn.classList.remove('active'));
    event.target.classList.add('active');

    const projectCards = document.querySelectorAll('.project-card');
    projectCards.forEach(card => {
        if (category === 'all' || card.dataset.category === category) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
}

// ========================================
// PROJECT DETAILS MODAL POPUP
// ========================================

function openProjectModal(projectId) {
    const modal = document.getElementById('project-modal');
    const modalContent = document.getElementById('project-modal-content');
    const detailsElement = document.getElementById(`details-${projectId}`);
    
    if (!modal || !modalContent || !detailsElement) return;
    
    // Clone the details content into the modal
    modalContent.innerHTML = detailsElement.innerHTML;
    
    // Show the modal
    modal.classList.add('show');
    
    // Prevent body scroll
    document.body.style.overflow = 'hidden';
}

function closeProjectModal() {
    const modal = document.getElementById('project-modal');
    
    if (!modal) return;
    
    // Hide the modal
    modal.classList.remove('show');
    
    // Restore body scroll
    document.body.style.overflow = '';
}

// Close modal when clicking anywhere EXCEPT links or buttons
const modal = document.getElementById('project-modal');
if (modal) {
    modal.addEventListener('click', function(e) {
        // 1. Check if the click was on (or inside) a link or button
        const isInteractive = e.target.closest('a') || e.target.closest('button');
        
        // 2. If it is interactive, do nothing (let the link/button work)
        if (isInteractive) {
            return;
        }

        // 3. Otherwise (text, images, background), close the modal
        closeProjectModal();
    });
}

// Close modal when clicking the dark overlay (background)
document.getElementById('project-modal').addEventListener('click', function(e) {
    // 'this' refers to the #project-modal container
    if (e.target === this) {
        closeProjectModal();
    }
});

// Close modal with Escape key
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        closeProjectModal();
    }
});

// Lightbox functionality
let currentImageIndex = 0;
let lightboxImages = [];

function initLightbox() {
    const clickableImages = document.querySelectorAll('.screenshot-grid img, .project-image-card img, .image-card img, .buddy-screenshot-grid img, .mario-image, .paradox-image');
    
    clickableImages.forEach((img, index) => {
        img.style.cursor = 'pointer';
        img.addEventListener('click', function(e) {
            e.stopPropagation();
            openLightbox(this, Array.from(clickableImages));
        });
    });
}

function openLightbox(clickedImg, allImages) {
    lightboxImages = allImages;
    currentImageIndex = lightboxImages.indexOf(clickedImg);
    
    const lightbox = document.getElementById('lightbox');
    const lightboxImg = document.getElementById('lightbox-img');
    const lightboxCaption = document.getElementById('lightbox-caption');
    
    lightboxImg.src = clickedImg.src;
    lightboxCaption.textContent = clickedImg.alt || '';
    lightbox.classList.add('active');
    
    document.body.style.overflow = 'hidden';
}

function closeLightbox() {
    const lightbox = document.getElementById('lightbox');
    lightbox.classList.remove('active');
    document.body.style.overflow = '';
}

function changeLightboxImage(direction) {
    currentImageIndex += direction;
    
    if (currentImageIndex >= lightboxImages.length) {
        currentImageIndex = 0;
    } else if (currentImageIndex < 0) {
        currentImageIndex = lightboxImages.length - 1;
    }
    
    const lightboxImg = document.getElementById('lightbox-img');
    const lightboxCaption = document.getElementById('lightbox-caption');
    
    lightboxImg.src = lightboxImages[currentImageIndex].src;
    lightboxCaption.textContent = lightboxImages[currentImageIndex].alt || '';
}

document.getElementById('lightbox').addEventListener('click', function(e) {
    if (e.target === this) {
        closeLightbox();
    }
});

document.addEventListener('keydown', function(e) {
    const lightbox = document.getElementById('lightbox');
    if (lightbox.classList.contains('active')) {
        if (e.key === 'Escape') {
            closeLightbox();
        } else if (e.key === 'ArrowLeft') {
            changeLightboxImage(-1);
        } else if (e.key === 'ArrowRight') {
            changeLightboxImage(1);
        }
    }
});

window.addEventListener('load', initLightbox);