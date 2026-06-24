const canvas = document.getElementById("starfield");
const ctx = canvas.getContext("2d");

let stars = [];
let shootingStars = [];

const numStars = 90;

function resizeCanvas() {
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
  initStars();
}

function initStars() {
  stars = Array.from({ length: numStars }, () => {
    const layer = Math.random();

    let size;
    let speedMultiplier;

    if (layer < 0.7) {
      // 70% ستاره‌های دور
      size = Math.random() * 0.7 + 0.3;
      speedMultiplier = 0.3;
    } else if (layer < 0.9) {
      // 20% ستاره‌های متوسط
      size = Math.random() * 1 + 0.8;
      speedMultiplier = 0.6;
    } else {
      // 10% ستاره‌های نزدیک
      size = Math.random() * 1.2 + 1.4;
      speedMultiplier = 1;
    }

    return {
      x: Math.random() * canvas.width,
      y: Math.random() * canvas.height,

      // جهت کلی حرکت (خیلی آروم)
      dx: (-0.03 + (Math.random() - 0.5) * 0.08) * speedMultiplier,
      dy: (0.01 + (Math.random() - 0.5) * 0.06) * speedMultiplier,

      size,
      flickerSeed: Math.random() * 1000
    };
  });
}

let lastShoot = 0;

function spawnShootingStar() {
  const now = Date.now();

  if (
    shootingStars.length === 0 &&
    now - lastShoot > 1000 &&
    Math.random() < 0.01
  ) {
    shootingStars.push({
      x: Math.random() * canvas.width,
      y: Math.random() * (canvas.height * 0.6),

      vx: 1.5 + Math.random() * 1.5,
      vy: 0.5 + Math.random() * 1,

      life: 120,
      initialLife: 120
    });

    lastShoot = now;
  }
}

function animate() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  // ⭐ Stars
  stars.forEach((s) => {
    s.x += s.dx;
    s.y += s.dy;

    // wrap around edges
    if (s.x < -10) s.x = canvas.width + 10;
    if (s.x > canvas.width + 10) s.x = -10;

    if (s.y < -10) s.y = canvas.height + 10;
    if (s.y > canvas.height + 10) s.y = -10;

    const flicker =
      0.45 +
      Math.abs(
        Math.sin(Date.now() * 0.0005 + s.flickerSeed)
      ) * 0.25;

    ctx.beginPath();
    ctx.fillStyle = `rgba(255,255,255,${flicker})`;
    ctx.arc(s.x, s.y, s.size, 0, Math.PI * 2);
    ctx.fill();
  });

  // 🌠 Shooting stars
  spawnShootingStar();

  for (let i = shootingStars.length - 1; i >= 0; i--) {
    const s = shootingStars[i];

    const opacity = s.life / s.initialLife;

    const grad = ctx.createLinearGradient(
      s.x,
      s.y,
      s.x - s.vx * 25,
      s.y - s.vy * 25
    );

    grad.addColorStop(0, `rgba(255,255,255,${opacity})`);
    grad.addColorStop(1, "rgba(255,255,255,0)");

    ctx.strokeStyle = grad;
    ctx.lineWidth = 1.5;

    ctx.beginPath();
    ctx.moveTo(s.x, s.y);
    ctx.lineTo(
      s.x - s.vx * 12,
      s.y - s.vy * 12
    );
    ctx.stroke();

    s.x += s.vx;
    s.y += s.vy;
    s.life--;

    if (s.life <= 0) {
      shootingStars.splice(i, 1);
    }
  }

  requestAnimationFrame(animate);
}

window.addEventListener("resize", resizeCanvas);

resizeCanvas();
animate();