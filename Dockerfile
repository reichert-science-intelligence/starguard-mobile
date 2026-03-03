FROM python:3.11

WORKDIR /app

# Copy requirements from Artifacts/app
COPY Artifacts/app/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy all files
COPY . .

# Expose port
EXPOSE 7860

# Change to app directory and run
WORKDIR /app/Artifacts/app
CMD ["shiny", "run", "app:app", "--host", "0.0.0.0", "--port", "7860"]
```

**5. Click "Commit new file to main"**

---

## ⏰ WHAT HAPPENS NEXT

**Immediately after committing:**

1. **HuggingFace will detect the Dockerfile**
2. **Build will start automatically**
3. **"Logs" tab will show build progress**
4. **Wait 2-3 minutes**
5. **App tab should show your running app**

---

## ✅ EXPECTED RESULT

**After the Dockerfile is at root, the Files tab should show:**
```
StarGuardAI / main
├── Dockerfile          ← NEW - at root level
├── Artifacts/
│   └── Dockerfile      ← Old one (can ignore)
└── README.md