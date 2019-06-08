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
FLASK_ENV=development
$ flask db init 
$ flask db migrate 
$ flask db upgrade
$ flask run 
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

## Running Docker Container
_--Docker can be installed from the [Docker website](https://docs.docker.com/docker-for-mac/install/)._


```sh
$ docker build -t neuroflow:latest .
$ docker run --name neuroflow --rm -p 5000:5000 --rm neuroflow:latest
```


