FROM python:alpine

RUN apk update && \
    apk add --no-cache postgresql-libs postgresql-dev gcc musl-dev libffi-dev

COPY . /app
WORKDIR /app

RUN python3 -m pip install -r requirements.txt --no-cache-dir

EXPOSE 5000
CMD ["python3", "app.py"]