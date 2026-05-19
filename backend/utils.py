from database import get_db
from models import FailureLogModel

db = get_db()

def log_failure(failure_type, description, vehicle_number=None):
    """Helper utility to log failures easily."""
    log = FailureLogModel.create(failure_type, description, vehicle_number)
    if db is not None:
        db.failure_logs.insert_one(log)

def update_vehicle_balance(vehicle_number, new_balance):
    """Helper utility to update wallet balance."""
    if db is not None:
        db.vehicles.update_one(
            {"vehicleNumber": vehicle_number},
            {"$set": {"walletBalance": new_balance}}
        )

def get_toll_amount(vehicle_type):
    """Simple configuration for toll amounts based on vehicle type."""
    rates = {
        "Car": 100,
        "Bus": 250,
        "Truck": 400,
        "LCV": 150
    }
    return rates.get(vehicle_type, 100)
