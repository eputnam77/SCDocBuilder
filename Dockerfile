FROM python:3.12-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir .

EXPOSE 8000

ENTRYPOINT ["scdocbuilder"]
