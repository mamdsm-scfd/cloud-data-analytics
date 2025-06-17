document.getElementById('uploadForm').addEventListener('submit', async (e) => {
  e.preventDefault();

  const fileInput = document.getElementById('csvFile');
  const formData = new FormData();
  formData.append('file', fileInput.files[0]);

  const response = await fetch('https://Mohammed040.pythonanywhere.com/upload', {
    method: 'POST',
    body: formData
  });

  const result = await response.json();
  document.getElementById('result').innerText = JSON.stringify(result, null, 2);

  drawChart(result.analysis);
});

function drawChart(data) {
  const labels = [];
  const means = [];
  const medians = [];
  const modes = [];

  for (const col in data) {
    labels.push(col);
    means.push(data[col].mean);
    medians.push(data[col].median);
    modes.push(data[col].mode);
  }

  const ctx = document.getElementById('chartCanvas').getContext('2d');

  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [
        {
          label: 'Mean',
          data: means,
          backgroundColor: 'rgba(75, 192, 192, 0.6)',
        },
        {
          label: 'Median',
          data: medians,
          backgroundColor: 'rgba(153, 102, 255, 0.6)',
        },
        {
          label: 'Mode',
          data: modes,
          backgroundColor: 'rgba(255, 159, 64, 0.6)',
        }
      ]
    },
    options: {
      responsive: true,
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  });
}
