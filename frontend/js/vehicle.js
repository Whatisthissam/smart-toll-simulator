async function detectVehicle() {
    const vNum = document.getElementById('vehicleNum').value;
    const rfid = document.getElementById('rfidTag').value;
    const vType = document.getElementById('vehicleType').value;
    
    const resultDiv = document.getElementById('detection-result');
    resultDiv.innerHTML = '<p>Processing...</p>';
    
    const res = await apiCall('/vehicle/detect', {
        method: 'POST',
        body: JSON.stringify({ vehicleNumber: vNum, rfidTag: rfid, vehicleType: vType })
    });
    
    if (res.success) {
        showNotification(res.message, 'success');
        resultDiv.innerHTML = `
            <p><strong>Status:</strong> <span style="color:var(--success)">Success</span></p>
            <p><strong>Vehicle:</strong> ${res.vehicle.vehicleNumber}</p>
            <p><strong>Type:</strong> ${res.vehicle.vehicleType}</p>
            <p><strong>Wallet Balance:</strong> ₹${res.vehicle.walletBalance}</p>
        `;
    } else {
        showNotification(res.message, 'error');
        resultDiv.innerHTML = `
            <p><strong>Status:</strong> <span style="color:var(--danger)">Failed</span></p>
            <p><strong>Reason:</strong> ${res.message}</p>
        `;
    }
}

async function simulateDuplicate() {
    const vNum = document.getElementById('vehicleNum').value || "UNKNOWN";
    const res = await apiCall('/vehicle/detect', {
        method: 'POST',
        body: JSON.stringify({ vehicleNumber: vNum, isDuplicateScan: true })
    });
    showNotification(res.message, 'error');
}
