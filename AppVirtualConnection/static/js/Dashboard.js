function openModal() {
    document.getElementById("myModal").style.display = "block";
}

function closeModal() {
    document.getElementById("myModal").style.display = "none";
}

function crearGrafico() {
    var chartType = document.getElementById('chartType').value;
    var chartLabel = document.getElementById('chartLabel').value;
    var chartLabels = document.getElementById('chartLabels').value.split(',');
    var chartData = document.getElementById('chartData').value.split(',').map(Number);

    var ctx = document.getElementById('myChart').getContext('2d');
    var myChart = new Chart(ctx, {
        type: chartType,
        data: {
            labels: chartLabels,
            datasets: [{
                label: chartLabel,
                data: chartData,
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });

    closeModal(); // Cierra el modal después de crear el gráfico
}