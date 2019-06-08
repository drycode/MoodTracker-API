# NeuroFlow Assessment Project

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
> This repository features my solution to the NeuroFlow Assessment 

## Project Requirements

1. Create a web REST application with a '/mood' endpoint, which when POSTed to persists the submitted mood value.
2. Add a GET method to the '/mood' endpoint which returns all submitted mood values
3. Add the ability for users to login. The GET method for the '/mood' endpoint should now only return values submitted by the logged-in user.
4. Add to the body of the response for the ‘/mood’ endpoint the length of their current "streak". A user is on a “streak” if that user has submitted at least 1 mood rating for each consecutive day of that streak.
5. Calculate the user's streak's percentile compared to other users, and if the percentile is >= 50%, return that percentile
6. Containerize your application


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
```


## Running Docker Container
_--Docker can be installed from the [Docker website](https://docs.docker.com/docker-for-mac/install/)._


```sh
$ docker build -t neuroflow:latest .
$ docker run --name neuroflow --rm -p 5000:5000 --rm neuroflow:latest
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