FROM python:3.7-alpine3.9

RUN apk add --no-cache gcc musl-dev
RUN adduser -D -g '' admin
WORKDIR /home/MoodTracker

COPY requirements.txt requirements.txt
RUN python -m venv venv

RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn


COPY app app
COPY migrations migrations
COPY mood_tracker.py config.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP mood_tracker.py

RUN chown -R admin:admin ./
USER admin

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]

CMD ["flask run"]