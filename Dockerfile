FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*

COPY Artifacts/requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

ENV PYTHONPATH=/app/Artifacts/app

CMD ["shiny", "run", "Artifacts.app.app:app", "--host", "0.0.0.0", "--port", "8000"]