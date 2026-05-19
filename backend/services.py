import os
from database import get_db
from models import TransactionModel, FailureLogModel
from utils import log_failure, update_vehicle_balance, get_toll_amount
import time

db = get_db()

def detect_vehicle_service(data):
    # Simulate Vehicle Detection
    vehicle_number = data.get('vehicleNumber')
    rfid_tag = data.get('rfidTag')
    is_duplicate_scan = data.get('isDuplicateScan', False)
    
    if is_duplicate_scan:
        log_failure("Duplicate Scan", "Vehicle scanned multiple times within a short period", vehicle_number)
        return {"success": False, "message": "Duplicate Scan Detected", "status_code": 400}
        
    vehicle = db.vehicles.find_one({"vehicleNumber": vehicle_number})
    
    if not vehicle:
        # Check by RFID if vehicle number wasn't found (Camera Backup Simulation)
        if rfid_tag:
            vehicle = db.vehicles.find_one({"rfidTag": rfid_tag})
            
        if not vehicle:
             log_failure("Invalid RFID", "Unregistered RFID Tag or Vehicle", vehicle_number)
             return {"success": False, "message": "Vehicle not found. Invalid RFID.", "status_code": 404}
    
    if vehicle.get("isBlacklisted"):
        log_failure("Blacklisted Vehicle", "Attempted entry by a blacklisted vehicle", vehicle.get('vehicleNumber'))
        return {"success": False, "message": "Vehicle is blacklisted!", "status_code": 403}
        
    # Successful Detection
    return {
        "success": True,
        "message": "Vehicle detected successfully",
        "vehicle": {
            "vehicleNumber": vehicle['vehicleNumber'],
            "rfidTag": vehicle['rfidTag'],
            "vehicleType": vehicle['vehicleType'],
            "walletBalance": vehicle['walletBalance']
        },
        "status_code": 200
    }

def process_payment_service(data):
    vehicle_number = data.get('vehicleNumber')
    
    vehicle = db.vehicles.find_one({"vehicleNumber": vehicle_number})
    if not vehicle:
        return {"success": False, "message": "Vehicle not found", "status_code": 404}
        
    amount = get_toll_amount(vehicle.get('vehicleType', 'Car'))
    
    if vehicle.get('walletBalance', 0) < amount:
        log_failure("Insufficient Balance", f"Wallet balance {vehicle.get('walletBalance')} is less than toll {amount}", vehicle_number)
        
        # Log pending transaction
        transaction = TransactionModel.create(vehicle_number, vehicle.get('rfidTag'), amount, "Wallet", "Failed", "Insufficient Balance")
        db.transactions.insert_one(transaction)
        
        return {"success": False, "message": "Insufficient Balance. Please use manual payment.", "amount": amount, "status_code": 400}
        
    # Process Success Payment
    new_balance = vehicle.get('walletBalance') - amount
    update_vehicle_balance(vehicle_number, new_balance)
    
    transaction = TransactionModel.create(vehicle_number, vehicle.get('rfidTag'), amount, "Wallet", "Success")
    db.transactions.insert_one(transaction)
    
    return {
        "success": True, 
        "message": "Payment processed successfully", 
        "amountDeducted": amount,
        "remainingBalance": new_balance,
        "status_code": 200
    }

def manual_payment_service(data):
    vehicle_number = data.get('vehicleNumber')
    amount = data.get('amount')
    method = data.get('method', 'Cash') # Cash, UPI, Card
    
    vehicle = db.vehicles.find_one({"vehicleNumber": vehicle_number})
    rfid_tag = vehicle.get('rfidTag') if vehicle else "UNKNOWN"
    
    transaction = TransactionModel.create(vehicle_number, rfid_tag, amount, method, "Success")
    db.transactions.insert_one(transaction)
    
    return {"success": True, "message": f"Manual payment via {method} successful", "status_code": 200}

def retry_payment_service(data):
    # Simulating a retry mechanism which might succeed or fail
    return process_payment_service(data)

def simulate_failure_service(data):
    failure_type = data.get('type')
    
    # Store failure log
    log = FailureLogModel.create(
        failure_type=failure_type,
        description=f"Simulated failure: {failure_type}",
        vehicle_number="SIMULATION"
    )
    db.failure_logs.insert_one(log)
    
    if failure_type == "Network Delay":
        time.sleep(2) # Simulate delay
        
    return {"success": True, "message": f"Failure '{failure_type}' simulated and logged.", "status_code": 200}

def get_dashboard_data():
    total_vehicles = db.vehicles.count_documents({})
    
    pipeline = [{"$match": {"paymentStatus": "Success"}}, {"$group": {"_id": None, "totalRevenue": {"$sum": "$amount"}}}]
    revenue_result = list(db.transactions.aggregate(pipeline))
    revenue = revenue_result[0]['totalRevenue'] if revenue_result else 0
    
    successful_payments = db.transactions.count_documents({"paymentStatus": "Success"})
    failed_payments = db.transactions.count_documents({"paymentStatus": "Failed"})
    manual_payments = db.transactions.count_documents({"paymentMethod": {"$in": ["Cash", "UPI", "Card"]}})
    rfid_failures = db.failure_logs.count_documents({"failureType": "Invalid RFID"})
    
    recent_transactions = list(db.transactions.find({}, {"_id": 0}).sort("timestamp", -1).limit(5))
    recent_logs = list(db.failure_logs.find({}, {"_id": 0}).sort("timestamp", -1).limit(5))
    
    return {
        "totalVehicles": total_vehicles,
        "revenue": revenue,
        "successfulPayments": successful_payments,
        "failedPayments": failed_payments,
        "manualPayments": manual_payments,
        "rfidFailures": rfid_failures,
        "systemHealth": "Online",
        "recentTransactions": recent_transactions,
        "recentLogs": recent_logs
    }

def get_transactions(args):
    # Support basic filtering
    query = {}
    if args.get('status'):
        query['paymentStatus'] = args.get('status')
        
    transactions = list(db.transactions.find(query, {"_id": 0}).sort("timestamp", -1).limit(100))
    return {"success": True, "transactions": transactions}

def get_vehicles():
    vehicles = list(db.vehicles.find({}, {"_id": 0}).limit(100))
    return {"success": True, "vehicles": vehicles}

def get_logs():
    logs = list(db.failure_logs.find({}, {"_id": 0}).sort("timestamp", -1).limit(100))
    return {"success": True, "logs": logs}

def get_analytics():
    # Provide simple data for charts
    
    # Revenue Trend (mocked for simplicity, in a real app this would group by date)
    revenue_trend = {
        "labels": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        "data": [1200, 1500, 1100, 1800, 2200, 2500, 2100]
    }
    
    # Payment Success %
    success = db.transactions.count_documents({"paymentStatus": "Success"})
    failed = db.transactions.count_documents({"paymentStatus": "Failed"})
    total = success + failed
    success_rate = (success / total * 100) if total > 0 else 0
    
    # Failure Distribution
    pipeline = [{"$group": {"_id": "$failureType", "count": {"$sum": 1}}}]
    failures = list(db.failure_logs.aggregate(pipeline))
    failure_dist = {
        "labels": [f["_id"] for f in failures],
        "data": [f["count"] for f in failures]
    }
    
    return {
        "revenueTrend": revenue_trend,
        "paymentSuccessRate": success_rate,
        "failureDistribution": failure_dist
    }
