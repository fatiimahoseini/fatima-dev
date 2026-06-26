const slider = document.getElementById("slider");
const slides = Array.from(slider.querySelectorAll(".slide"));
const dotsContainer = document.getElementById("dots");

let current = 0;
let autoplayInterval = null;

const total = slides.length;

/* -------------------------
   INIT DOTS
------------------------- */
function createDots() {
    slides.forEach((_, i) => {
        const dot = document.createElement("button");
        dot.className = "w-2.5 h-2.5 rounded-full transition-all";
        dot.addEventListener("click", () => goTo(i));
        dotsContainer.appendChild(dot);
    });
}

/* -------------------------
   UPDATE UI
------------------------- */
function updateUI() {
    slides.forEach((slide, i) => {
        slide.style.opacity = i === current ? "1" : "0";
        slide.style.zIndex = i === current ? "10" : "0";
    });

    [...dotsContainer.children].forEach((dot, i) => {
        dot.classList.toggle("bg-white", i === current);
        dot.classList.toggle("bg-white/40", i !== current);
    });
}

/* -------------------------
   INFINITE LOGIC
------------------------- */
function next() {
    current = (current + 1) % total;
    updateUI();
}

function prev() {
    current = (current - 1 + total) % total;
    updateUI();
}

function goTo(i) {
    current = i;
    updateUI();
    resetAutoplay();
}

/* -------------------------
   AUTOPLAY
------------------------- */
function startAutoplay() {
    autoplayInterval = setInterval(next, 5000);
}

function resetAutoplay() {
    clearInterval(autoplayInterval);
    startAutoplay();
}

/* -------------------------
   DRAG (MOUSE)
------------------------- */
let startX = 0;
let isDragging = false;

slider.addEventListener("mousedown", (e) => {
    startX = e.clientX;
    isDragging = true;
});

slider.addEventListener("mouseup", (e) => {
    if (!isDragging) return;
    isDragging = false;

    let diff = e.clientX - startX;

    if (diff > 50) prev();
    else if (diff < -50) next();
});

/* -------------------------
   SWIPE (TOUCH)
------------------------- */
slider.addEventListener("touchstart", (e) => {
    startX = e.touches[0].clientX;
});

slider.addEventListener("touchend", (e) => {
    let diff = e.changedTouches[0].clientX - startX;

    if (diff > 50) prev();
    else if (diff < -50) next();
});

/* -------------------------
   HOVER PAUSE
------------------------- */
slider.parentElement.addEventListener("mouseenter", () => {
    clearInterval(autoplayInterval);
});

slider.parentElement.addEventListener("mouseleave", () => {
    startAutoplay();
});

/* -------------------------
   INIT
------------------------- */
createDots();
updateUI();
startAutoplay();