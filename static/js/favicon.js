const frames = ["•", " "];
let i = 0;

function drawFavicon() {
    const canvas = document.createElement("canvas");
    canvas.width = 64;
    canvas.height = 64;

    const ctx = canvas.getContext("2d");

    ctx.clearRect(0, 0, 64, 64);

    ctx.fillStyle = "#38bdf8";
    ctx.font = "bold 48px monospace";
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";

    const text = frames[i];

    ctx.fillText(text, 32, 34);

    document.getElementById("favicon").href = canvas.toDataURL("image/png");

    i = (i + 1) % frames.length;
}

setInterval(drawFavicon, 300);
drawFavicon();