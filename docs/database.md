# Database Schema

The project uses MongoDB to store the simulation data. The database is called `smart_toll_simulator`.

## Collections

### 1. `vehicles`
Stores registered vehicles and their wallet balances.
- `vehicleNumber` (String): Unique identifier.
- `ownerName` (String): Name of the owner.
- `vehicleType` (String): Car, Bus, Truck, LCV.
- `rfidTag` (String): The simulated RFID tag.
- `walletBalance` (Number): Current balance.
- `isBlacklisted` (Boolean): Whether the vehicle is blacklisted.
- `createdAt` (Date): Registration date.

### 2. `transactions`
Stores all payment attempts (success and failures).
- `transactionId` (String): UUID.
- `vehicleNumber` (String): The vehicle involved.
- `rfidTag` (String): The RFID used.
- `amount` (Number): Toll amount.
- `paymentMethod` (String): Wallet, Cash, UPI, Card.
- `paymentStatus` (String): Success, Failed.
- `failureReason` (String): Reason if failed.
- `timestamp` (Date): Time of transaction.
- `tollBoothId` (String): Identifier for the booth.

### 3. `failure_logs`
Stores simulated system failures and errors for analytics.
- `failureId` (String): UUID.
- `failureType` (String): Category of failure (e.g., 'Network Delay').
- `description` (String): Detailed reason.
- `vehicleNumber` (String): Associated vehicle, if any.
- `retryCount` (Number): Number of retries attempted.
- `timestamp` (Date): Time of failure.
