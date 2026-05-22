document.querySelectorAll(".vacancy-card").forEach((card, index) => {
  card.style.animationDelay = `${index * 60}ms`;
  card.classList.add("fade-in");
});