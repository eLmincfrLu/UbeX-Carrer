document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".flash").forEach((el) => {
    setTimeout(() => {
      el.style.opacity = "0";
      el.style.transform = "translateY(-4px)";
      setTimeout(() => el.remove(), 300);
    }, 4500);
  });
});