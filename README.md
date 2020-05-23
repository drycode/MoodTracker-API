# Mood Tracker API

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
> A REST API which allows users track their mood. 

## Features
1. Allows users to Login to their account, and privately submit their current mood to a persistent database. Users can view their mood entries over time.
2. Users who submit at least 1 mood rating daily will maintain a "streak" (a measure of consecutive days in which they submitted to the app).
3. The user's streak percentile compared to other users will be tracked, and if a user is in the 50% percentile, it will be retrievable
4. The development server for the application is containerized using Docker


## Running Development Server
```sh
$ pip install -r requirements.txt
$ export FLASK_APP=mood_tracker.py 
$ export FLASK_ENV=development
$ flask db init 
$ flask db migrate 
$ flask db upgrade
$ flask run 
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 277-572-647
```

## Testing in the shell
Environment variables have been instantiated in `mood_tracker.py`
```py
@app.shell_context_processor
def make_shell_context():
    """
    Establishes necessary context to test server in the python shell.
    Execute by typing `flask shell`
    """
    return {"db": db, "User": User, "MoodEntry": MoodEntry}

```
A python shell can be run with these environment variables pre-imported by executing:

```sh
$ flask shell
```

## Run Unit Tests
```
$ pytest
============================= test session starts ==============================
platform darwin -- Python 3.7.2, pytest-4.6.2, py-1.8.0, pluggy-0.12.0
collected 21 items

tests/test_helpers.py ............                                       [ 57%]
tests/test_models.py .........                                           [100%]
========================== 21 passed in 0.51 seconds ===========================
```


## Running Docker Container
_--Docker can be installed from the [Docker website](https://docs.docker.com/docker-for-mac/install/)._


```sh
$ docker build -t moodtracker:latest .
$ docker run --name moodtracker --rm -p 5000:5000 --rm moodtracker:latest
```


## [API Endpoints](https://documenter.getpostman.com/view/6396321/S1TZxvQw?version=latest)
_-- Follow the link for Auto generated Postman Docs_
<hr>

#### GET Check Server
_-- This confirms that the server is active._

`http://localhost:5000/health`
##### SAMPLE OUTPUT
```json
{
    "msg": "Flask is up and running!"
}
```
<hr>

#### GET Active User
_-- This returns information about the active user._

`http://localhost:5000/getuser`

##### SAMPLE OUTPUT
```json
{
    "msg": "<User DanYoung> is active.",
    "user_id": "2"
}
```
<hr>

#### POST Login
_-- This creates a new user and stores it in the database._

`http://localhost:5000/mood`


##### HEADERS
```json
{
    "username": "DanYoung",
    "email": "dan@testemail.com",
    "password": "testpass1"
}
```

##### SAMPLE OUTPUT
```json
{
    "User": {
        "best_streak": 0,
        "current_streak": 0,
        "email": "dan@testemail.com",
        "id": 2,
        "username": "DanYoung"
    },
    "msg": "Successfully created user with username DanYoung"
}
```

<hr>

#### GET Logout
_-- This logs the user out._

`http://localhost:5000/logout`

<hr>

#### POST Moods
_-- This route allows users to post a mood score (int between 1 and 10) to the database._

`http://localhost:5000/mood`
##### HEADERS
```json
{
    "mood_score": 2
}
```

##### SAMPLE OUTPUT
```json
{
    "id": 10,
    "mood_score": 2,
    "timestamp": "Jun 08 2019 20:14:37",
    "user_id": 2
}
```

<hr>

#### GET Moods

_-- This returns a list off all the mood scores posted by a user, as well as their best streak, current streak, and percentile rank compare to other users (if greater than 50)._

`http://localhost:5000/mood`



##### SAMPLE OUTPUT
```json
{
    "best_streak": 8,
    "current_streak": 5,
    "mood_entries": [
        {
            "id": 8,
            "mood_score": 2,
            "timestamp": "Jun 08 2019 20:14:37",
            "user_id": 2
        },
        {
            "id": 9,
            "mood_score": 2,
            "timestamp": "Jun 08 2019 20:14:37",
            "user_id": 2
        },
        {
            "id": 10,
            "mood_score": 2,
            "timestamp": "Jun 08 2019 20:14:37",
            "user_id": 2
        }
    ],
    "percentile": 50
}
```