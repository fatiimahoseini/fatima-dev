(function () {
  const article = document.querySelector(".article-content");
  const toc = document.getElementById("toc");
  if (!article || !toc) return;

  const headings = article.querySelectorAll("h2, h3");

  headings.forEach((h, i) => {
    const id = "heading-" + i;
    h.id = id;
    const isH3 = h.tagName === "H3";

    const li = document.createElement("li");
    li.className = "relative pl-6 min-w-0";
    li.innerHTML =
      '<span class="toc-dot absolute left-0 top-1/2 -translate-y-1/2 w-[11px] h-[11px] rounded-full bg-blue-500 transition-opacity"></span>' +
      '<a href="#' +
      id +
      '" class="toc-link block w-full whitespace-normal break-words text-muted hover:text-foreground transition-colors ' +
      (isH3 ? "text-sm" : "") +
      '">' +
      h.textContent.trim() +
      "</a>";
    toc.appendChild(li);
  });

  if (headings.length === 0) return;

  function updateToc() {
    let current = 0;
    headings.forEach((h, i) => {
      if (h.getBoundingClientRect().top <= 120) current = i;
    });

    toc.querySelectorAll("li").forEach((li, i) => {
      const dot = li.querySelector(".toc-dot");
      const link = li.querySelector(".toc-link");
      if (i === current) {
        dot.classList.remove("opacity-0");
        link.classList.add("text-blue-400", "font-medium");
        link.classList.remove("text-muted");
      } else {
        dot.classList.add("opacity-0");
        link.classList.remove("text-blue-400", "font-medium");
        link.classList.add("text-muted");
      }
    });
  }

  window.addEventListener("scroll", updateToc, { passive: true });
  updateToc();
})();
