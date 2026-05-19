from database import get_db
from models import VehicleModel
from faker import Faker
import random

fake = Faker('en_IN')
db = get_db()

def generate_sample_data():
    if db is None:
        print("Database not connected. Cannot insert sample data.")
        return

    # Check if we already have data
    if db.vehicles.count_documents({}) > 0:
        print("Data already exists. Skipping dummy data generation.")
        return
        
    print("Generating sample data...")
    
    vehicle_types = ['Car', 'Bus', 'Truck', 'LCV']
    vehicles_data = []
    
    # Generate 20 vehicles
    for i in range(20):
        # Format: MH 12 AB 1234
        state_codes = ['MH', 'KA', 'DL', 'GJ', 'TN']
        v_num = f"{random.choice(state_codes)} {random.randint(10, 99)} {fake.lexify('??').upper()} {random.randint(1000, 9999)}"
        rfid = f"RFID-{fake.uuid4()[:8].upper()}"
        
        balance = random.choice([0, 50, 100, 500, 1000, 2000])
        is_blacklisted = random.choice([True, False, False, False, False]) # 20% chance
        v_type = random.choice(vehicle_types)
        
        vehicle = VehicleModel.create(
            vehicle_number=v_num,
            owner_name=fake.name(),
            vehicle_type=v_type,
            rfid_tag=rfid,
            wallet_balance=balance,
            is_blacklisted=is_blacklisted
        )
        vehicles_data.append(vehicle)
        
    if vehicles_data:
        db.vehicles.insert_many(vehicles_data)
        print("Sample vehicles inserted successfully!")

if __name__ == "__main__":
    generate_sample_data()
