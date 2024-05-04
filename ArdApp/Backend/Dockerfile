FROM python:alpine
COPY . /app
WORKDIR /app
RUN \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
 python3 -m pip install -r requirements.txt --no-cache-dir && \
 apk --purge del .build-deps && \
 apk --no-cache --update add libffi-dev 

EXPOSE 5000
CMD ["python3", "app.py"]