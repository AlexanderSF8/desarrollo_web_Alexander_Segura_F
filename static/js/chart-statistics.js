document.addEventListener('DOMContentLoaded', function() {
    
    // --- MEMBERS PER DAY (Line Chart) ---
    fetch('/api/stats/members-per-day')
        .then(response => response.json())
        .then(data => {
            // data = [{fecha: '2026-06-08', cantidad: 2}, ...]
            const fechas = data.map(item => item.fecha);
            const cantidades = data.map(item => item.cantidad);

            const ctx1 = document.getElementById('membersChart').getContext('2d');
            new Chart(ctx1, {
                type: 'line',
                data: {
                    labels: fechas,
                    datasets: [{
                        label: 'Nuevos Miembros',
                        data: cantidades,
                        borderColor: '#0d75fd', 
                        backgroundColor: 'rgba(13, 110, 253, 0.2)',
                        borderWidth: 2,
                        fill: true,
                        tension: 0.3 // Hace que la línea sea curva y elegante
                    }]
                },
                options: { responsive: true }
            });
        });

    // --- ACTIVITIES BY TYPE (Pie Chart) ---
    fetch('/api/stats/activities-by-type')
        .then(response => response.json())
        .then(data => {
            const tipos = data.map(item => item.tipo);
            const cantidades = data.map(item => item.cantidad);

            const ctx2 = document.getElementById('activitiesTypeChart').getContext('2d');
            new Chart(ctx2, {
                type: 'pie', // o 'doughnut' si quieres el centro vacío
                data: {
                    labels: tipos,
                    datasets: [{
                        data: cantidades,
                        backgroundColor: [
                            '#198754', '#dc3545', '#ffc107', '#0dcaf0', '#6610f2', '#fd7e14'
                        ]
                    }]
                },
                options: { 
                    responsive: true,
                    maintainAspectRatio: false 
                }
            });
        });

    // --- ACTIVITIES BY COMMUNE (Bar Chart) ---
    fetch('/api/stats/activities-by-commune')
        .then(response => response.json())
        .then(data => {
            const comunas = data.map(item => item.comuna);
            const cantidades = data.map(item => item.cantidad);

            const ctx3 = document.getElementById('activitiesCommuneChart').getContext('2d');
            new Chart(ctx3, {
                type: 'bar',
                data: {
                    labels: comunas,
                    datasets: [{
                        label: 'Total Actividades',
                        data: cantidades,
                        backgroundColor: '#0dcaf0',
                        borderColor: '#0abcce',
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        y: { beginAtZero: true, ticks: { stepSize: 1 } }
                    }
                }
            });
        });
        
});
