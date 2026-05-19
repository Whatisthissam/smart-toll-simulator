document.addEventListener('DOMContentLoaded', loadLogs);

async function loadLogs() {
    const data = await apiCall('/logs');
    const tbody = document.querySelector('#logs-table tbody');
    if (!tbody || !data.logs) return;
    
    tbody.innerHTML = data.logs.map(log => `
        <tr>
            <td><span class="badge badge-warning">${log.failureType}</span></td>
            <td>${log.description}</td>
            <td>${log.vehicleNumber || 'N/A'}</td>
            <td style="font-size:12px">${new Date(log.timestamp).toLocaleString()}</td>
        </tr>
    `).join('');
}

async function simulateFailure(type) {
    const res = await apiCall('/failure/simulate', {
        method: 'POST',
        body: JSON.stringify({ type: type })
    });
    
    if (res.success) {
        showNotification(res.message, type.includes('Error') || type.includes('Failure') ? 'error' : 'warning');
    } else {
        showNotification("Failed to simulate", 'error');
    }
    loadLogs();
}
