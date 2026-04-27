# Data Simulation

This repository contains Python scripts to simulate tag data and store it into MongoDB or export it as CSV files.

## Files Structure

- **`OnlyData.py`**: Generates synthetic data for existing tags in the database and updates them in real-time.
- **`Tags_withData.py`**: Creates new tags in the database and generates continuous synthetic data for them over a specified period.
- **`Data_csv.py`**: Simulates tag data and exports the results directly to a CSV file (`dicv_sim_data_test.csv`).
- **`slowchangevalues.py`**: Contains the core logic for generating smoothly changing values over time.

## Prerequisites

- Python 3.8+
- MongoDB instance (remote or local)

## Setup

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd Data_Simulation
   ```

2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure environment variables. Create a `.env` file in the root directory and add your MongoDB details:
   ```ini
   MONGO_URI="your_mongodb_connection_string"
   DB_NAME="your_database_name"
   TAG_COLLECTION="your_tag_collection"
   LIVE_COLLECTION="your_live_data_collection"
   ```

## Running the scripts

To insert multiple synthetic tags:
```bash
python OnlyData.py
```

To insert tags with associated data:
```bash
python Tags_withData.py
```

To export simulated data to a CSV:
```bash
python Data_csv.py
```
