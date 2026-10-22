document.addEventListener("DOMContentLoaded", () => {
  const current = window.location.pathname;
  document.querySelectorAll(".nav-links a").forEach(link => {
    const href = link.getAttribute("href") || "";
    if (href !== "/" && current.startsWith(href)) {
      link.setAttribute("aria-current", "page");
    }
  });

  const canvas = document.querySelector(".hero-card canvas");
  if (canvas) {
    const ctx = canvas.getContext("2d");
    if (ctx) {
      const draw = () => {
        const { width, height } = canvas;
        ctx.clearRect(0, 0, width, height);
        ctx.strokeStyle = "rgba(255,255,255,.35)";
        ctx.lineWidth = 1;
        for (let i = 0; i < 8; i++) {
          ctx.beginPath();
          ctx.moveTo(0, i * (height / 8));
          ctx.lineTo(width, i * (height / 8));
          ctx.stroke();
        }
      };
      draw();
    }
  }
});
