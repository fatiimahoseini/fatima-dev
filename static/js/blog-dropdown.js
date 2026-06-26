const sortBtn = document.getElementById("sortBtn");
const sortMenu = document.getElementById("sortMenu");
const sortSelected = document.getElementById("sortSelected");

sortBtn.addEventListener("click", () => {
    sortMenu.classList.toggle("hidden");
});

document.querySelectorAll(".sort-option").forEach(option => {
    option.addEventListener("click", () => {
        sortSelected.textContent = option.textContent;
        sortMenu.classList.add("hidden");
    });
});

document.addEventListener("click", (e) => {
    if (!sortBtn.contains(e.target) && !sortMenu.contains(e.target)) {
        sortMenu.classList.add("hidden");
    }
});