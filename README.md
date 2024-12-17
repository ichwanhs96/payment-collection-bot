# Payment Collection Bot Project

This is a simple Payment Collection bot project that uses Flask and Python virtual environment and Alembic for database migrations.

## Prerequisites

- Python > 3.8
- pip

## Setup

1. **Clone the repository:**

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Database Setup with Docker

To set up the PostgreSQL database locally using Docker Compose, follow these steps:

1. **Start the database service:**
   ```bash
   docker-compose up -d
   ```

2. **Connect to the database:**
   You can connect to the PostgreSQL database using a database client or through your application using the following connection string:
   ```
   postgres://testing:testing@localhost:5435/testing
   ```

## Database Migration with Alembic

1. **Initialize Alembic:**
   ```bash
   alembic init alembic
   ```

2. **Create a migration script:**
   ```bash
   alembic revision --autogenerate -m "Initial migration"
   ```

3. **Apply the migration:**
   ```bash
   alembic upgrade head
   ```

## Running the Application

To run the Flask application, use the following command:
```bash
flask run
```

## License
TBD