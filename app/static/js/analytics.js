async function loadChart() {
  const canvas = document.getElementById("skills-chart");
  if (!canvas || typeof Chart === "undefined") return;

  const res = await fetch("/api/analytics/chart");
  const data = await res.json();

  new Chart(canvas, {
    type: "bar",
    data: {
      labels: data.labels,
      datasets: [{
        label: "Score",
        data: data.scores,
        borderRadius: 8,
        backgroundColor: "rgba(91, 124, 250, 0.7)",
        borderColor: "rgba(34, 211, 166, 0.9)",
        borderWidth: 1,
      }],
    },
    options: {
      responsive: true,
      plugins: { legend: { display: false } },
      scales: {
        y: {
          beginAtZero: true,
          grid: { color: "rgba(255,255,255,0.06)" },
          ticks: { color: "#9aa8c7" },
        },
        x: {
          grid: { display: false },
          ticks: { color: "#9aa8c7" },
        },
      },
    },
  });
}

loadChart();