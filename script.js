/*
    Project: Portfolio
    File: script.js
    @author: Matthew Pool

    MODAL POPUP VERSION: Click card → popup window with details
    ARCHITECTURE: Master IIFE Encapsulation to protect global scope
*/

(() => {
  "use strict";

  // =========================================================================
  // DOM QUERY CACHING (Performance Optimization)
  // =========================================================================
  // Cache these outside the function so we aren't querying the DOM 60x a second
  let stickyZone;
  let bannerContainer;

  // =========================================================================
  // 1. GENERAL UTILITIES & UI
  // =========================================================================

  function showToast(button) {
    const container = button.parentElement.querySelector(".toast-container");
    if (!container) return;

    const existingToast = container.querySelector(".toast");
    if (existingToast) existingToast.remove();

    const toast = document.createElement("span");
    toast.className = "toast";
    toast.textContent = "copied";
    container.appendChild(toast);

    setTimeout(() => toast.classList.add("show"), 10);
    setTimeout(() => {
      toast.classList.remove("show");
      setTimeout(() => toast.remove(), 200);
    }, 500);
  }

  function copyEmail(button) {
    navigator.clipboard.writeText("appbuddy.contact@gmail.com").then(() => {
      showToast(button);
    });
  }

  function copyPhone(button) {
    navigator.clipboard.writeText("903-576-0223").then(() => {
      showToast(button);
    });
  }

  function hideDirections() {
    const popup = document.getElementById("directionsPopup");
    if (popup) popup.classList.remove("show");
  }

  function downloadResume(e) {
    e.preventDefault();
    const isDark = document.body.classList.contains("dark-mode");
    window.open(
      `assets/documents/${isDark ? "resume-dark.pdf" : "resume-light.pdf"}`,
      "_blank"
    );
  }

  function updateResumeLabel() {
    const label = document.getElementById("resume-theme-label");
    if (label) {
      label.textContent = document.body.classList.contains("dark-mode")
        ? "DARK"
        : "LIGHT";
    }
  }

  // =========================================================================
  // 2. DOM CONTENT LOADED (All Initialization)
  // =========================================================================

  document.addEventListener('DOMContentLoaded', () => {
    
    // Initialize cached elements once the DOM is ready
    stickyZone = document.querySelector(".sticky-header-zone");
    bannerContainer = document.querySelector(".portfolio-banner-container");

    // Render footers dynamically FIRST
    renderFooters();

    // --- Theme Management ---
    const themeToggle = document.getElementById("themeToggle");
    const savedTheme = localStorage.getItem("theme");
    
    if (savedTheme === "dark" || (!savedTheme && window.matchMedia("(prefers-color-scheme: dark)").matches)) {
      document.body.classList.add("dark-mode");
    }
    updateResumeLabel();

    if (themeToggle) {
      themeToggle.addEventListener("click", () => {
        document.body.classList.toggle("dark-mode");
        localStorage.setItem("theme", document.body.classList.contains("dark-mode") ? "dark" : "light");
        updateResumeLabel();

        setTimeout(() => {
          if (!birdHasFlown) positionBird();
        }, 350);
      });
    }

    // --- Tab Navigation ---
    document.querySelectorAll('[data-tab-target]').forEach(btn => {
        btn.addEventListener('click', (e) => {
            if (typeof openTab === 'function') openTab(e, btn.getAttribute('data-tab-target'));
        });
    });

    // --- Copy Email ---
    document.querySelectorAll('[data-action="copy-email"]').forEach(btn => {
        btn.addEventListener('click', function() {
            if (typeof copyEmail === 'function') copyEmail(this);
        });
    });

    // --- Copy Phone ---
    document.querySelectorAll('[data-action="copy-phone"]').forEach(btn => {
        btn.addEventListener('click', function() {
            if (typeof copyPhone === 'function') copyPhone(this);
        });
    });
    
    // --- Resume Download ---
    const resumeBtn = document.getElementById('resume-btn');
    if (resumeBtn) {
        resumeBtn.addEventListener('click', (e) => {
            if (typeof downloadResume === 'function') downloadResume(e);
        });
    }

    // --- Project Filtering ---
    document.querySelectorAll('[data-filter]').forEach(btn => {
        btn.addEventListener('click', (e) => {
            if (typeof filterProjects === 'function') filterProjects(btn.getAttribute('data-filter'), e);
        });
    });

    // --- Project Modals ---
    document.querySelectorAll('[data-project-target]').forEach(card => {
        const target = card.getAttribute('data-project-target');
        card.addEventListener('click', () => {
            if (typeof openProjectModal === 'function') openProjectModal(target);
        });
        card.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                if (typeof openProjectModal === 'function') openProjectModal(target);
            }
        });
    });
    
    document.querySelectorAll('[data-action="close-project"]').forEach(btn => {
        btn.addEventListener('click', () => {
            if (typeof closeProjectModal === 'function') closeProjectModal();
        });
    });

    // Modal Click-Anywhere-To-Close
    const projectModal = document.getElementById("project-modal");
    if (projectModal) {
      projectModal.addEventListener("click", function (e) {
        // Ignore clicks on links or buttons (let them work normally)
        if (e.target.closest("a") || e.target.closest("button")) {
            return;
        }
        // Clicking anywhere else closes the modal
        closeProjectModal();
      });
    }

    // --- Contact Modal ---
    document.querySelectorAll('[data-action="open-contact"]').forEach(btn => {
        btn.addEventListener('click', () => {
            if (typeof openContactModal === 'function') openContactModal();
        });
    });
    
    document.querySelectorAll('[data-action="close-contact"]').forEach(btn => {
        btn.addEventListener('click', (e) => {
            if (typeof cancelContactModal === 'function') cancelContactModal(e);
        });
    });

    const contactModal = document.getElementById("contactModal");
    if (contactModal) {
      contactModal.addEventListener("click", function (e) {
        if (e.target === this) closeContactModal();
      });
    }

    const contactForm = document.getElementById('contactForm');
    if (contactForm) {
        contactForm.addEventListener('submit', (e) => {
            if (typeof sendContactMessage === 'function') sendContactMessage(e);
        });
    }

    // --- Popups and Disclaimers ---
    const directionsBtn = document.getElementById("directions-btn");
    if (directionsBtn) {
      directionsBtn.addEventListener("click", function() {
        const popup = document.getElementById("directionsPopup");
        if (popup) popup.classList.add("show");
      });
    }

    const directionsPopup = document.getElementById('directionsPopup');
    if (directionsPopup) {
        directionsPopup.addEventListener('click', () => {
            if (typeof hideDirections === 'function') hideDirections();
        });
        directionsPopup.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' || e.key === 'Escape') {
                if (typeof hideDirections === 'function') hideDirections();
            }
        });
    }

    const wormholeDisclaimer = document.getElementById('wormholeDisclaimerPopup');
    if (wormholeDisclaimer) {
        wormholeDisclaimer.addEventListener('click', () => {
            if (typeof hideWormholeDisclaimer === 'function') hideWormholeDisclaimer();
        });
    }

    document.querySelectorAll('[data-action="show-disclaimer"]').forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.stopPropagation();
            if (typeof showWormholeDisclaimer === 'function') showWormholeDisclaimer();
        });
    });

    // --- Portfolio Preview Toggle ---
    document.querySelectorAll('[data-action="toggle-preview"]').forEach(btn => {
        btn.addEventListener('click', () => {
            if (typeof togglePortfolioPreview === 'function') togglePortfolioPreview();
        });
    });

    // --- Lightbox Navigation ---
    document.querySelectorAll('[data-action="close-lightbox"]').forEach(btn => {
        btn.addEventListener('click', () => {
            if (typeof closeLightbox === 'function') closeLightbox();
        });
    });
    
    document.querySelectorAll('[data-action="prev-lightbox"]').forEach(btn => {
        btn.addEventListener('click', () => {
            if (typeof changeLightboxImage === 'function') changeLightboxImage(-1);
        });
    });
    
    document.querySelectorAll('[data-action="next-lightbox"]').forEach(btn => {
        btn.addEventListener('click', () => {
            if (typeof changeLightboxImage === 'function') changeLightboxImage(1);
        });
    });

    const lightboxElement = document.getElementById("lightbox");
    if (lightboxElement) {
      lightboxElement.addEventListener("click", function (e) {
        if (e.target === this) closeLightbox();
      });
    }

    // Keyboard Accessibility for Modals
    document.addEventListener("keydown", function (e) {
      const lightbox = document.getElementById("lightbox");
      const projectModal = document.getElementById("project-modal");
      const contactModal = document.getElementById("contactModal");
      
      if (lightbox && lightbox.classList.contains("active")) {
          if (e.key === "Escape") closeLightbox();
          else if (e.key === "ArrowLeft") changeLightboxImage(-1);
          else if (e.key === "ArrowRight") changeLightboxImage(1);
      } else if (projectModal && projectModal.classList.contains("show")) {
          if (e.key === "Escape") closeProjectModal();
      } else if (contactModal && contactModal.classList.contains("show")) {
          if (e.key === "Escape") closeContactModal();
      }
    });

  }); // End DOMContentLoaded

  // =========================================================================
  // 3. UI FUNCTIONS
  // =========================================================================

  function togglePortfolioPreview() {
    const modalContent = document.getElementById("project-modal-content");
    if (!modalContent) return;

    const img = modalContent.querySelector(".portfolio-preview-img");
    const text = modalContent.querySelector(".preview-theme-text");
    if (!img || !text) return;

    if (img.src.includes("portfolio-dark.webp")) {
      img.src = "assets/images/portfolio-light.webp";
      img.alt = "High-fidelity preview of this portfolio website currently displaying the light mode theme";
      text.textContent = "PREVIEW: LIGHT MODE";
    } else {
      img.src = "assets/images/portfolio-dark.webp";
      img.alt = "High-fidelity preview of this portfolio website currently displaying the dark mode theme";
      text.textContent = "PREVIEW: DARK MODE";
    }
  }

  function openTab(evt, tabName) {
    const tabContents = document.getElementsByClassName("tab-content");
    for (let i = 0; i < tabContents.length; i++) {
      tabContents[i].classList.remove("active");
    }

    const tabButtons = document.getElementsByClassName("tab-button");
    for (let i = 0; i < tabButtons.length; i++) {
      tabButtons[i].classList.remove("active");
    }

    document.getElementById(tabName).classList.add("active");
    evt.currentTarget.classList.add("active");
    window.scrollTo(0, 0);

    if (tabName !== "home") {
      flyBirdBack();
    }

    if (!birdHasFlown) {
      requestAnimationFrame(() => positionBird());
    }
  }

  function renderFooters() {
    const footers = document.querySelectorAll('.dynamic-footer');
    const currentYear = new Date().getFullYear(); // Automatically gets the current year!

    footers.forEach(footer => {
      // Grab the custom text you left inside the placeholder
      const customText = footer.innerHTML;

      // Rebuild the HTML
      footer.innerHTML = `
        <div class="footer-metallic-black">
          ${customText}
          
          <div class="unified-header-inner mt-20">
            <span class="uh-name font-weight-normal"><b>Matthew Pool</b></span>
            <span class="uh-divider">|</span>
            <span class="uh-email relative inline-flex items-center uh-email-pad">
              <a href="mailto:appbuddy.contact@gmail.com">appbuddy.contact@gmail.com</a>
              <button data-action="copy-email" data-theme="light" aria-label="Copy Email Address" class="btn-copy-email right-aligned" title="Copy email">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="rgba(255, 255, 255, 0.9)" stroke-width="2" aria-hidden="true">
                      <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
                      <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
                  </svg>
              </button>
              <span class="toast-container"></span>
            </span>
            <span class="uh-divider">|</span>
            <span class="uh-phone relative inline-flex items-center">
              <a href="tel:+19035760223">903-576-0223</a>
              <button data-action="copy-phone" data-theme="light" aria-label="Copy Phone Number" class="btn-copy-email right-aligned" title="Copy phone">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="rgba(255, 255, 255, 0.9)" stroke-width="2" aria-hidden="true">
                      <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
                      <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
                  </svg>
              </button>
              <span class="toast-container"></span>
            </span>
          </div>
        </div>
        <div class="copyright-notice">
            &copy; ${currentYear} Matthew Pool. All rights reserved.
        </div>
      `;
      
      footer.classList.remove('dynamic-footer');
    });
  }

  // =========================================================================
  // 4. STICKY HEADER & LAYOUT LOCK
  // =========================================================================
  
  const BANNER_SHOW_FRACTION = 0;
  let STICKY_LOCK_PX = 170;

  function updateStickyLock() {
    requestAnimationFrame(() => {
      requestAnimationFrame(() => {
        if (!stickyZone || !bannerContainer) return;

        const bannerHeight = bannerContainer.getBoundingClientRect().height;
        if (bannerHeight <= 0) {
          setTimeout(updateStickyLock, 50);
          return;
        }

        const visibleStrip = bannerHeight * BANNER_SHOW_FRACTION;
        STICKY_LOCK_PX = Math.round(bannerHeight - visibleStrip);
        stickyZone.style.top = `-${STICKY_LOCK_PX}px`;
      });
    });
  }

  window.addEventListener("load", () => {
    const _bannerImg = document.querySelector(".portfolio-banner");
    if (_bannerImg) {
      if (_bannerImg.complete && _bannerImg.naturalHeight > 0) {
        updateStickyLock();
      } else {
        _bannerImg.addEventListener("load", updateStickyLock);
      }
    }
  });
  
  window.addEventListener("resize", updateStickyLock, { passive: true });
  
  // =========================================================================
  // 5. BIRD ANIMATION SYSTEM
  // =========================================================================

  let birdHasFlown = false;
  let birdOnFlick = false;
  let isPositioned = false;
  let isReady = false;
  let _flightRafId = null;
  let _resizeTimer;
  let _lastWindowWidth = window.innerWidth;

  const bird = document.getElementById("bird");
  const birdTooltip = document.getElementById("bird-tooltip");

  function cancelFlight() {
    if (_flightRafId !== null) {
      cancelAnimationFrame(_flightRafId);
      _flightRafId = null;
    }
    if (bird) {
      bird.classList.remove("flying", "landed");
      bird.classList.add("idle");
      bird.style.transform = "scaleX(1) rotate(0deg)";
    }
  }

  function positionTooltip() {
    if (!birdTooltip || !bird) return;

    const birdRect = bird.getBoundingClientRect();
    birdTooltip.style.top = Math.max(4, birdRect.top + window.scrollY - 44) + "px";
    birdTooltip.style.bottom = "auto";

    if (birdOnFlick) {
      birdTooltip.style.left = birdRect.left + window.scrollX + "px";
      birdTooltip.style.right = "auto";
      birdTooltip.classList.add("flipped");
    } else {
      birdTooltip.style.left = birdRect.left + window.scrollX - 40 + "px";
      birdTooltip.style.right = "auto";
      birdTooltip.classList.remove("flipped");
    }
  }

  function showBirdTooltip() {
    if (!birdTooltip || !bird || bird.classList.contains("flying")) return;
    positionTooltip();
    birdTooltip.classList.add("visible");
  }

  function hideBirdTooltip() {
    if (!birdTooltip) return;
    birdTooltip.classList.remove("visible");
  }

  function handleBirdFlightReset() {
    if (window.innerWidth === _lastWindowWidth) return;
    _lastWindowWidth = window.innerWidth;

    clearTimeout(_resizeTimer);
    _resizeTimer = setTimeout(() => {
      cancelFlight();
      birdHasFlown = false;
      birdOnFlick = false;
      isReady = false;
      hideBirdTooltip();

      updateStickyLock();
      requestAnimationFrame(() => {
        requestAnimationFrame(() => {
          positionBird(true);
          setTimeout(() => { isReady = true; }, 500);
        });
      });
    }, 150);
  }

  window.addEventListener("resize", handleBirdFlightReset, { passive: true });

  function getBirdDocCoords() {
    const bottomShelf = document.querySelectorAll(".shelf-container")[1];
    if (!bottomShelf) return null;

    const shelfRect = bottomShelf.getBoundingClientRect();
    const BIRD_WIDTH = 60;
    const RIGHT_MARGIN = 4;

    return {
      left: shelfRect.right + window.scrollX - BIRD_WIDTH - RIGHT_MARGIN,
      top: shelfRect.top + window.scrollY - BIRD_WIDTH + 10,
    };
  }

  function updateRestingBirdPosition() {
    const bottomShelf = document.querySelectorAll(".shelf-container")[1];
    if (!bottomShelf || !bird) return;

    if (window.scrollY >= STICKY_LOCK_PX) {
      const shelfRect = bottomShelf.getBoundingClientRect();
      bird.style.position = "fixed";
      bird.style.top = (shelfRect.top - 50) + "px";
      bird.style.left = (shelfRect.right - 64) + "px";
    } else {
      const coords = getBirdDocCoords();
      if (coords) {
        bird.style.position = "absolute";
        bird.style.top = coords.top + "px";
        bird.style.left = coords.left + "px";
      }
    }
  }

  function positionBird(force = false) {
    if ((birdHasFlown && !force) || !bird) return;

    bird.classList.remove("flying", "idle", "landed");
    bird.style.transform = "scaleX(1) rotate(0deg)";
    
    updateRestingBirdPosition(); 

    bird.style.opacity = "1";
    bird.classList.add("landed");

    setTimeout(() => {
      bird.classList.remove("landed");
      bird.classList.add("idle");
    }, 500);

    isPositioned = true;
  }

  function flyBirdBack() {
    if (!birdHasFlown || !bird) return;

    hideBirdTooltip();
    birdOnFlick = false;

    bird.classList.remove("idle", "landed");
    bird.classList.add("flying");
    bird.style.position = "absolute";

    const currentLeft = parseFloat(bird.style.left);
    const currentTop = parseFloat(bird.style.top);
    const coords = getBirdDocCoords();
    if (!coords) return;

    const targetLeft = coords.left;
    const targetTop = coords.top;
    const cpX = (currentLeft + targetLeft) / 2;
    const cpY = Math.min(currentTop, targetTop) - 300;

    const duration = 2500;
    const startTime = performance.now();

    function animateReturn(currentTime) {
      const elapsed = currentTime - startTime;
      const progress = Math.min(elapsed / duration, 1);

      const t = 1 - Math.pow(1 - progress, 3);
      const invT = 1 - t;

      const x = invT * invT * currentLeft + 2 * invT * t * cpX + t * t * targetLeft;
      const y = invT * invT * currentTop + 2 * invT * t * cpY + t * t * targetTop;

      const dx = 2 * invT * (cpX - currentLeft) + 2 * t * (targetLeft - cpX);
      const dy = 2 * invT * (cpY - currentTop) + 2 * t * (targetTop - cpY);

      let angle = Math.atan2(dy, dx) * (180 / Math.PI);
      const scaleX = Math.abs(angle) > 90 ? -1 : 1;
      let visualRotation = angle;
      if (scaleX === -1) {
        visualRotation = angle - 180;
        if (visualRotation < -180) visualRotation += 360;
      }
      if (dy > 0) visualRotation *= 0.3;
      if (progress > 0.6) visualRotation *= 1 - (progress - 0.6) / 0.4;
      visualRotation = Math.max(-25, Math.min(25, visualRotation));

      bird.style.left = x + "px";
      bird.style.top = y + "px";
      bird.style.transform = `scaleX(${scaleX}) rotate(${visualRotation}deg)`;

      if (progress < 1) {
        _flightRafId = requestAnimationFrame(animateReturn);
      } else {
        _flightRafId = null;
        bird.classList.remove("flying");
        bird.classList.add("landed");

        birdHasFlown = false; 
        updateRestingBirdPosition(); 

        bird.style.transform = "scaleX(1) rotate(0deg)";
        isReady = false;

        setTimeout(() => {
          bird.classList.remove("landed");
          bird.classList.add("idle");
        }, 500);

        setTimeout(() => { isReady = true; }, 1000);
      }
    }

    _flightRafId = requestAnimationFrame(animateReturn);
  }

  // Bird Initialization
  window.addEventListener("load", function () {
    if (birdTooltip) document.body.appendChild(birdTooltip);
    if (bird) {
      document.body.appendChild(bird);
      bird.classList.remove("flying", "idle", "landed");
    }

    positionBird();

    setTimeout(() => { isReady = true; }, 1000);

    if (birdTooltip) {
      setTimeout(() => {
        showBirdTooltip();
        setTimeout(hideBirdTooltip, 2500);
      }, 1800);

      setInterval(() => {
        if (bird && bird.classList.contains("flying")) return;
        showBirdTooltip();
        setTimeout(hideBirdTooltip, 2500);
      }, 7000);
    }
  });

  // Outbound Flight Scroll Listener
  window.addEventListener("scroll", function () {
    const homeTab = document.getElementById("home");
    const isHomeActive = homeTab && homeTab.classList.contains("active");
    const flickLogo = document.querySelector(".flick-logo");

    if (!birdHasFlown && isPositioned && isReady && bird) {
      if (isHomeActive && flickLogo && window.scrollY >= STICKY_LOCK_PX) {
        birdHasFlown = true;
        hideBirdTooltip();

        bird.classList.remove("landed", "idle");
        bird.classList.add("flying");
        bird.style.position = "absolute";

        const birdRect = bird.getBoundingClientRect();
        const startLeft = birdRect.left + window.scrollX;
        const startTop = birdRect.top + window.scrollY;

        const flickRect = flickLogo.getBoundingClientRect();
        const endLeft = flickRect.left + window.scrollX + flickRect.width / 2 - 30;
        const endTop = flickRect.top + window.scrollY - 36;

        const duration = 2800;
        const startTime = performance.now();

        function animateBird(currentTime) {
          const elapsed = currentTime - startTime;
          const progress = Math.min(elapsed / duration, 1);

          let x, y, rotation, scaleX;

          if (progress < 0.15) {
            const fp = progress / 0.15;
            x = startLeft - 20 * fp;
            y = startTop - 80 * fp;
            scaleX = fp < 0.2 ? 1 : -1;
            rotation = -20 * fp;
          } else {
            const fp2 = (progress - 0.15) / 0.85;

            const p0x = startLeft - 20, p0y = startTop - 80;
            const p3x = endLeft, p3y = endTop;
            const p1x = startLeft - 50, p1y = startTop + 500;
            const p2x = endLeft - 100, p2y = endTop - 80;

            const t = fp2, invT = 1 - t;
            x = Math.pow(invT, 3) * p0x + 3 * Math.pow(invT, 2) * t * p1x + 3 * invT * Math.pow(t, 2) * p2x + Math.pow(t, 3) * p3x;
            y = Math.pow(invT, 3) * p0y + 3 * Math.pow(invT, 2) * t * p1y + 3 * invT * Math.pow(t, 2) * p2y + Math.pow(t, 3) * p3y;

            scaleX = -1;
            if (fp2 < 0.3) rotation = -20 + 110 * (fp2 / 0.3);
            else if (fp2 < 0.7) rotation = 90 - 120 * ((fp2 - 0.3) / 0.4);
            else rotation = -30 + 30 * ((fp2 - 0.7) / 0.3);
          }

          bird.style.left = x + "px";
          bird.style.top = y + "px";
          bird.style.transform = `scaleX(${scaleX}) rotate(${rotation}deg)`;

          if (progress < 1) {
            _flightRafId = requestAnimationFrame(animateBird);
          } else {
            _flightRafId = null;
            bird.classList.remove("flying");
            bird.classList.add("landed");
            bird.style.position = "absolute";
            bird.style.left = endLeft + "px";
            bird.style.top = endTop + "px";
            bird.style.transform = "scaleX(-1) rotate(0deg)";

            setTimeout(() => {
              bird.classList.remove("landed");
              bird.classList.add("idle");
              birdOnFlick = true;
            }, 500);
          }
        }

        _flightRafId = requestAnimationFrame(animateBird);
      } else {
        updateRestingBirdPosition();
      }
    }
  }, { passive: true });

  // =========================================================================
  // 6. PORTFOLIO & MODAL SYSTEM
  // =========================================================================

  function filterProjects(category, event) {
    const filterButtons = document.querySelectorAll(".filter-btn");
    filterButtons.forEach((btn) => btn.classList.remove("active"));
    event.currentTarget.classList.add("active");

    const projectCards = document.querySelectorAll(".project-card");
    projectCards.forEach((card) => {
      card.style.display =
        category === "all" || card.dataset.category === category
          ? "block"
          : "none";
    });
  }

  function openProjectModal(projectId) {
    const modal = document.getElementById("project-modal");
    const modalContent = document.getElementById("project-modal-content");
    const detailsElement = document.getElementById(`details-${projectId}`);
    
    if (!modal || !modalContent || !detailsElement) return;

    modalContent.innerHTML = detailsElement.innerHTML;
    
    const modalTitle = modalContent.querySelector('h3');
    if (modalTitle) modalTitle.id = 'project-modal-title';
    
    const previewBtn = modalContent.querySelector('[data-action="toggle-preview"]');
    if (previewBtn) {
        previewBtn.addEventListener('click', function(e) {
            e.stopPropagation(); 
            if (typeof togglePortfolioPreview === 'function') togglePortfolioPreview();
        });
    }

    modal.classList.add("show");
    document.body.style.overflow = "hidden";
    trapFocus(modal);

    const modalBody = modal.querySelector('.project-modal-body');
    
    requestAnimationFrame(() => {
        modal.scrollTop = 0; 
        if (modalBody) {
            modalBody.scrollTop = 0; 
        }
        modalContent.scrollTop = 0;
    });
  }

  function closeProjectModal() {
    const modal = document.getElementById("project-modal");
    if (!modal) return;
    modal.classList.remove("show");
    document.body.style.overflow = "";
  }

  function showWormholeDisclaimer() {
    const popup = document.getElementById("wormholeDisclaimerPopup");
    if (popup) popup.classList.add("show");
  }

  // Utility: Trap focus inside a specific element
  function trapFocus(modalElement) {
    const focusableElements = modalElement.querySelectorAll(
      'a[href], button:not([disabled]), textarea:not([disabled]), input:not([disabled]), [tabindex]:not([tabindex="-1"])'
    );
    
    if (focusableElements.length === 0) return;

    const firstElement = focusableElements[0];
    const lastElement = focusableElements[focusableElements.length - 1];

    firstElement.focus();

    modalElement.removeEventListener('keydown', modalElement._focusTrap);

    modalElement._focusTrap = function(e) {
      const isTabPressed = e.key === 'Tab' || e.keyCode === 9;
      if (!isTabPressed) return;

      if (e.shiftKey) { 
        if (document.activeElement === firstElement) {
          lastElement.focus();
          e.preventDefault();
        }
      } else { 
        if (document.activeElement === lastElement) {
          firstElement.focus();
          e.preventDefault();
        }
      }
    };

    modalElement.addEventListener('keydown', modalElement._focusTrap);
  }

  // =========================================================================
  // CONTACT MODAL SYSTEM
  // =========================================================================

  function openContactModal() {
    const modal = document.getElementById('contactModal');
    if(!modal) return;

    modal.classList.add('show');
    document.body.style.overflow = 'hidden';
    trapFocus(modal);

    const contactForm = document.getElementById('contactForm');
    const sendBtn = document.getElementById('sendContactBtn');
    
    if (contactForm && sendBtn) {
        sendBtn.disabled = true; 
        contactForm.addEventListener('input', validateContactForm);
    }
  }

  function closeContactModal() {
    const modal = document.getElementById('contactModal');
    if(!modal) return;

    modal.classList.remove('show');
    document.body.style.overflow = ''; 
    
    const contactForm = document.getElementById('contactForm');
    if (contactForm) {
        contactForm.reset();
        contactForm.removeEventListener('input', validateContactForm);
    }
  }

  function cancelContactModal(event) {
    if (event) event.preventDefault();
    closeContactModal();
  }

  function validateContactForm() {
    const name = document.getElementById('senderName').value.trim();
    const email = document.getElementById('senderEmail').value.trim();
    const message = document.getElementById('message').value.trim();
    const sendBtn = document.getElementById('sendContactBtn');
    
    const isEmailValid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    
    if (name && isEmailValid && message) {
        sendBtn.disabled = false;
        sendBtn.style.opacity = '1';
        sendBtn.style.cursor = 'pointer';
    } else {
        sendBtn.disabled = true;
        sendBtn.style.opacity = '0.5';
        sendBtn.style.cursor = 'not-allowed';
    }
  }

  function sendContactMessage(event) {
    event.preventDefault(); 
    
    const name = document.getElementById('senderName').value.trim();
    const message = document.getElementById('message').value.trim();
    
    const encodedSubject = encodeURIComponent(`CONTACT-MESSAGE - ${name}`);
    const encodedBody = encodeURIComponent(message);
    
    window.location.href = `mailto:appbuddy.contact@gmail.com?subject=${encodedSubject}&body=${encodedBody}`;
    
    closeContactModal();
  }
  
  // =========================================================================
  // 7. LIGHTBOX SYSTEM
  // =========================================================================
  
  let currentImageIndex = 0;
  let lightboxImages = [];

  function initLightbox() {
    const clickableImages = document.querySelectorAll(
      ".screenshot-grid img, .project-image-card img, .image-card img, .buddy-screenshot-grid img, .mario-image, .paradox-image"
    );

    clickableImages.forEach((img) => {
      img.style.cursor = "pointer";
      img.addEventListener("click", function (e) {
        e.stopPropagation();
        openLightbox(this, Array.from(clickableImages));
      });
    });
  }

  function openLightbox(clickedImg, allImages) {
    lightboxImages = allImages;
    currentImageIndex = lightboxImages.indexOf(clickedImg);

    const lightbox = document.getElementById("lightbox");
    const lightboxImg = document.getElementById("lightbox-img");
    const lightboxCaption = document.getElementById("lightbox-caption");

    if (!lightbox || !lightboxImg || !lightboxCaption) return;

    lightboxImg.src = clickedImg.src;
    lightboxCaption.textContent = clickedImg.alt || "";
    lightbox.classList.add("active");
    document.body.style.overflow = "hidden";
  }

  function closeLightbox() {
    const lightbox = document.getElementById("lightbox");
    if (lightbox) {
        lightbox.classList.remove("active");
        document.body.style.overflow = "";
    }
  }

  function changeLightboxImage(direction) {
    if (lightboxImages.length === 0) return;
    
    currentImageIndex = (currentImageIndex + direction + lightboxImages.length) % lightboxImages.length;

    const lightboxImg = document.getElementById("lightbox-img");
    const lightboxCaption = document.getElementById("lightbox-caption");

    if (lightboxImg && lightboxCaption) {
        lightboxImg.src = lightboxImages[currentImageIndex].src;
        lightboxCaption.textContent = lightboxImages[currentImageIndex].alt || "";
    }
  }

  window.addEventListener("load", initLightbox);

})();