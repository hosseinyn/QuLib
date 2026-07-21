const ctx = document.getElementById("studentsFav").getContext("2d");

document.fonts.ready.then(() => {
  new Chart(ctx, {
    type: "bar",
    data: {
      labels: [
        "یادگیری تعاملی و سرگرم‌کننده",
        "یادگیری هماهنگ با کلاس",
        "یادگیری خام از اینترنت",
        "یادگیری خام از کتاب درسی",
      ],
      datasets: [
        {
          label: "درصد علاقه دانش‌آموزان",
          data: [60, 20, 10, 10],
          backgroundColor: [
            "rgba(59, 130, 246, 0.7)",
            "rgba(16, 185, 129, 0.7)",
            "rgba(234, 179, 8, 0.7)",
            "rgba(239, 68, 68, 0.7)",
          ],
          borderWidth: 1,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      font: {
        family: "tanha, Tahoma, Arial, sans-serif",
        size: 13,
      },

      scales: {
        x: {
            ticks: {
                font: { family: "tanha" },
                maxRotation: 0,
                minRotation: 0,
                autoSkip: false,
                callback: function(value, index, ticks) {
                const label = this.getLabelForValue(index);
                const maxChars = 10;
                const words = label.split(" ");
                let lines = [];
                let line = "";
                words.forEach(word => {
                    if ((line + word).length > maxChars) {
                    lines.push(line.trim());
                    line = word + " ";
                    } else {
                    line += word + " ";
                    }
                });
                lines.push(line.trim());
                return lines;
                }
            }
            },

        y: {
          beginAtZero: true,
          max: 100,
          ticks: {
            font: {
              family: "tanha",
            },
            callback: (value) => value + "%",
          },
        },
      },

      plugins: {
        legend: {
          labels: {
            font: {
              family: "tanha",
              size: 14,
            },
          },
        },
        tooltip: {
          titleFont: {
            family: "tanha",
          },
          bodyFont: {
            family: "tanha",
          },
          callbacks: {
            label: (context) => context.raw + "%",
          },
        },
      },
    },
  });
});