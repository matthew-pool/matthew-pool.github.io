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

// Bird animation variables
let birdHasFlown = false;
let birdOnFlick = false;
let isPositioned = false;
let isReady = false;
let _flightRafId = null;

const bird = document.getElementById("bird");
const birdTooltip = document.getElementById("bird-tooltip");

// ─────────────────────────────────────────────────────────────
// CANCEL any in-progress flight animation
// ─────────────────────────────────────────────────────────────
function cancelFlight() {
  if (_flightRafId !== null) {
    cancelAnimationFrame(_flightRafId);
    _flightRafId = null;
  }
  bird.classList.remove("flying", "landed");
  bird.classList.add("idle");
  bird.style.transform = "scaleX(1) rotate(0deg)";
}

// ─────────────────────────────────────────────────────────────
// TOOLTIP HELPERS
//
// position:fixed is set directly in JS here so it can never be
// overridden by a competing CSS rule (e.g. the original styles.css
// .bird-tooltip rule which has position:absolute). This guarantees
// the bubble stays anchored to the viewport and never scrolls.
// ─────────────────────────────────────────────────────────────
function positionTooltip() {
  if (!birdTooltip || !bird) return;

  // Enforce fixed positioning in JS — beats any CSS specificity
  birdTooltip.style.position = "fixed";

  const birdRect = bird.getBoundingClientRect();
  birdTooltip.style.top = Math.max(4, birdRect.top - 44) + "px";
  birdTooltip.style.bottom = "auto";

  if (birdOnFlick) {
    birdTooltip.style.left = birdRect.left + "px";
    birdTooltip.style.right = "auto";
    birdTooltip.classList.add("flipped");
  } else {
    birdTooltip.style.right = window.innerWidth - birdRect.right + "px";
    birdTooltip.style.left = "auto";
    birdTooltip.classList.remove("flipped");
  }
}

function showBirdTooltip() {
  if (!birdTooltip || bird.classList.contains("flying")) return;
  positionTooltip();
  birdTooltip.classList.add("visible");
}

function hideBirdTooltip() {
  if (!birdTooltip) return;
  birdTooltip.classList.remove("visible");
}

// Keep tooltip locked to bird's viewport position while scrolling.
// position:fixed can be broken by CSS transforms on ancestor elements
// (e.g. the sticky header). Repositioning on every scroll frame is
// the only fully reliable solution.
window.addEventListener(
  "scroll",
  () => {
    if (birdTooltip && birdTooltip.classList.contains("visible")) {
      positionTooltip();
    }
  },
  { passive: true },
);

// ─────────────────────────────────────────────────────────────
// PAGE LOAD
// ─────────────────────────────────────────────────────────────
window.addEventListener("load", function () {
  if (birdTooltip) document.body.appendChild(birdTooltip);
  document.body.appendChild(bird);

  birdHasFlown = false;
  birdOnFlick = false;
  isPositioned = false;
  isReady = false;

  bird.classList.remove("flying", "idle", "landed");
  positionBird();

  setTimeout(() => {
    isReady = true;
  }, 1000);

  if (birdTooltip) {
    setTimeout(() => {
      showBirdTooltip();
      setTimeout(hideBirdTooltip, 2500);
    }, 1800);

    setInterval(() => {
      if (bird.classList.contains("flying")) return;
      showBirdTooltip();
      setTimeout(hideBirdTooltip, 2500);
    }, 7000);
  }
});

// ─────────────────────────────────────────────────────────────
// DARK MODE TOGGLE
// ─────────────────────────────────────────────────────────────
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

themeToggle.addEventListener("click", () => {
  document.body.classList.toggle("dark-mode");
  localStorage.setItem(
    "theme",
    document.body.classList.contains("dark-mode") ? "dark" : "light",
  );
  updateResumeLabel();

  setTimeout(() => {
    if (!birdHasFlown) positionBird();
  }, 350);
});

// ─────────────────────────────────────────────────────────────
// TAB SWITCHING
// ─────────────────────────────────────────────────────────────
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

// ─────────────────────────────────────────────────────────────
// STICKY LOCK + TOGGLE ALIGNMENT
// ─────────────────────────────────────────────────────────────
const BANNER_SHOW_FRACTION = 0.12;
let STICKY_LOCK_PX = 170;

function updateStickyLock() {
  requestAnimationFrame(() => {
    requestAnimationFrame(() => {
      const stickyZone = document.querySelector(".sticky-header-zone");
      const bannerContainer = document.querySelector(
        ".portfolio-banner-container",
      );
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
        const toggleTop = Math.max(
          4,
          Math.round((visibleStrip - toggleHeight) / 2),
        );
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

// ─────────────────────────────────────────────────────────────
// RESIZE — cancel flight, reset state, snap bird to shelf
// ─────────────────────────────────────────────────────────────
let _resizeTimer;
window.addEventListener(
  "resize",
  () => {
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
          setTimeout(() => {
            isReady = true;
          }, 500);
        });
      });
    }, 150);
  },
  { passive: true },
);

