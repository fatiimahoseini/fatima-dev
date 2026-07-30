(function () {
  const STORAGE_KEY = "theme";
  const root = document.documentElement;
  const toggle = document.getElementById("theme-toggle");
  const sunIcon = document.getElementById("theme-icon-sun");
  const moonIcon = document.getElementById("theme-icon-moon");

  function isDark() {
    return root.classList.contains("dark");
  }

  function updateIcons() {
    if (!sunIcon || !moonIcon) return;

    if (isDark()) {
      sunIcon.classList.remove("hidden");
      moonIcon.classList.add("hidden");
      if (toggle) toggle.setAttribute("aria-label", "Switch to light mode");
    } else {
      sunIcon.classList.add("hidden");
      moonIcon.classList.remove("hidden");
      if (toggle) toggle.setAttribute("aria-label", "Switch to dark mode");
    }
  }

  function setTheme(theme) {
    if (theme === "light") {
      root.classList.remove("dark");
      localStorage.setItem(STORAGE_KEY, "light");
    } else {
      root.classList.add("dark");
      localStorage.setItem(STORAGE_KEY, "dark");
    }
    updateIcons();
  }

  if (toggle) {
    toggle.addEventListener("click", function () {
      setTheme(isDark() ? "light" : "dark");
    });
  }

  updateIcons();
})();
