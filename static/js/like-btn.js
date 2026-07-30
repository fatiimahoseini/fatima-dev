document.querySelectorAll(".like-btn").forEach((btn) => {
  btn.addEventListener("click", (e) => {
    e.preventDefault();
    e.stopPropagation();

    const liked = btn.dataset.liked === "true";
    const svg = btn.querySelector("svg");

    btn.dataset.liked = liked ? "false" : "true";
    svg.setAttribute("fill", liked ? "none" : "currentColor");
    btn.classList.toggle("text-pink-400", !liked);
    btn.classList.toggle("text-muted", liked);

    if (!liked) {
      const heart = document.createElement("span");
      heart.innerHTML = "&#10084;";
      heart.className = "flying-heart";
      btn.appendChild(heart);
      heart.addEventListener("animationend", () => heart.remove());
    }
  });
});
