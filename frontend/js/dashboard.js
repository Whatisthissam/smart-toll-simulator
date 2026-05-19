document.addEventListener('DOMContentLoaded', () => {
    loadDashboardData();
    setInterval(loadDashboardData, 10000); // Refresh every 10s
});

async function loadDashboardData() {
    const data = await apiCall('/dashboard');
    if (!data) return;
    
    const statsContainer = document.getElementById('dashboard-stats');
    if (statsContainer) {
        statsContainer.innerHTML = `
            <div class="card"><h3>Total Vehicles</h3><div class="value">${data.totalVehicles || 0}</div></div>
            <div class="card"><h3>Total Revenue</h3><div class="value">₹${data.revenue || 0}</div></div>
            <div class="card"><h3>Successful Payments</h3><div class="value" style="color:var(--success)">${data.successfulPayments || 0}</div></div>
            <div class="card"><h3>Failed Payments</h3><div class="value" style="color:var(--danger)">${data.failedPayments || 0}</div></div>
            <div class="card"><h3>Manual Payments</h3><div class="value" style="color:var(--warning)">${data.manualPayments || 0}</div></div>
            <div class="card"><h3>RFID Errors</h3><div class="value">${data.rfidFailures || 0}</div></div>
        `;
    }

    const txTable = document.querySelector('#recent-transactions tbody');
    if (txTable && data.recentTransactions) {
        txTable.innerHTML = data.recentTransactions.map(tx => `
            <tr>
                <td>${tx.vehicleNumber}</td>
                <td>₹${tx.amount}</td>
                <td><span class="badge ${tx.paymentStatus === 'Success' ? 'badge-success' : 'badge-danger'}">${tx.paymentStatus}</span></td>
            </tr>
        `).join('');
    }

    const logsTable = document.querySelector('#recent-logs tbody');
    if (logsTable && data.recentLogs) {
        logsTable.innerHTML = data.recentLogs.map(log => `
            <tr>
                <td><span class="badge badge-warning">${log.failureType}</span></td>
                <td>${log.description}</td>
            </tr>
        `).join('');
    }
}
