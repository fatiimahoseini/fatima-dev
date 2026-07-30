(function() {
    const slider = document.getElementById("blogSlider");
    const track = document.getElementById("blogTrack");
    const prevBtn = document.getElementById("blogPrev");
    const nextBtn = document.getElementById("blogNext");
    const dotsContainer = document.getElementById("blogDots");
    if (!slider || !track) return;

    const slides = track.querySelectorAll(".blog-slide");
    const total = slides.length;
    let perView = window.innerWidth < 768 ? 1 : 3;
    let page = 0;
    let totalPages = Math.ceil(total / perView);
    let autoplayTimer = null;
    let touchStartX = 0;
    let touchDeltaX = 0;
    const SWIPE_THRESHOLD = 50;
    const AUTOPLAY_MS = 5000;

    function getGap() {
        return parseFloat(window.getComputedStyle(track).columnGap || window.getComputedStyle(track).gap || "0");
    }

    function setSlideWidths() {
        const gap = getGap();
        const sliderWidth = slider.clientWidth;
        const slideWidth = perView === 1
            ? sliderWidth
            : (sliderWidth - gap * (perView - 1)) / perView;

        slides.forEach((slide) => {
            slide.style.width = slideWidth + "px";
        });

        return { gap, slideWidth };
    }

    function rebuildDots() {
        if (!dotsContainer) return;
        dotsContainer.innerHTML = "";
        for (let i = 0; i < totalPages; i++) {
            const dot = document.createElement("button");
            dot.className = "w-2 h-2 rounded-full transition " + (i === page ? "bg-sky-400" : "bg-muted");
            dot.addEventListener("click", () => {
                goTo(i);
                restartAutoplay();
            });
            dotsContainer.appendChild(dot);
        }
    }

    rebuildDots();

    function update() {
        const { gap, slideWidth } = setSlideWidths();
        const offset = page * (slideWidth + gap) * perView;
        track.style.transform = "translateX(-" + offset + "px)";

        if (dotsContainer) {
            dotsContainer.querySelectorAll("button").forEach((d, i) => {
                d.className = "w-2 h-2 rounded-full transition " + (i === page ? "bg-sky-400" : "bg-muted");
            });
        }
        if (prevBtn) prevBtn.style.opacity = page === 0 ? "0.3" : "1";
        if (nextBtn) nextBtn.style.opacity = page >= totalPages - 1 ? "0.3" : "1";
    }

    function goTo(p) {
        page = Math.max(0, Math.min(p, totalPages - 1));
        update();
    }

    function nextPage() {
        if (totalPages <= 1) return;
        page = (page + 1) % totalPages;
        update();
    }

    function stopAutoplay() {
        if (!autoplayTimer) return;
        window.clearInterval(autoplayTimer);
        autoplayTimer = null;
    }

    function startAutoplay() {
        stopAutoplay();
        if (totalPages > 1) {
            autoplayTimer = window.setInterval(nextPage, AUTOPLAY_MS);
        }
    }

    function restartAutoplay() {
        stopAutoplay();
        startAutoplay();
    }

    if (prevBtn) prevBtn.addEventListener("click", () => {
        goTo(page - 1);
        restartAutoplay();
    });

    if (nextBtn) nextBtn.addEventListener("click", () => {
        goTo(page + 1);
        restartAutoplay();
    });

    track.addEventListener("touchstart", (e) => {
        touchStartX = e.touches[0].clientX;
        touchDeltaX = 0;
        stopAutoplay();
    }, { passive: true });

    track.addEventListener("touchmove", (e) => {
        touchDeltaX = e.touches[0].clientX - touchStartX;
    }, { passive: true });

    track.addEventListener("touchend", () => {
        if (Math.abs(touchDeltaX) > SWIPE_THRESHOLD) {
            if (touchDeltaX < 0) goTo(page + 1);
            if (touchDeltaX > 0) goTo(page - 1);
        }
        restartAutoplay();
    });

    track.addEventListener("mouseenter", stopAutoplay);
    track.addEventListener("mouseleave", startAutoplay);

    window.addEventListener("resize", () => {
        perView = window.innerWidth < 768 ? 1 : 3;
        totalPages = Math.ceil(total / perView);
        rebuildDots();
        goTo(Math.min(page, totalPages - 1));
        restartAutoplay();
    });

    update();
    startAutoplay();
})();
