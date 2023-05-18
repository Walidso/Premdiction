PREMDICTION by:
Gary Bennet
Pontus Brusewitz
Walid Soboh



This project involves creating a simple RESTful Flask API application named 'PREMDICTION'. The purpose of this application is to allow users to make predictions on the outcome of Premier League football matches.

# Premdiction - The Premier League Prediction App

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.


## Prerequisites

The following tools need to be installed on your machine:

- Python 3.8 or higher
- pip
- virtualenv


## Installing

1. Clone the repository:

    git clone https://github.com/yourusername/premdiction.git
    cd premdiction

2. Create a virtual environment and activate it:

    python3 -m venv .venv
    source .venv/bin/activate

3. Install the required Python packages:

    pip install -r requirements.txt
  
4. Initialize the SQLite database:
first of all you have to change the path to the database.db file in app.py to the actuall path where you keep the database file  : app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///............write the path for database.db here.......\\instance\\database.db'
now we can start initialising the database:

you can use those commandos:

    python (or python3 depends on what version you have)
    from app import db
    db.create_all()
    exit()


## External API Setup

The application uses the [Football Data API](https://www.football-data.org/) to fetch match data. Here are the steps to use it:

1. Visit [Football Data API](https://www.football-data.org/) and register for a free account.

2. Once registered, you will receive an API Key. Store it safely.

3. In your local project, you need to set this API Key in the environment variables. The key is named `API_KEY`:  Create a file and name it .env and you should have this line in it:
API_KEY="your-api-key"
Replace `<your-api-key>` with the actual key you received upon registration.

4. The app fetches data from the Football Data API by making requests to the specific endpoints. You can use it for endpoints used in this app like `/teams` and `/matches`. The data from these endpoints are used to power the match predictions feature.

5. The API rate limits free tier users to a certain number of requests per minute. If you exceed this limit, you may need to wait for a bit before you can make more requests.

6. If you encounter any issues, please refer to the Football Data API documentation or contact their support.

Now, when you run your app, it will use the Football Data API to fetch Premier League match data.


## Running the App

To run the app:

1. Make sure you're in the project directory and the virtual environment is activated.

2. Run the Flask app:

    python app.py

The app should now be running at [http://localhost:5000].

## API Documentation

The API documentation for the project is described using the OpenAPI Specification (Swagger). The documentation includes all the details of the API's endpoints, request/response types, and status codes.

You can view the Swagger documentation by navigating to [http://localhost:5000/api/docs] in your browser.


