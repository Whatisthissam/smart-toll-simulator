# Architecture

The Smart Toll Collection Simulator follows a modular, distributed-systems-inspired architecture to simulate real-world conditions of a large-scale electronic toll collection system.

## Components

1. **Frontend Layer**: Built with HTML, CSS, and Vanilla JS for a lightweight, beginner-friendly UI. It serves as the Dashboard and Simulation trigger mechanism.
2. **API Gateway (Flask Route Layer)**: Handles all incoming requests from the frontend and routes them to appropriate services.
3. **Services Layer**: Contains business logic (Detection, Validation, Payment, Failure Injection).
4. **Data Layer**: MongoDB is used to persist Vehicles, Transactions, and Failure Logs.

## Workflow

1. **Detection**: Vehicle approaches the toll. RFID is scanned.
2. **Validation**: System checks if the vehicle is registered, blacklisted, or if the scan is a duplicate.
3. **Payment**: System checks wallet balance and deducts the toll amount. If insufficient, it marks the transaction as failed and requires manual intervention.
4. **Logging**: All successful transactions, failures, and manual interventions are logged into the database.
5. **Analytics**: The dashboard fetches aggregated data to show system health, revenue, and failure distributions.
