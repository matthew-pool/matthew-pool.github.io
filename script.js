/*
    Project: Portfolio
    File: script.js
    @author: Matthew Pool
    
    MODAL POPUP VERSION: Click card → popup window with details
*/

/* Email */
function copyEmail(button) {
  navigator.clipboard.writeText("mathyou.me@gmail.com").then(() => {
    showToast(button);
  });
}

/* Directions popup */
function showDirections() {
  document.getElementById("directionsPopup").classList.add("show");
}

function hideDirections() {
  document.getElementById("directionsPopup").classList.remove("show");
}

function showToast(button) {
  const container = button.parentElement.querySelector(".toast-container");
  if (!container) return;

  const existingToast = container.querySelector(".toast");
  if (existingToast) {
    existingToast.remove();
  }

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

function downloadResume(e) {
  e.preventDefault();
  const isDark = document.body.classList.contains("dark-mode");
  window.open(
    `assets/documents/${isDark ? "resume-dark.pdf" : "resume-light.pdf"}`,
    "_blank",
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

function syncBirdToScroll() {
  const bird = document.getElementById("bird");
  if (!bird || birdHasFlown) return;

  if (isPositioned) {
    const homeTab = document.getElementById("home");
    if (!homeTab || !homeTab.classList.contains("active")) return;

    const bannerEl = document.querySelector(".portfolio-banner-container");
    if (!bannerEl) return;
    const bannerRect = bannerEl.getBoundingClientRect();
    bird.style.top = bannerRect.bottom + window.scrollY - 53 + "px";
    return;
  }

  const offset = Math.min(window.scrollY, STICKY_LOCK_PX);
  bird.style.setProperty("--scroll-offset", `-${offset}px`);
}

window.addEventListener("scroll", syncBirdToScroll, { passive: true });

// Bird animation variables
let birdHasFlown = false;
let isPositioned = false;
let isReady = false;
const bird = document.getElementById("bird");

// Reset bird state on page load
window.addEventListener("load", function () {
  birdHasFlown = false;
  isPositioned = false;
  isReady = false;

  bird.classList.remove("flying", "idle", "landed");
  positionBird();

  setTimeout(() => {
    isReady = true;
  }, 1000);

  const birdTooltip = document.getElementById("bird-tooltip");
  if (birdTooltip) {
    setTimeout(() => {
      birdTooltip.classList.add("visible");
      setTimeout(() => birdTooltip.classList.remove("visible"), 3500);
    }, 1800);

    bird.addEventListener("mouseenter", () =>
      birdTooltip.classList.add("visible"),
    );
    bird.addEventListener("mouseleave", () =>
      birdTooltip.classList.remove("visible"),
    );
  }
});

// Dark mode toggle
const themeToggle = document.getElementById("themeToggle");
const body = document.body;

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

themeToggle.addEventListener("click", () => {
  document.body.classList.toggle("dark-mode");
  const currentTheme = document.body.classList.contains("dark-mode")
    ? "dark"
    : "light";
  localStorage.setItem("theme", currentTheme);

  updateResumeLabel();

  setTimeout(() => {
    if (!birdHasFlown) {
      positionBird();
    }
  }, 350);
});

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
}

// ─────────────────────────────────────────────────────────────
// STICKY LOCK + TOGGLE ALIGNMENT
// Both the zone top and toggle top derive from the same rendered
// banner height so they always agree at every viewport width.
// ─────────────────────────────────────────────────────────────
const BANNER_SHOW_FRACTION = 0.34; // bottom N% of banner stays visible when locked
let STICKY_LOCK_PX = 170; // overwritten on every updateStickyLock call

function updateStickyLock() {
  // Double-RAF: first RAF enters the rendering pipeline;
  // second RAF fires after the browser completes layout so that
  // getBoundingClientRect reflects the true dimensions for the
  // current viewport — this is the key fix for cross-size consistency.
  requestAnimationFrame(() => {
    requestAnimationFrame(() => {
      const stickyZone = document.querySelector(".sticky-header-zone");
      const bannerContainer = document.querySelector(
        ".portfolio-banner-container",
      );
      const toggleWrapper = document.querySelector(".theme-toggle-wrapper");

      if (!stickyZone || !bannerContainer) return;

      // getBoundingClientRect gives accurate post-layout height at any
      // viewport width, unlike offsetHeight which can lag on resize.
      const bannerHeight = bannerContainer.getBoundingClientRect().height;

      if (bannerHeight <= 0) {
        // Not yet painted — retry shortly
        setTimeout(updateStickyLock, 50);
        return;
      }

      const visibleStrip = bannerHeight * BANNER_SHOW_FRACTION;
      STICKY_LOCK_PX = Math.round(bannerHeight - visibleStrip);

      // A negative `top` on position:sticky means "allow the element to
      // scroll STICKY_LOCK_PX pixels above the viewport before locking".
      // Result: bottom 25% of banner + shelf + tabs stay pinned.
      stickyZone.style.top = `-${STICKY_LOCK_PX}px`;

      // Centre the toggle vertically within the visible banner strip
      if (toggleWrapper) {
        const toggleHeight = toggleWrapper.getBoundingClientRect().height || 36;
        const toggleTop = Math.max(
          4,
          Math.round((visibleStrip - toggleHeight) / 2),
        );
        toggleWrapper.style.top = `${toggleTop}px`;
      }
    });
  });
}

// ── Trigger 1: image load (handles cached AND network-loaded images) ──────────
const _bannerImg = document.querySelector(".portfolio-banner");
if (_bannerImg) {
  if (_bannerImg.complete && _bannerImg.naturalHeight > 0) {
    // Image already decoded from cache — run immediately
    updateStickyLock();
  } else {
    // Wait for the image to finish loading over the network
    _bannerImg.addEventListener("load", updateStickyLock);
  }
}

// ── Trigger 2: window resize — debounced, covers ALL viewport changes ─────────
// Using window resize instead of ResizeObserver on the img element ensures we
// recalculate AFTER the browser has reflowed the image to its new dimensions.
let _resizeTimer;
window.addEventListener(
  "resize",
  () => {
    clearTimeout(_resizeTimer);
    _resizeTimer = setTimeout(() => {
      updateStickyLock();
      if (!birdHasFlown) positionBird(true);
    }, 66); // ~1 frame at 15 fps — responsive without layout thrashing
  },
  { passive: true },
);

// ── Trigger 3: full page load — catches anything the above might miss ─────────
window.addEventListener("load", updateStickyLock);

// ─────────────────────────────────────────────────────────────
// BIRD POSITIONING
// ─────────────────────────────────────────────────────────────
function positionBird(isResize = false) {
  if (birdHasFlown) return;

  const refactorTab = document.querySelector(".tab-button:nth-child(3)");
  const bannerEl = document.querySelector(".portfolio-banner-container");
  if (!refactorTab || !bannerEl) return;

  const tabRect = refactorTab.getBoundingClientRect();
  const bannerRect = bannerEl.getBoundingClientRect();

  const leftPos = tabRect.left + window.scrollX + tabRect.width / 2 + 15;
  const topPos = bannerRect.bottom + window.scrollY - 53;

  bird.dataset.initialLeft = leftPos;
  bird.dataset.initialTop = topPos;

  bird.style.left = leftPos + "px";
  bird.style.top = topPos + "px";
  bird.style.position = "absolute";
  bird.style.opacity = "1";
  bird.classList.add("landed");

  setTimeout(() => {
    bird.classList.remove("landed");
    bird.classList.add("idle");
  }, 500);

  isPositioned = true;
  bird.style.setProperty("--scroll-offset", "0px");
}

function flyBirdBack() {
  if (!birdHasFlown) return;

  bird.classList.remove("idle", "landed");
  bird.classList.add("flying");

  const currentLeft = parseFloat(bird.style.left);
  const currentTop = parseFloat(bird.style.top);

  const refactorTab = document.querySelector(".tab-button:nth-child(3)");
  const bannerEl = document.querySelector(".portfolio-banner-container");
  if (!refactorTab || !bannerEl) return;

  const tabRect = refactorTab.getBoundingClientRect();
  const bannerRect = bannerEl.getBoundingClientRect();
  const targetLeft = tabRect.left + window.scrollX + tabRect.width / 2 + 15;
  const targetTop = bannerRect.bottom + window.scrollY - 53;

  const cpX = (currentLeft + targetLeft) / 2;
  const cpY = Math.min(currentTop, targetTop) - 300;

  const duration = 2500;
  const startTime = performance.now();

  function animateReturn(currentTime) {
    const elapsed = currentTime - startTime;
    const progress = Math.min(elapsed / duration, 1);

    const t = 1 - Math.pow(1 - progress, 3);
    const invT = 1 - t;

    const x =
      invT * invT * currentLeft + 2 * invT * t * cpX + t * t * targetLeft;
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

    if (dy > 0) {
      visualRotation = visualRotation * 0.3;
    }

    if (progress > 0.6) {
      const landingProgress = (progress - 0.6) / 0.4;
      visualRotation = visualRotation * (1 - landingProgress);
    }

    visualRotation = Math.max(-25, Math.min(25, visualRotation));

    bird.style.left = x + "px";
    bird.style.top = y + "px";
    bird.style.transform = `scaleX(${scaleX}) rotate(${visualRotation}deg)`;

    if (progress < 1) {
      requestAnimationFrame(animateReturn);
    } else {
      bird.classList.remove("flying");
      bird.classList.add("landed");

      bird.style.transform = "scaleX(1) rotate(0deg)";
      bird.style.position = "absolute";
      bird.style.left = targetLeft + "px";
      bird.style.top = targetTop + "px";

      birdHasFlown = false;
      isReady = false;

      setTimeout(() => {
        bird.classList.remove("landed");
        bird.classList.add("idle");
      }, 500);

      setTimeout(() => {
        isReady = true;
      }, 1000);
    }
  }

  requestAnimationFrame(animateReturn);
}

setTimeout(positionBird, 100);
setTimeout(positionBird, 500);

const bannerImg = document.querySelector(".portfolio-banner");
if (bannerImg) {
  if (bannerImg.complete) {
    positionBird();
  } else {
    bannerImg.addEventListener("load", () => positionBird());
  }
}

window.addEventListener("load", positionBird);

setTimeout(() => {
  isReady = true;
}, 1000);

window.addEventListener("scroll", function () {
  const homeTab = document.getElementById("home");
  const isHomeActive = homeTab && homeTab.classList.contains("active");

  const flickLogo = document.querySelector(".flick-logo");

  if (!birdHasFlown && isPositioned && isReady && isHomeActive && flickLogo) {
    const rect = flickLogo.getBoundingClientRect();

    if (rect.top < window.innerHeight) {
      birdHasFlown = true;
      bird.style.setProperty("--scroll-offset", "0px");
      bird.classList.remove("landed", "idle");
      bird.classList.add("flying");

      const startLeft = parseFloat(bird.dataset.initialLeft);
      const startTop = parseFloat(bird.dataset.initialTop);

      const flickRect = flickLogo.getBoundingClientRect();
      const endLeft =
        flickRect.left + window.scrollX + flickRect.width / 2 - 30;
      const endTop = flickRect.top + window.scrollY - 36;

      const duration = 2800;
      const startTime = performance.now();

      function animateBird(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);

        let x, y, rotation, scaleX;

        if (progress < 0.15) {
          const flapProgress = progress / 0.15;
          x = startLeft - 20 * flapProgress;
          y = startTop - 80 * flapProgress;

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

          x =
            Math.pow(invT, 3) * p0x +
            3 * Math.pow(invT, 2) * t * p1x +
            3 * invT * Math.pow(t, 2) * p2x +
            Math.pow(t, 3) * p3x;

          y =
            Math.pow(invT, 3) * p0y +
            3 * Math.pow(invT, 2) * t * p1y +
            3 * invT * Math.pow(t, 2) * p2y +
            Math.pow(t, 3) * p3y;

          scaleX = -1;

          if (flightProgress < 0.3) {
            rotation = -20 + 110 * (flightProgress / 0.3);
          } else if (flightProgress < 0.7) {
            const curveP = (flightProgress - 0.3) / 0.4;
            rotation = 90 - 120 * curveP;
          } else {
            const landP = (flightProgress - 0.7) / 0.3;
            rotation = -30 + 30 * landP;
          }
        }

        bird.style.left = x + "px";
        bird.style.top = y + "px";
        bird.style.transform = `scaleX(${scaleX}) rotate(${rotation}deg)`;

        if (progress < 1) {
          requestAnimationFrame(animateBird);
        } else {
          bird.classList.remove("flying");
          bird.classList.add("landed");
          bird.style.position = "absolute";
          bird.style.left = endLeft + "px";
          bird.style.top = endTop + "px";
          bird.style.transform = "scaleX(-1) rotate(0deg)";

          setTimeout(() => {
            bird.classList.remove("landed");
            bird.classList.add("idle");
          }, 500);
        }
      }

      requestAnimationFrame(animateBird);
    }
  }
});

// Project filter functionality
function filterProjects(category, event) {
  const filterButtons = document.querySelectorAll(".filter-btn");
  filterButtons.forEach((btn) => btn.classList.remove("active"));
  event.currentTarget.classList.add("active");

  const projectCards = document.querySelectorAll(".project-card");
  projectCards.forEach((card) => {
    if (category === "all" || card.dataset.category === category) {
      card.style.display = "block";
    } else {
      card.style.display = "none";
    }
  });
}

// ========================================
// PROJECT DETAILS MODAL POPUP
// ========================================

function openProjectModal(projectId) {
  const modal = document.getElementById("project-modal");
  const modalContent = document.getElementById("project-modal-content");
  const detailsElement = document.getElementById(`details-${projectId}`);

  if (!modal || !modalContent || !detailsElement) return;

  modalContent.innerHTML = detailsElement.innerHTML;
  modal.classList.add("show");
  document.body.style.overflow = "hidden";
}

function closeProjectModal() {
  const modal = document.getElementById("project-modal");
  if (!modal) return;
  modal.classList.remove("show");
  document.body.style.overflow = "";
}

const modal = document.getElementById("project-modal");
if (modal) {
  modal.addEventListener("click", function (e) {
    const isInteractive = e.target.closest("a") || e.target.closest("button");
    if (isInteractive) return;
    closeProjectModal();
  });
}

document
  .getElementById("project-modal")
  .addEventListener("click", function (e) {
    if (e.target === this) {
      closeProjectModal();
    }
  });

document.addEventListener("keydown", function (e) {
  if (e.key === "Escape") {
    closeProjectModal();
  }
});

// Lightbox functionality
let currentImageIndex = 0;
let lightboxImages = [];

function initLightbox() {
  const clickableImages = document.querySelectorAll(
    ".screenshot-grid img, .project-image-card img, .image-card img, .buddy-screenshot-grid img, .mario-image, .paradox-image",
  );

  clickableImages.forEach((img, index) => {
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

  lightboxImg.src = clickedImg.src;
  lightboxCaption.textContent = clickedImg.alt || "";
  lightbox.classList.add("active");
  document.body.style.overflow = "hidden";
}

function closeLightbox() {
  const lightbox = document.getElementById("lightbox");
  lightbox.classList.remove("active");
  document.body.style.overflow = "";
}

function changeLightboxImage(direction) {
  currentImageIndex += direction;

  if (currentImageIndex >= lightboxImages.length) {
    currentImageIndex = 0;
  } else if (currentImageIndex < 0) {
    currentImageIndex = lightboxImages.length - 1;
  }

  const lightboxImg = document.getElementById("lightbox-img");
  const lightboxCaption = document.getElementById("lightbox-caption");

  lightboxImg.src = lightboxImages[currentImageIndex].src;
  lightboxCaption.textContent = lightboxImages[currentImageIndex].alt || "";
}

document.getElementById("lightbox").addEventListener("click", function (e) {
  if (e.target === this) {
    closeLightbox();
  }
});

document.addEventListener("keydown", function (e) {
  const lightbox = document.getElementById("lightbox");
  if (lightbox.classList.contains("active")) {
    if (e.key === "Escape") {
      closeLightbox();
    } else if (e.key === "ArrowLeft") {
      changeLightboxImage(-1);
    } else if (e.key === "ArrowRight") {
      changeLightboxImage(1);
    }
  }
});

window.addEventListener("load", initLightbox);
