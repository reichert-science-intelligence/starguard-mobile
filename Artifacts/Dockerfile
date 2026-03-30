FROM python:3.11

WORKDIR /app

# Copy requirements from the Artifacts/app directory
COPY Artifacts/app/requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir \
    gotrue==1.3.0 \
    httpcore==0.16.3 \
    httpx==0.24.0 \
    anyio==3.7.1 \
    python-dotenv==1.0.0 \
    supabase==2.3.0 \
    && pip install --no-cache-dir -r requirements.txt

# Copy everything
COPY . .

# Expose the port HuggingFace expects
EXPOSE 7860

# Run the Shiny app from the Artifacts/app directory
# Using the package structure: Artifacts.app.app:app
CMD ["shiny", "run", "Artifacts.app.app:app", "--host", "0.0.0.0", "--port", "7860"]