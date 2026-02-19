# Train Station API 🚂

API service for managing train trips, creating orders, and buying tickets.
Written in Python using Django REST Framework.

## Features
- **JWT Authentication** (Register, Login, Refresh)
- **Admin Panel** to manage trains, stations, and trips.
- **Documentation** via Swagger UI.
- **Validation**: Cannot buy a ticket for an occupied seat.
- **Filtering**: Find trips by city and date.
- **Dockerized**: Run efficiently with Docker & PostgreSQL.

## Technologies
- Python 3.11+
- Django 5 & DRF
- PostgreSQL
- Docker & Docker Compose

## How to Run 

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/nastyagst/train-station-api.git](https://github.com/nastyagst/train-station-api.git)
   cd train-station-api

2. **Create .env file:**
   Copy the sample config:

    cp .env.sample .env

   *Note: Inside .env, define variables like POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST=db, POSTGRES_PORT=5432.*

3. **Build and run with Docker:**
    ```bash
    docker-compose up --build

4. **Access the API:**
   - **API Root**: http://127.0.0.1:8002/api/station/
   - **Swagger Docs**: http://127.0.0.1:8002/api/doc/swagger/

## Running Tests 

To run tests inside the Docker container:

    docker-compose exec app python manage.py test

## API Usage Flow

1. **Register** a new user (/api/user/register/).
2. **Obtain Token** (/api/user/token/).
3. **Create Stations** (e.g., Kyiv, Lviv).
4. **Create Route** (Kyiv -> Lviv).
5. **Create Train** (Define capacity and type).
6. **Create Journey** (Assign a Train to a Route at a specific time).

7. **Buy Tickets** (Create an Order with selected seats).
