from datetime import datetime
import uuid

# Models to structure the data being inserted into MongoDB
# Keeps the code organized and easy to understand

class VehicleModel:
    @staticmethod
    def create(vehicle_number, owner_name, vehicle_type, rfid_tag, wallet_balance, is_blacklisted=False):
        return {
            "vehicleNumber": vehicle_number,
            "ownerName": owner_name,
            "vehicleType": vehicle_type,
            "rfidTag": rfid_tag,
            "walletBalance": wallet_balance,
            "isBlacklisted": is_blacklisted,
            "createdAt": datetime.utcnow()
        }

class TransactionModel:
    @staticmethod
    def create(vehicle_number, rfid_tag, amount, payment_method, payment_status, failure_reason=None, toll_booth_id="BOOTH-01"):
        return {
            "transactionId": str(uuid.uuid4()),
            "vehicleNumber": vehicle_number,
            "rfidTag": rfid_tag,
            "amount": amount,
            "paymentMethod": payment_method,
            "paymentStatus": payment_status,
            "failureReason": failure_reason,
            "timestamp": datetime.utcnow(),
            "tollBoothId": toll_booth_id
        }

class FailureLogModel:
    @staticmethod
    def create(failure_type, description, vehicle_number, retry_count=0):
        return {
            "failureId": str(uuid.uuid4()),
            "failureType": failure_type,
            "description": description,
            "vehicleNumber": vehicle_number,
            "retryCount": retry_count,
            "timestamp": datetime.utcnow()
        }
