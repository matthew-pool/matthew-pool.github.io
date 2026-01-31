/*
    Project: Portfolio
    File: script.js
    @author: Matthew Pool
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
    // Find the toast container (parent span)
    const container = button.parentElement.querySelector('.toast-container');
    if (!container) return;

    // Remove existing toast if any
    const existingToast = container.querySelector('.toast');
    if (existingToast) {
        existingToast.remove();
    }

    // Create and show new toast
    const toast = document.createElement('span');
    toast.className = 'toast';
    toast.textContent = 'copied';

    container.appendChild(toast);

    // Trigger animation
    setTimeout(() => toast.classList.add('show'), 10);

    // Remove after 1 second
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

    // Reset bird classes
    bird.classList.remove('flying', 'idle', 'landed');

    // Reposition bird
    positionBird();

    // Mark as ready after delay
    setTimeout(() => {
        isReady = true;
    }, 1000);
});


// Dark mode toggle
const themeToggle = document.getElementById('themeToggle');
const body = document.body;

// Check for saved theme preference
const savedTheme = localStorage.getItem('theme');
if (savedTheme === 'light') {
    document.body.classList.remove('dark-mode');
}

// Toggle Click Handler
themeToggle.addEventListener('click', () => {
    document.body.classList.toggle('dark-mode');

    // Determine what to save based on the state AFTER the toggle
    const currentTheme = document.body.classList.contains('dark-mode') ? 'dark' : 'light';
    localStorage.setItem('theme', currentTheme);
});

function openTab(evt, tabName) {
    // Hide all tab contents
    const tabContents = document.getElementsByClassName('tab-content');
    for (let i = 0; i < tabContents.length; i++) {
        tabContents[i].classList.remove('active');
    }

    // Remove active class from all buttons
    const tabButtons = document.getElementsByClassName('tab-button');
    for (let i = 0; i < tabButtons.length; i++) {
        tabButtons[i].classList.remove('active');
    }

    // Show the current tab and mark button as active
    document.getElementById(tabName).classList.add('active');
    evt.currentTarget.classList.add('active');

    // Scroll to top when switching tabs
    window.scrollTo(0, 0);

    // Reset bird if switching away from home
    if (tabName !== 'home') {
        flyBirdBack();
    }
}

function flyBirdBack() {
    if (!birdHasFlown) return; // Bird hasn't flown yet, nothing to reset

    // Add flying class for wing flapping during return
    bird.classList.remove('idle', 'landed');
    bird.classList.add('flying');

    // Get current position
    const currentLeft = parseFloat(bird.style.left);
    const currentTop = parseFloat(bird.style.top);

    // Get target absolute position
    const refactorTab = document.querySelector('.tab-button:nth-child(3)');
    const contactHeader = document.querySelector('.contact-card');
    if (!refactorTab || !contactHeader) return;

    const tabRect = refactorTab.getBoundingClientRect();
    const headerRect = contactHeader.getBoundingClientRect();
    const targetLeft = tabRect.left + window.scrollX + (tabRect.width / 2) - 30;
    const targetTop = headerRect.bottom + window.scrollY - 58; 

    // Setup Control Point (High Arc)
    const cpX = (currentLeft + targetLeft) / 2;
    const cpY = Math.min(currentTop, targetTop) - 300; 

    const duration = 2500; 
    const startTime = performance.now();

    function animateReturn(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        
        // Ease out cubic
        const t = 1 - Math.pow(1 - progress, 3); 
        const invT = 1 - t;

        // Quadratic Bezier Position
        const x = (invT * invT * currentLeft) + (2 * invT * t * cpX) + (t * t * targetLeft);
        const y = (invT * invT * currentTop) + (2 * invT * t * cpY) + (t * t * targetTop);

        // Calculate Derivative (Tangent) for Rotation
        const dx = 2 * invT * (cpX - currentLeft) + 2 * t * (targetLeft - cpX);
        const dy = 2 * invT * (cpY - currentTop) + 2 * t * (targetTop - cpY);
        
        // Basic Angle
        let angle = Math.atan2(dy, dx) * (180 / Math.PI);
        
        // Determine facing direction
        const scaleX = (Math.abs(angle) > 90) ? -1 : 1;
        
        let visualRotation = angle;
        if (scaleX === -1) {
            visualRotation = angle - 180;
            if (visualRotation < -180) visualRotation += 360;
        }

        // --- STABILIZATION FIX ---
        // 1. If we are moving DOWN (dy > 0), dampen the rotation significantly.
        //    This prevents steep dives.
        if (dy > 0) {
             visualRotation = visualRotation * 0.3; 
        }

        // 2. Early Landing Preparation (The "Vertical" Fix)
        //    Once we are 60% through the flight (past the peak), 
        //    start forcing the bird to become upright (0 degrees).
        if (progress > 0.6) {
            const landingProgress = (progress - 0.6) / 0.4; // Normalize 0.6->1.0 to 0->1
            
            // Linearly interpolate whatever angle we have towards 0
            // By the time progress hits 1.0, visualRotation will strictly be 0.
            visualRotation = visualRotation * (1 - landingProgress);
        }

        // 3. Hard Safety Clamp
        //    Never allow rotation past 25 degrees in either direction during return.
        visualRotation = Math.max(-25, Math.min(25, visualRotation));

        bird.style.left = x + 'px';
        bird.style.top = y + 'px';
        bird.style.transform = `scaleX(${scaleX}) rotate(${visualRotation}deg)`;

        if (progress < 1) {
            requestAnimationFrame(animateReturn);
        } else {
            // Animation Complete
            bird.classList.remove('flying');
            bird.classList.add('landed');
            
            // Hard set to perfect position/rotation
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

// Position bird above Refactor tab at bottom edge of contact header
function positionBird() {
    if (birdHasFlown) return;

    const refactorTab = document.querySelector('.tab-button:nth-child(3)');
    const contactHeader = document.querySelector('.contact-card');

    if (refactorTab && contactHeader) {
        const tabRect = refactorTab.getBoundingClientRect();
        const headerRect = contactHeader.getBoundingClientRect();

        // Position horizontally centered on Refactor tab, vertically at bottom of contact card
        const leftPos = tabRect.left + window.scrollX + (tabRect.width / 2) - 30;
        const topPos = headerRect.bottom + window.scrollY - 58;

        bird.dataset.initialLeft = leftPos;
        bird.dataset.initialTop = topPos;

        bird.style.left = leftPos + 'px';
        bird.style.top = topPos + 'px';
        bird.style.position = 'absolute';
        bird.style.opacity = '1';

        // TRIGGER LANDING PHYSICS
        bird.classList.add('landed');

        // Add idle animation after landing animation completes
        setTimeout(() => {
            bird.classList.remove('landed');
            bird.classList.add('idle');
        }, 500);

        isPositioned = true;
    }
}

// Position after delays
setTimeout(positionBird, 100);
setTimeout(positionBird, 500);
window.addEventListener('load', positionBird);

// Mark as ready after a delay to prevent initial scroll events
setTimeout(() => {
    isReady = true;
}, 1000);

window.addEventListener('scroll', function() {
    // Only animate on home tab
    const homeTab = document.getElementById('home');
    const isHomeActive = homeTab && homeTab.classList.contains('active');

    if (!birdHasFlown && isPositioned && isReady && isHomeActive && window.scrollY > 0) {
        birdHasFlown = true;

        // Add flying class for wing flapping
        bird.classList.remove('landed', 'idle');
        bird.classList.add('flying');

        // Get current absolute position
        const startLeft = parseFloat(bird.dataset.initialLeft);
        const startTop = parseFloat(bird.dataset.initialTop);

        // Find Flick logo position and calculate absolute position
        const flickLogo = document.querySelector('.flick-logo');
        let endLeft = startLeft - 600;
        let endTop = startTop + 600;

        if (flickLogo) {
            const flickRect = flickLogo.getBoundingClientRect();
            // Calculate absolute position (viewport position + scroll offset)
            endLeft = flickRect.left + window.scrollX + (flickRect.width / 2) - 30;
            endTop = flickRect.top + window.scrollY - 36;
        }

        // Animate using JavaScript - bird stays in absolute positioning throughout
        const duration = 2800; // Slower duration for a deeper, more dramatic path
        const startTime = performance.now();

        function animateBird(currentTime) {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);

            let x, y, rotation, scaleX;

            if (progress < 0.15) {
                // ==========================================
                // Phase 1: Takeoff (0% - 15%)
                // ==========================================
                const flapProgress = progress / 0.15;
                // Move Up and slightly left
                x = startLeft - (20 * flapProgress);
                y = startTop - (80 * flapProgress);

                // Flip to face left early
                scaleX = flapProgress < 0.2 ? 1 : -1;

                // Tilt beak up
                rotation = -20 * flapProgress;

            } else {
                // ==========================================
                // Phase 2 & 3: Deep Dive + Curve Approach (15% - 100%)
                // ==========================================
                
                // We normalize this part of the animation to 0.0 - 1.0
                const flightProgress = (progress - 0.15) / 0.85;
                
                // Bezier Control Points for the "Deep Dive & Float" trajectory
                // P0: Start of this phase (Up in the air)
                const p0x = startLeft - 20;
                const p0y = startTop - 80;

                // P3: Destination (Flick Logo)
                const p3x = endLeft;
                const p3y = endTop;

                // P1: THE DEEP DIVE POINT
                // We pull this WAY down to force the bird to dive deep.
                // It is positioned left of the start, and 500px BELOW the start.
                const p1x = startLeft - 50; 
                const p1y = startTop + 500; 

                // P2: THE FLOAT-IN POINT
                // This control point is ABOVE the destination. 
                // This causes the bird to curve UP from the deep dive, crest, 
                // and then "float down" onto the logo without a sharp drop.
                const p2x = endLeft - 100; // Approach from left
                const p2y = endTop - 80;   // Approach from above

                // Standard Cubic Bezier Formula
                // B(t) = (1-t)³P0 + 3(1-t)²tP1 + 3(1-t)t²P2 + t³P3
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

                // Facing Left
                scaleX = -1;

                // ROTATION LOGIC
                // We want: 
                // 1. Dive down (90deg)
                // 2. Swoop bottom (0deg - flat upside down or level)
                // 3. Curve Up (-45deg)
                // 4. Land Flat (0deg)
                
                if (flightProgress < 0.3) {
                    // Diving down rapidly
                    rotation = -20 + (110 * (flightProgress / 0.3)); // Rotates to ~90 (nose down)
                } else if (flightProgress < 0.7) {
                    // Bottom of curve, swooping up
                    // Interpolate from 90 (down) to -30 (nose up)
                    const curveP = (flightProgress - 0.3) / 0.4; 
                    rotation = 90 - (120 * curveP); 
                } else {
                    // Final float approach
                    // Interpolate from -30 (nose up) to 0 (flat landing)
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
                // Animation complete - Landed state
                bird.classList.remove('flying');
                bird.classList.add('landed');
                bird.style.position = 'absolute';
                bird.style.left = endLeft + 'px';
                bird.style.top = endTop + 'px';
                bird.style.transform = 'scaleX(-1) rotate(0deg)'; // Upright, facing LEFT

                // Transition from landed to idle animation
                setTimeout(() => {
                    bird.classList.remove('landed');
                    bird.classList.add('idle');
                }, 500);
            }
        }

        requestAnimationFrame(animateBird);
    }
});

// Reposition if window resized
window.addEventListener('resize', function() {
    if (!birdHasFlown) {
        positionBird();
    }
});