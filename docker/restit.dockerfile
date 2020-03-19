FROM        python:3.8.2-alpine

EXPOSE      5000

COPY        restit_app.py /

RUN         pip3 install gunicorn restit

ENTRYPOINT  ["gunicorn", "--bind", "0.0.0.0:5000", "restit_app:app"]
