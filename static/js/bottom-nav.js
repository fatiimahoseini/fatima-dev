(function () {
  const desktopNav = document.getElementById("bottom-nav-desktop");
  if (!desktopNav) return;

  function getThreshold() {
    const hero = document.getElementById("hero");
    if (hero) return Math.max(150, hero.offsetHeight - 120);
    return 300;
  }

  function check() {
    const threshold = getThreshold();
    if (window.scrollY > threshold) {
      desktopNav.classList.add("opacity-100");
      desktopNav.classList.remove("opacity-0", "pointer-events-none");
    } else {
      desktopNav.classList.add("opacity-0", "pointer-events-none");
      desktopNav.classList.remove("opacity-100");
    }
  }

  window.addEventListener("scroll", check, { passive: true });
  window.addEventListener("resize", check);
  check();
})();
