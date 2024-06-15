# Weather Data API

## Overview

This Django project provides an API to manage and retrieve weather records and statistics. It includes endpoints for listing weather records and statistics, with filtering options for date and station. The project also includes pagination and API documentation.

## Table of Contents

- [Project Structure](#project-structure)
- [Installation](#installation)
- [Running the Server](#running-the-server)
- [API Endpoints](#api-endpoints)
- [Running Tests](#running-tests)
- [Data Ingestion Command](#data-ingestion-command)
- [API Documentation](#api-documentation)
- [AWS Deployment](#aws-deployment)



## Project Structure

```bash
├── manage.py
├── db.sqlite3
├── requirements.txt
├── weather/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py             # Defines the `WeatherRecord` and `WeatherStatistics` models.
│   ├── serializers.py        # Contains serializers for the models.
│   ├── tests.py              # Contains the test cases for the API endpoints.
│   ├── urls.py               # Defines the URL patterns for the API.
│   ├── views.py              # Implements the API views using Django Rest Framework generics.
│   ├── migrations/
│   │   └── __init__.py
│   └── management/
│       └── commands/
│           └── ingest_weather_data.py  # Custom command for data ingestion.
├── weather_data_api/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
└── Readme.md
```



## Installation

1. **Clone the Repository**

   ```bash
   git clone <repository_url>
   cd <repository_directory>
   ```

2. **Create a Virtual Environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Apply Migrations**

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

## Running the Server

To run the Django development server, use the following command:

```bash
python manage.py runserver
```
>example output: 

![](/img/terminal_output.png)

The server will start at `http://127.0.0.1:8000/`.


## API Endpoints

### Weather Records

- **List Weather Records**
  - URL: `/weather/records/`
  - Method: `GET`
  - Query Parameters:
    - `date`: Filter by date (format: YYYY-MM-DD)
    - `station`: Filter by station ID

### Weather Statistics

- **List Weather Statistics**
  - URL: `/weather/stats/`
  - Method: `GET`
  - Query Parameters:
    - `year`: Filter by year
    - `station`: Filter by station ID

## Running Tests

To run the tests, use the following command:

```bash
python manage.py test
```
>example output:

![](/img/tests_output.png)

### Test Cases

The project includes test cases for filtering weather records and statistics. These are located in `tests.py` and test the following scenarios:

> WeatherRecordListTests
- Filtering weather records by date
- Filtering weather records by station
- Filtering weather records by both date and station
- Handling invalid date format in weather records
- Filtering weather records by invalid station
- Filtering weather records by date and invalid station
> WeatherStatisticsListTests
- Filtering weather statistics by year
- Filtering weather statistics by station
- Filtering weather statistics by both year and station
- Filtering weather statistics by year, station, and date
- Filtering weather statistics by invalid year
- Filtering weather statistics by invalid station
- Filtering weather statistics by year and invalid station
- Filtering weather statistics by year, station, and invalid date
- Swagger schema availability
- Redoc schema availability



## Test Coverage (98%)
![](/img/cover.png)


## Data Ingestion Command

The project includes a custom Django management command to ingest weather data from text files. The command reads data from files, processes it, and stores it in the database.

### Usage

```bash
python manage.py ingest_weather_data <data_dir>
```

- `data_dir`: Directory containing weather data files in text format

### Example Command

```bash
python manage.py ingest_weather_data data/wx_data/
```

## API Documentation

API documentation is provided using drf-spectacular and can be accessed at the following endpoints:

- **Swagger UI**: `/weather/api/docs/`
- **ReDoc**: `/weather/api/redoc/`

## AWS Deployment

**Deploy Django API:**
Use AWS Elastic Beanstalk to easily deploy and run a web application in multiple languages, including Python, which is used by Django.
Configure a load balancer to handle incoming traffic and distribute it to multiple instances of the Django application.


**Deploy database:**
Use Amazon Relational Database Service (RDS) to host a PostgreSQL database. It is fully managed and provides a scalable and secure database solution. and Configure database access in Django to securely connect to the RDS instance.

**Data Storage:**
Use AWS S3 to store text files.


**Scheduling data ingestion:**
Use AWS ECS FARGATE to run the data ingestion code on a schedule and ECR for storing the Image.
and Use Amazon CloudWatch Events to set up a rule to trigger the Fargate tasks at specific intervals.
Store the ingested data in the RDS database.


**Conclusion**
With this approach, application is scalable, secure, and easily managed deployment of Django API, database, and data ingestion code.
The load balancer and auto-scaling features of AWS Elastic Beanstalk and Amazon RDS will ensure that the API and database can handle changing levels of traffic, while AWS ECS FARGATE and Amazon CloudWatch Events allow you to run the data ingestion code as needed without having to manage any infrastructure.



## Screen Shots
![](/img/1.png)
![](/img/2.png)


