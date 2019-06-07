# NeuroFlow Assessment Project
> This repository features my solution to the NeuroFlow Assessment 

```sh
export FLASK_APP=mood_tracker.py
```

Testing in the shell
```
flask shell
```

Docker
```
docker build -t neuroflow:latest .
docker run --name neuroflow --rm -p 5000:5000 --rm neuroflow:latest

```