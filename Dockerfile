FROM python:3.8-alpine

WORKDIR /application
EXPOSE 8000
COPY requirements.txt .

RUN apk add libpq-dev build-base && \
    pip3 install -r requirements.txt --no-cache-dir

COPY . /application/
ENV DEBUG=False

CMD ["gunicorn", "--config", "gunicorn.config.py", "challenge.wsgi:application"]