window.addEventListener("load", updateStickyLock);

// ─────────────────────────────────────────────────────────────
// BIRD POSITIONING
// ─────────────────────────────────────────────────────────────
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

function positionBird(force = false) {
  if (birdHasFlown && !force) return;

  const coords = getBirdDocCoords();
  if (!coords) return;

  bird.classList.remove("flying", "idle", "landed");
  bird.style.transform = "scaleX(1) rotate(0deg)";
  bird.style.position = "absolute";
  bird.style.left = coords.left + "px";
  bird.style.top = coords.top + "px";
  bird.style.opacity = "1";
  bird.classList.add("landed");

  setTimeout(() => {
    bird.classList.remove("landed");
    bird.classList.add("idle");
  }, 500);

  isPositioned = true;
}

// ─────────────────────────────────────────────────────────────
// RETURN FLIGHT
// ─────────────────────────────────────────────────────────────
function flyBirdBack() {
  if (!birdHasFlown) return;

  hideBirdTooltip();
  birdOnFlick = false;

  bird.classList.remove("idle", "landed");
  bird.classList.add("flying");

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

  _flightRafId = requestAnimationFrame(animateReturn);
}

// ─────────────────────────────────────────────────────────────
// INITIAL POSITIONING
// ─────────────────────────────────────────────────────────────
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

// ─────────────────────────────────────────────────────────────
// OUTBOUND FLIGHT TRIGGER
// ─────────────────────────────────────────────────────────────
window.addEventListener(
  "scroll",
  function () {
    const homeTab = document.getElementById("home");
    const isHomeActive = homeTab && homeTab.classList.contains("active");
    const flickLogo = document.querySelector(".flick-logo");

    if (!birdHasFlown && isPositioned && isReady && isHomeActive && flickLogo) {
      if (window.scrollY >= STICKY_LOCK_PX) {
        birdHasFlown = true;
        hideBirdTooltip();

        bird.classList.remove("landed", "idle");
        bird.classList.add("flying");

        const startLeft = parseFloat(bird.style.left);
        const startTop = parseFloat(bird.style.top);

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
            const fp = progress / 0.15;
            x = startLeft - 20 * fp;
            y = startTop - 80 * fp;
            scaleX = fp < 0.2 ? 1 : -1;
            rotation = -20 * fp;
          } else {
            const fp2 = (progress - 0.15) / 0.85;

            const p0x = startLeft - 20,
              p0y = startTop - 80;
            const p3x = endLeft,
              p3y = endTop;
            const p1x = startLeft - 50,
              p1y = startTop + 500;
            const p2x = endLeft - 100,
              p2y = endTop - 80;

            const t = fp2,
              invT = 1 - t;
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
      }
    }
  },
  { passive: true },
);

// ========================================
// PROJECT FILTER
// ========================================
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
    if (e.target.closest("a") || e.target.closest("button")) return;
    closeProjectModal();
  });
}

document
  .getElementById("project-modal")
  .addEventListener("click", function (e) {
    if (e.target === this) closeProjectModal();
  });

document.addEventListener("keydown", function (e) {
  if (e.key === "Escape") closeProjectModal();
});

// ========================================
// LIGHTBOX
// ========================================
let currentImageIndex = 0;
let lightboxImages = [];

function initLightbox() {
  const clickableImages = document.querySelectorAll(
    ".screenshot-grid img, .project-image-card img, .image-card img, .buddy-screenshot-grid img, .mario-image, .paradox-image",
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

  lightboxImg.src = clickedImg.src;
  lightboxCaption.textContent = clickedImg.alt || "";
  lightbox.classList.add("active");
  document.body.style.overflow = "hidden";
}

function closeLightbox() {
  document.getElementById("lightbox").classList.remove("active");
  document.body.style.overflow = "";
}

function changeLightboxImage(direction) {
  currentImageIndex =
    (currentImageIndex + direction + lightboxImages.length) %
    lightboxImages.length;

  document.getElementById("lightbox-img").src =
    lightboxImages[currentImageIndex].src;
  document.getElementById("lightbox-caption").textContent =
    lightboxImages[currentImageIndex].alt || "";
}

document.getElementById("lightbox").addEventListener("click", function (e) {
  if (e.target === this) closeLightbox();
});

document.addEventListener("keydown", function (e) {
  if (!document.getElementById("lightbox").classList.contains("active")) return;
  if (e.key === "Escape") closeLightbox();
  else if (e.key === "ArrowLeft") changeLightboxImage(-1);
  else if (e.key === "ArrowRight") changeLightboxImage(1);
});

window.addEventListener("load", initLightbox);
