# Coffee Shop

A website that helps customers to view a coffee shop menu, and allows baristas to view the ingredients of any drink, and it allows the manager to add a new drink to the menu.

## Devlopment

The app developed in python using Flask and SQLAlchemy with an SQLite for the database in the backend, for the frontend it mainly using Ionic.

### Backend

The `./backend` directory contains completed Flask server with SQLAlchemy module to simplify your data needs. You will need to complete the configuration, and integrate Auth0 for authentication.

[View the README.md within ./backend for more details.](./backend/README.md)

### Frontend

The `./frontend` directory contains a complete Ionic frontend to consume the data from the Flask server. You will only need to update the environment variables found within (./frontend/src/environment/environment.ts) to reflect the Auth0 configuration details set up for the backend app. 

[View the README.md within ./frontend for more details.](./frontend/README.md)
