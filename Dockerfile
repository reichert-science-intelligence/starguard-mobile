FROM python:3.11

WORKDIR /app

COPY Artifacts/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 7860

WORKDIR /app/Artifacts/app
CMD ["shiny", "run", "app:app", "--host", "0.0.0.0", "--port", "7860"]