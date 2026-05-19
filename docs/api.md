# API Documentation

## Endpoints

### 1. `POST /api/vehicle/detect`
Simulates a vehicle entering the toll plaza.
- **Body**: `{ "vehicleNumber": "MH 12 AB 1234", "rfidTag": "RFID-123", "vehicleType": "Car" }`
- **Response**: `{ "success": true, "message": "Vehicle detected successfully", "vehicle": {...} }`

### 2. `POST /api/payment/process`
Processes the automatic toll deduction.
- **Body**: `{ "vehicleNumber": "MH 12 AB 1234" }`
- **Response**: `{ "success": true, "message": "Payment processed successfully" }`

### 3. `POST /api/payment/manual`
Fallback for manual payment collection.
- **Body**: `{ "vehicleNumber": "MH 12 AB 1234", "amount": 100, "method": "Cash" }`
- **Response**: `{ "success": true, "message": "Manual payment successful" }`

### 4. `POST /api/failure/simulate`
Simulates various system failures.
- **Body**: `{ "type": "Network Delay" }`
- **Response**: `{ "success": true, "message": "Failure simulated" }`

### 5. Data Retrieval Endpoints
- `GET /api/transactions`: Returns list of transactions.
- `GET /api/vehicles`: Returns registered vehicles.
- `GET /api/dashboard`: Returns aggregated metrics for the dashboard.
- `GET /api/analytics`: Returns data formatted for Chart.js.
- `GET /api/logs`: Returns failure logs.
