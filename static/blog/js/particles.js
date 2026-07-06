(function () {
    const canvas = document.getElementById("particleCanvas");
    if (!canvas) return;

    const ctx = canvas.getContext("2d");
    let particles = [];
    let w, h;
    let opacity = 1;
    let targetOpacity = 1;

    // Config from data attributes
    const density = parseInt(canvas.dataset.density) || 12000;
    const fadeScroll = canvas.dataset.fadeScroll === "true";
    const zoneSelector = canvas.dataset.zone || null;
    const focus = canvas.dataset.focus || null; // "top-right", "top-left", etc.
    let zoneRect = null;

    function resize() {
        w = canvas.width = window.innerWidth;
        h = canvas.height = window.innerHeight;
        if (zoneSelector) updateZone();
    }

    function updateZone() {
        const el = document.querySelector(zoneSelector);
        if (el) {
            const r = el.getBoundingClientRect();
            zoneRect = {
                x: r.left - 40,
                y: r.top - 40,
                w: r.width + 80,
                h: r.height + 80,
            };
        }
    }

    function isInZone(x, y) {
        if (!zoneRect) return false;
        return (
            x > zoneRect.x &&
            x < zoneRect.x + zoneRect.w &&
            y > zoneRect.y &&
            y < zoneRect.y + zoneRect.h
        );
    }

    // Bias random position toward a focus area
    function biasedPos() {
        if (!focus) return { x: Math.random() * w, y: Math.random() * h };

        // 60% of particles near focus, 40% spread across page
        if (Math.random() < 0.6) {
            let x, y;
            if (focus === "top-right") {
                x = w * 0.5 + Math.random() * w * 0.5;
                y = Math.random() * h * 0.5;
            } else if (focus === "top-left") {
                x = Math.random() * w * 0.5;
                y = Math.random() * h * 0.5;
            } else if (focus === "bottom-right") {
                x = w * 0.5 + Math.random() * w * 0.5;
                y = h * 0.5 + Math.random() * h * 0.5;
            } else {
                x = Math.random() * w * 0.5;
                y = h * 0.5 + Math.random() * h * 0.5;
            }
            return { x, y };
        }
        return { x: Math.random() * w, y: Math.random() * h };
    }

    function createParticles() {
        particles = [];
        const count = Math.floor((w * h) / density);
        for (let i = 0; i < count; i++) {
            const pos = biasedPos();
            const p = {
                x: pos.x,
                y: pos.y,
                vx: (Math.random() - 0.5) * 0.4,
                vy: (Math.random() - 0.5) * 0.4,
                r: Math.random() * 2 + 0.8,
                pulse: Math.random() * Math.PI * 2,
            };
            if (zoneSelector && isInZone(p.x, p.y)) {
                p.x = Math.random() < 0.5 ? zoneRect.x - 20 : zoneRect.x + zoneRect.w + 20;
                p.y = Math.random() * h;
            }
            particles.push(p);
        }
    }

    function draw() {
        // Scroll fade — fade when leaving the hero section
        if (fadeScroll) {
            const scrollY = window.scrollY;
            const heroEl = document.querySelector("section.max-w-5xl");
            const heroBottom = heroEl ? heroEl.offsetTop + heroEl.offsetHeight : window.innerHeight;
            const fadeRange = heroBottom * 0.5;
            const progress = Math.max(0, (scrollY - fadeRange) / (heroBottom - fadeRange));
            const minOpacity = zoneSelector ? 0 : 0.1;
            targetOpacity = Math.max(minOpacity, 1 - Math.min(progress, 1) * 0.85);
        }

        opacity += (targetOpacity - opacity) * 0.05;

        ctx.clearRect(0, 0, w, h);
        ctx.globalAlpha = opacity;

        for (let i = 0; i < particles.length; i++) {
            const p = particles[i];
            p.x += p.vx;
            p.y += p.vy;
            p.pulse += 0.02;

            if (p.x < 0) p.x = w;
            if (p.x > w) p.x = 0;
            if (p.y < 0) p.y = h;
            if (p.y > h) p.y = 0;

            if (zoneSelector && isInZone(p.x, p.y)) continue;

            const glow = 0.3 + Math.sin(p.pulse) * 0.15;

            // Glow halo
            ctx.beginPath();
            ctx.arc(p.x, p.y, p.r * 3, 0, Math.PI * 2);
            ctx.fillStyle = "rgba(100, 180, 255, " + (glow * 0.08) + ")";
            ctx.fill();

            // Core dot
            ctx.beginPath();
            ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
            ctx.fillStyle = "rgba(140, 200, 255, " + glow + ")";
            ctx.fill();

            // Connections
            for (let j = i + 1; j < particles.length; j++) {
                const p2 = particles[j];
                if (zoneSelector && isInZone(p2.x, p2.y)) continue;
                const dx = p.x - p2.x;
                const dy = p.y - p2.y;
                const dist = Math.sqrt(dx * dx + dy * dy);

                if (dist < 150) {
                    const alpha = 0.12 * (1 - dist / 150);
                    ctx.beginPath();
                    ctx.moveTo(p.x, p.y);
                    ctx.lineTo(p2.x, p2.y);
                    ctx.strokeStyle = "rgba(120, 180, 255, " + alpha + ")";
                    ctx.lineWidth = 0.6;
                    ctx.stroke();
                }
            }
        }

        ctx.globalAlpha = 1;
        requestAnimationFrame(draw);
    }

    resize();
    createParticles();
    draw();

    window.addEventListener("resize", () => {
        resize();
        createParticles();
    });

    if (zoneSelector) {
        window.addEventListener("scroll", updateZone, { passive: true });
    }
})();
