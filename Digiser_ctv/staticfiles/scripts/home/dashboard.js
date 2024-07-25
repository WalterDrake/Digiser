function openTab(tabName) {
  var i, tabcontent, tablinks;
  tabcontent = document.getElementsByClassName("tab-content");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }
  tablinks = document.getElementsByClassName("tab-button");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }
  document.getElementById(tabName).style.display = "block";
  document.querySelector(`[onclick="openTab('${tabName}')"]`).className +=
    " active";
}

// Default open tab
document.addEventListener("DOMContentLoaded", (event) => {
  document.getElementById("system").style.display = "block";
});

document
  .getElementById("detail-standard-project")
  .addEventListener("click", function () {
    window.location.href = "{% url 'data_statistic' %}";
  });

// Function to format tooltip content
function tooltipItemCallback(context) {
  const total = context.dataset.data.reduce((acc, curr) => acc + curr, 0);
  const percentage = ((context.raw / total) * 100).toFixed(1) + "%";
  return percentage;
}

new Chart(document.getElementById("analysis_chart"), {
  type: "doughnut",
  data: {
    labels: ["Completed", "Development", "Live"],
    datasets: [
      {
        label: "Work",
        data: [300, 50, 100],
        backgroundColor: [
          "rgb(255, 99, 132)",
          "rgb(54, 162, 235)",
          "rgb(255, 205, 86)",
        ],
        hoverOffset: 16,
        borderRadius: 12,
        spacing: 8,
      },
    ],
  },
  options: {
    aspectRatio: 1.6,
    plugins: {
      legend: {
        display: true,
        labels: {
          usePointStyle: true,
          pointStyle: "circle",
        },
      },
      tooltip: {
        usePointStyle: true,
        callbacks: {
          label: function (context) {
            const label = context.label || "";
            const value = context.raw;
            const percentage = tooltipItemCallback(context);
            return `${label}: ${value} (${percentage})`;
          },
        },
      },
    },
  },
});

new Chart(document.getElementById("progression_chart"), {
  type: "scatter",
  data: {
    labels: ["Q1", "Q2", "Q3", "Q4", "Q5"],
    datasets: [
      {
        type: "bar",
        label: "Bar Dataset",
        data: [10, 20, 30, 40, 10],
        borderColor: "rgb(255, 99, 132)",
        backgroundColor: "rgba(255, 99, 132)",
        borderRadius: 10,
        order: 2,
      },
      {
        type: "line",
        label: "Line Dataset",
        data: [30, 35, 59, 50, 10],
        fill: false,
        borderColor: "rgb(54, 162, 235)",
        borderCapStyle: "round",
        borderJoinStyle: "round",
        tension: 0.1,
        order: 1,
      },
    ],
  },
  options: {
    aspectRatio: 1.6,
    scales: {
      y: {
        beginAtZero: true,
      },
    },
    elements: {
      line: {
        borderWidth: 2,
      },
      point: {
        radius: 2,
      },
      bar: {
        borderWidth: 2,
      },
    },
    plugins: {
      legend: {
        display: true,
        labels: {
          usePointStyle: true,
          pointStyle: "triangle",
        },
      },
      tooltip: {
        usePointStyle: true,
      },
    },
  },
});
