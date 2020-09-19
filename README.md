# MyGusto Backend API
MyGusto is an app that caters personalized Migusto recipes to users.
This repository is the backend API that interacts with different Migros APIs.

## Quickstart Guide
To run this locally, simply set up docker on your machine and call `docker-compose up --build` from the root of this repository.
This will start a Postgres database and a Flask API, which will have a Swagger developer interface on http://0.0.0.0:5000. 

To run this on a server, make sure that gunicorn is installed. Then build the docker image and run it.

## Documentation
For documentation, please refer to the models in the Swagger interface and the comments in the code.

## Database Migrations
To create a new migration with Flask-Migrate it's easiest to start the server locally. You can then execute the migrate command like this: `docker-compose run app flask db migrate --message "ADD MIGRATION COMMENT"`.
