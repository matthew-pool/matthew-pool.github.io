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

  window.copyEmail = function (button) {
    navigator.clipboard.writeText("mathyou.me@gmail.com").then(() => {
      showToast(button);
    });
  };

// Bind the event listener dynamically to the ID you added!
  const directionsBtn = document.getElementById("directions-btn");
  if (directionsBtn) {
    directionsBtn.addEventListener("click", function() {
      document.getElementById("directionsPopup").classList.add("show");
    });
  }
  
  window.hideDirections = function () {
    document.getElementById("directionsPopup").classList.remove("show");
  };

  window.downloadResume = function (e) {
    e.preventDefault();
    const isDark = document.body.classList.contains("dark-mode");
    window.open(
      `assets/documents/${isDark ? "resume-dark.pdf" : "resume-light.pdf"}`,
      "_blank"
    );
  };

  function updateResumeLabel() {
    const label = document.getElementById("resume-theme-label");
    if (label) {
      label.textContent = document.body.classList.contains("dark-mode")
        ? "DARK"
        : "LIGHT";
    }
  }

  // =========================================================================
  // 2. THEME MANAGEMENT
  // =========================================================================
  
  const themeToggle = document.getElementById("themeToggle");
  const savedTheme = localStorage.getItem("theme");
  
  if (savedTheme === "dark") {
    document.body.classList.add("dark-mode");
  } else if (
    !savedTheme &&
    window.matchMedia("(prefers-color-scheme: dark)").matches
  ) {
    document.body.classList.add("dark-mode");
  }

  updateResumeLabel();

  if (themeToggle) {
    themeToggle.addEventListener("click", () => {
      document.body.classList.toggle("dark-mode");
      localStorage.setItem(
        "theme",
        document.body.classList.contains("dark-mode") ? "dark" : "light"
      );
      updateResumeLabel();

      setTimeout(() => {
        if (!birdHasFlown) positionBird();
      }, 350);
    });
  }

  window.togglePortfolioPreview = function () {
    const img = document.getElementById("portfolio-preview-img");
    const text = document.getElementById("preview-theme-text");

    if (img.src.includes("portfolio-dark.png")) {
      img.src = "assets/images/portfolio-light.png";
      img.alt = "High-fidelity preview of this portfolio website currently displaying the light mode theme";
      text.textContent = "PREVIEW: LIGHT MODE";
    } else {
      img.src = "assets/images/portfolio-dark.png";
      img.alt = "High-fidelity preview of this portfolio website currently displaying the dark mode theme";
      text.textContent = "PREVIEW: DARK MODE";
    }
  };

  // =========================================================================
  // 3. TAB NAVIGATION
  // =========================================================================

  window.openTab = function (evt, tabName) {
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
  };

  // =========================================================================
  // 4. STICKY HEADER & LAYOUT LOCK
  // =========================================================================
  
  const BANNER_SHOW_FRACTION = 0.12;
  let STICKY_LOCK_PX = 170;

  function updateStickyLock() {
    requestAnimationFrame(() => {
      requestAnimationFrame(() => {
        const stickyZone = document.querySelector(".sticky-header-zone");
        const bannerContainer = document.querySelector(".portfolio-banner-container");
        const toggleWrapper = document.querySelector(".theme-toggle-wrapper");

        if (!stickyZone || !bannerContainer) return;

        const bannerHeight = bannerContainer.getBoundingClientRect().height;
        if (bannerHeight <= 0) {
          setTimeout(updateStickyLock, 50);
          return;
        }

        const visibleStrip = bannerHeight * BANNER_SHOW_FRACTION;
        STICKY_LOCK_PX = Math.round(bannerHeight - visibleStrip);
        stickyZone.style.top = `-${STICKY_LOCK_PX}px`;

        if (toggleWrapper) {
          const toggleHeight = toggleWrapper.getBoundingClientRect().height || 36;
          const toggleTop = Math.max(4, Math.round((visibleStrip - toggleHeight) / 2));
          toggleWrapper.style.top = `${toggleTop}px`;
        }
      });
    });
  }

  const _bannerImg = document.querySelector(".portfolio-banner");
  if (_bannerImg) {
    if (_bannerImg.complete && _bannerImg.naturalHeight > 0) {
      updateStickyLock();
    } else {
      _bannerImg.addEventListener("load", updateStickyLock);
    }
  }

  window.addEventListener("load", updateStickyLock);
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

  window.filterProjects = function (category, event) {
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
  };

  window.openProjectModal = function (projectId) {
    const modal = document.getElementById("project-modal");
    const modalContent = document.getElementById("project-modal-content");
    const detailsElement = document.getElementById(`details-${projectId}`);
    
    if (!modal || !modalContent || !detailsElement) return;

    modalContent.innerHTML = detailsElement.innerHTML;
    modal.classList.add("show");
    document.body.style.overflow = "hidden";
    
    const modalBody = modal.querySelector('.project-modal-body');
    
    requestAnimationFrame(() => {
        modal.scrollTop = 0; 
        if (modalBody) {
            modalBody.scrollTop = 0; 
        }
        modalContent.scrollTop = 0;
    });
  };

  window.closeProjectModal = function () {
    const modal = document.getElementById("project-modal");
    if (!modal) return;
    modal.classList.remove("show");
    document.body.style.overflow = "";
  };

  window.showWormholeDisclaimer = function () {
    const popup = document.getElementById("wormholeDisclaimerPopup");
    if (popup) popup.classList.add("show");
  };

  window.hideWormholeDisclaimer = function () {
    const popup = document.getElementById("wormholeDisclaimerPopup");
    if (popup) popup.classList.remove("show");
  };

const modal = document.getElementById("project-modal");
  if (modal) {
    modal.addEventListener("click", function (e) {
      // Ignore clicks on links or buttons (let them work normally)
      if (e.target.closest("a") || e.target.closest("button")) {
          return;
      }
      // Clicking anywhere else closes the modal
      window.closeProjectModal();
    });
  }

  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") window.closeProjectModal();
  });

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
        window.openLightbox(this, Array.from(clickableImages));
      });
    });
  }

  window.openLightbox = function (clickedImg, allImages) {
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
  };

  window.closeLightbox = function () {
    const lightbox = document.getElementById("lightbox");
    if (lightbox) {
        lightbox.classList.remove("active");
        document.body.style.overflow = "";
    }
  };

  window.changeLightboxImage = function (direction) {
    if (lightboxImages.length === 0) return;
    
    currentImageIndex = (currentImageIndex + direction + lightboxImages.length) % lightboxImages.length;

    const lightboxImg = document.getElementById("lightbox-img");
    const lightboxCaption = document.getElementById("lightbox-caption");

    if (lightboxImg && lightboxCaption) {
        lightboxImg.src = lightboxImages[currentImageIndex].src;
        lightboxCaption.textContent = lightboxImages[currentImageIndex].alt || "";
    }
  };

  const lightboxElement = document.getElementById("lightbox");
  if (lightboxElement) {
    lightboxElement.addEventListener("click", function (e) {
      if (e.target === this) window.closeLightbox();
    });
  }

  document.addEventListener("keydown", function (e) {
    const lightbox = document.getElementById("lightbox");
    if (!lightbox || !lightbox.classList.contains("active")) return;
    
    if (e.key === "Escape") window.closeLightbox();
    else if (e.key === "ArrowLeft") window.changeLightboxImage(-1);
    else if (e.key === "ArrowRight") window.changeLightboxImage(1);
  });

  window.addEventListener("load", initLightbox);

})();