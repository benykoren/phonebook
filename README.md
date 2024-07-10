# Phonebook API

This is a simple phonebook web server API built using Python and Flask, with SQLite as the database.

## Getting Started

### Prerequisites

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Installation

**Clone the repository and run tha applicaiton**:

   ```bash
   git clone https://github.com/benykoren/phonebook.git
   cd phonebook

Build and run the application using Docker Compose:
docker-compose up --build

Stop the application using Docker Compose:
docker-compose down

Build and run the application using Docker run:
docker build -t my-flask-app .
docker run -p 5000:5000 my-flask-app

Stop the application using Docker kill:
docker kill my-flask-app  
```

I added a test file for checking the server logic.
You can run it without the server, and it will test the server logic.
In addition, I added a file named request_checker.py.
This file can be used to check the server with the requests package in Python.

### API Documentation

Base URL
The base URL for all endpoints is http://localhost:5000.
API's
GET /contacts get list of all contacts.
GET /contacts/<id> get details of a specific contact by ID.
POST /contacts Adds a new contact.
PUT /contacts/<id> Updates an existing contact by ID.
DELETE /contacts/<id> Deletes a specific contact by ID.
