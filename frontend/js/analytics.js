document.addEventListener('DOMContentLoaded', initCharts);

async function initCharts() {
    const data = await apiCall('/analytics');
    if (!data) return;
    
    // Revenue Chart
    const revCtx = document.getElementById('revenueChart').getContext('2d');
    new Chart(revCtx, {
        type: 'line',
        data: {
            labels: data.revenueTrend.labels,
            datasets: [{
                label: 'Revenue (₹)',
                data: data.revenueTrend.data,
                borderColor: '#3b82f6',
                backgroundColor: 'rgba(59, 130, 246, 0.1)',
                tension: 0.4,
                fill: true
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { display: false }
            },
            scales: {
                y: { beginAtZero: true }
            }
        }
    });

    // Failure Chart
    const failCtx = document.getElementById('failureChart').getContext('2d');
    new Chart(failCtx, {
        type: 'doughnut',
        data: {
            labels: data.failureDistribution.labels,
            datasets: [{
                data: data.failureDistribution.data,
                backgroundColor: [
                    '#ef4444', '#f59e0b', '#3b82f6', '#10b981', '#8b5cf6'
                ]
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { position: 'bottom' }
            }
        }
    });
}
