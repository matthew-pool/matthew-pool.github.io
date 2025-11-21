/*
	Project: Portfolio
    File: script.js
    @version: 1.2
	@author: Matthew Pool
	@updated: 2025-20-11
*/

	// Bird animation logic
	let birdHasFlown = false;
	let isPositioned = false;
	let isReady = false;
	const bird = document.getElementById('bird');

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
		bird.classList.remove('idle');
		bird.classList.add('flying');
		
		// Get current absolute position
		const birdRect = bird.getBoundingClientRect();
		const currentLeft = birdRect.left + window.scrollX;
		const currentTop = birdRect.top + window.scrollY;
		
		// Get target absolute position (Refactor tab)
		const refactorTab = document.querySelector('.tab-button:nth-child(3)');
		if (!refactorTab) return;
		
		const rect = refactorTab.getBoundingClientRect();
		const targetLeft = rect.left + window.scrollX + rect.width / 2 - 30;
		const targetTop = rect.top + window.scrollY - 70;
		
		// Switch to absolute positioning for flight back
		bird.style.position = 'absolute';
		bird.style.left = currentLeft + 'px';
		bird.style.top = currentTop + 'px';
		
		// Animate flight back
		const duration = 1500; // 1.5 seconds for return flight
		const startTime = performance.now();
		
		function animateReturn(currentTime) {
			const elapsed = currentTime - startTime;
			const progress = Math.min(elapsed / duration, 1);
			const eased = 1 - Math.pow(1 - progress, 3); // Ease out cubic
			
			const x = currentLeft + ((targetLeft - currentLeft) * eased);
			const y = currentTop + ((targetTop - currentTop) * eased);
			const rotation = -45 + (45 * eased); // Rotate from -45 to 0
			
			bird.style.left = x + 'px';
			bird.style.top = y + 'px';
			bird.style.transform = `rotate(${rotation}deg)`;
			
			if (progress < 1) {
				requestAnimationFrame(animateReturn);
			} else {
				// Return complete - stay at absolute position and add idle flapping
				bird.classList.remove('flying');
				bird.classList.add('idle'); // Add idle class for sporadic flapping
				bird.style.transform = 'rotate(0deg)';
				bird.style.position = 'absolute'; // Explicitly set to absolute
				bird.style.left = targetLeft + 'px';
				bird.style.top = targetTop + 'px';
				birdHasFlown = false;
				isReady = false;
				
				// Store the absolute position
				bird.dataset.initialLeft = targetLeft;
				bird.dataset.initialTop = targetTop;
				
				// Re-enable animation after delay
				setTimeout(() => {
					isReady = true;
				}, 1000);
			}
		}
		
		requestAnimationFrame(animateReturn);
	}

	// Position bird on Refactor tab
	function positionBird() {
		// Only position if bird hasn't flown yet
		if (birdHasFlown) return;
		
		const refactorTab = document.querySelector('.tab-button:nth-child(3)');
		if (refactorTab) {
			const rect = refactorTab.getBoundingClientRect();
			const leftPos = rect.left + window.scrollX + rect.width / 2 - 30;
			const topPos = rect.top + window.scrollY - 70;
			
			// Store initial absolute position for animation
			bird.dataset.initialLeft = leftPos;
			bird.dataset.initialTop = topPos;
			
			// Position the bird at absolute position (not fixed)
			bird.style.left = leftPos + 'px';
			bird.style.top = topPos + 'px';
			bird.style.position = 'absolute'; // Changed from 'fixed' to 'absolute'
			bird.style.zIndex = '10000';
			
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
			bird.classList.add('flying');
			
			// Convert absolute position to viewport coordinates for smooth animation
			const absoluteLeft = parseFloat(bird.dataset.initialLeft);
			const absoluteTop = parseFloat(bird.dataset.initialTop);
			const startLeft = absoluteLeft - window.scrollX;
			const startTop = absoluteTop - window.scrollY;
			
			// Switch to fixed positioning for the flight animation
			bird.style.position = 'fixed';
			bird.style.left = startLeft + 'px';
			bird.style.top = startTop + 'px';
			
			// Find Flick logo position and calculate absolute position
			const flickLogo = document.querySelector('.flick-logo');
			let endLeft = absoluteLeft - 600;
			let endTop = absoluteTop + 600;
			
			if (flickLogo) {
				const flickRect = flickLogo.getBoundingClientRect();
				// Calculate absolute position (viewport position + scroll offset)
				endLeft = flickRect.left + window.scrollX + (flickRect.width / 2) - 30;
				endTop = flickRect.top + window.scrollY - 28;
			}
			
			// Animate using JavaScript
			const duration = 2500; // 2.5 seconds
			const startTime = performance.now();
			
			function animateBird(currentTime) {
				const elapsed = currentTime - startTime;
				const progress = Math.min(elapsed / duration, 1);
				
				// Animation path with upward flap then dive
				let x, y, rotation;
				if (progress < 0.15) {
					// Flap upward
					const flapProgress = progress / 0.15;
					x = startLeft - (30 * flapProgress);
					y = startTop - (80 * flapProgress);
					rotation = -10 * flapProgress;
				} else if (progress < 0.3) {
					// Continue upward
					const flapProgress = (progress - 0.15) / 0.15;
					x = startLeft - 30 - (30 * flapProgress);
					y = startTop - 80 - (20 * flapProgress);
					rotation = -10 - (5 * flapProgress);
				} else {
					// Dive down to target (convert to viewport coordinates)
					const diveProgress = (progress - 0.3) / 0.7;
					const diveEased = diveProgress * diveProgress; // Accelerate
					const startDiveX = startLeft - 60;
					const startDiveY = startTop - 100;
					// Convert endLeft/endTop from absolute to viewport coordinates
					const viewportEndLeft = endLeft - window.scrollX;
					const viewportEndTop = endTop - window.scrollY;
					x = startDiveX + ((viewportEndLeft - startDiveX) * diveEased);
					y = startDiveY + ((viewportEndTop - startDiveY) * diveEased);
					rotation = -15 + (-30 * diveProgress);
				}
				
				bird.style.left = x + 'px';
				bird.style.top = y + 'px';
				bird.style.transform = `rotate(${rotation}deg)`;
				
				if (progress < 1) {
					requestAnimationFrame(animateBird);
				} else {
					// Animation complete - switch to absolute positioning and idle flapping
					bird.classList.remove('flying');
					bird.classList.add('idle');
					bird.style.position = 'absolute';
					bird.style.left = endLeft + 'px';
					bird.style.top = endTop + 'px';
					bird.style.transform = 'rotate(0deg)';
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