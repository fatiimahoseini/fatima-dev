function drawFavicon() {
  const canvas = document.createElement("canvas");
  canvas.width = 64;
  canvas.height = 64;

  const ctx = canvas.getContext("2d");

  ctx.clearRect(0, 0, 64, 64);

  // Blue circle
  ctx.fillStyle = "#3984F5";
  ctx.beginPath();
  ctx.arc(32, 32, 14, 0, Math.PI * 2);
  ctx.fill();

  document.getElementById("favicon").href = canvas.toDataURL("image/png");
}

drawFavicon();
