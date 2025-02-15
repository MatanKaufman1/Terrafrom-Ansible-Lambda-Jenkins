FROM python:3.12-slim AS build-stage
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r /app/src/http_app/requirements.txt

FROM python:3.12-slim AS runtime-stage
WORKDIR /app
COPY --from=build-stage /app /app
RUN pip install --no-cache-dir flask
EXPOSE 5000
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
CMD ["flask", "run"]
