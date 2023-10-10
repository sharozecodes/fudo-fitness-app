# FUDO Backend

Welcome to the FUDO Backend - Powering Your Fitness and Nutrition App

FUDO Backend is the server component of the FUDO fitness and nutrition app, built using Python and Flask. This backend server provides the necessary APIs and functionality to support the FUDO front end.

## Getting Started

To set up the FUDO Backend, follow these steps:

1. Fork and clone this repository to your local machine.

```bash
git clone git@github.com:sharozecodes/fudo-fitness-app.git
```

2. Navigate to the project directory.

```bash
cd fudo-fitness-app
```

3. Install pipenv if you haven't already.

```bash
pip install pipenv
```

4. Create and activate a virtual environment for the project.

```bash
pipenv install
pipenv shell

```

5. Navigate to the server folder.

```bash
cd server
```

6. Initialize the database (run this only once).

```bash
flask db init
```

7. Upgrade the database to the latest version.

```bash
flask db upgrade
```

8. Seed the database with initial data.

```bash
python seed.py
```

9.  Start the Flask application.

```bash
python app.py
```

The backend server will now be running at http://localhost:5555

## Link to FUDO Front End

After you have successfully set up and started the FUDO Backend, make sure to visit the [FUDO Front End](https://github.com/sharozecodes/fudo-fitness-app-frontend) to interact with the complete FUDO fitness and nutrition app.

## Contributor's Guide

We welcome contributions from the community to improve the FUDO Backend. If you would like to contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and ensure that the code is properly tested.
4. Submit a pull request, detailing the changes you've made.

## License

This project is licensed under the MIT License. You are free to use, modify, and distribute the code as per the terms of the license.
