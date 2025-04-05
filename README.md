# Sensor Data Batch Ingestion System

This project implements a batch ingestion pipeline for environmental IoT sensor data. It reads semi-structured telemetry data from a CSV file, validates and processes it using Python, and stores the cleaned data in a MongoDB database. The system is fully containerized using Docker and Docker Compose to ensure portability and easy deployment.

The project demonstrates:
- Scalable batch ingestion with Python
- Schema-flexible storage using MongoDB
- Data validation and error logging
- Environment-based configuration with .env support
- Containerized setup with Docker Compose

## Dataset (Not Included)

The dataset used in this project is not included in the repository due to licensing. Please download it manually from Kaggle and place it in the project root directory.

Dataset source:  
[Environmental Sensor Telemetry Dataset on Kaggle](https://www.kaggle.com/datasets/garystafford/environmental-sensor-data-132k)

Expected filename:
```
iot_telemetry_data.csv
```

## Environment Configuration

This project uses a `.env` file to manage configuration variables. Create a `.env` file in the root directory with the following content:

```
MONGO_URI=mongodb://localhost:27017
DB_NAME=environment
COLLECTION_NAME=sensor_data
```

These variables are loaded automatically using the `python-dotenv` package.

## How to Run the Project

### Prerequisites

- Docker
- Docker Compose
- Python 3.8+
- `python-dotenv` (automatically installed with requirements)

### Setup Instructions

1. Clone the repository:

   ```
   git clone https://github.com/valerieholtz/sensor-data-batch-ingestion.git
   cd sensor-data-batch-ingestion
   ```

2. Download the dataset from Kaggle and place it in the root folder with the name:

   ```
   iot_telemetry_data.csv
   ```

3. Create a `.env` file with your MongoDB connection and collection config.

4. Build and start the application:

   ```
   docker compose up --build
   ```

This will:
- Launch a MongoDB container
- Build and run the Python batch ingestion script
- Insert valid records into MongoDB
- Log invalid records to `logs/invalid_rows.log`


## Project Structure

```
sensor-data-batch-ingestion/
├── ingest.py              # Batch ingestion script
├── validate.py            # Validation logic
├── .env                   # Environment variables (not committed)
├── Dockerfile             # Python environment container
├── docker-compose.yml     # MongoDB and Python orchestration
├── requirements.txt       # Python dependencies
├── logs/                  # Log directory (created automatically)
└── iot_telemetry_data.csv # Dataset file (add manually)
```

## Future Enhancements

- Integration with Terraform for cloud infrastructure provisioning
- API layer for querying data (Flask or FastAPI)
- Basic frontend dashboard for visualization

## License and Credits

- Dataset: Gary Stafford, Kaggle  
- Code: Licensed under MIT License
