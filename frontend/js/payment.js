document.addEventListener('DOMContentLoaded', loadTransactions);

async function loadTransactions() {
    const data = await apiCall('/transactions');
    const tbody = document.querySelector('#transactions-table tbody');
    if (!tbody || !data.transactions) return;
    
    tbody.innerHTML = data.transactions.map(tx => `
        <tr>
            <td style="font-size:12px; color:var(--text-muted)">${tx.transactionId.substring(0,8)}</td>
            <td>${tx.vehicleNumber}</td>
            <td>₹${tx.amount}</td>
            <td>${tx.paymentMethod}</td>
            <td><span class="badge ${tx.paymentStatus === 'Success' ? 'badge-success' : 'badge-danger'}">${tx.paymentStatus}</span></td>
            <td style="font-size:12px">${new Date(tx.timestamp).toLocaleString()}</td>
        </tr>
    `).join('');
}

async function processAutoPayment() {
    const vNum = document.getElementById('autoVehicleNum').value;
    const res = await apiCall('/payment/process', {
        method: 'POST',
        body: JSON.stringify({ vehicleNumber: vNum })
    });
    
    if (res.success) {
        showNotification(res.message, 'success');
    } else {
        showNotification(res.message, 'error');
    }
    loadTransactions();
}

async function processManualPayment() {
    const vNum = document.getElementById('manualVehicleNum').value;
    const amt = document.getElementById('manualAmount').value;
    const method = document.getElementById('manualMethod').value;
    
    const res = await apiCall('/payment/manual', {
        method: 'POST',
        body: JSON.stringify({ vehicleNumber: vNum, amount: parseFloat(amt), method: method })
    });
    
    if (res.success) {
        showNotification(res.message, 'success');
    } else {
        showNotification(res.message, 'error');
    }
    loadTransactions();
}
