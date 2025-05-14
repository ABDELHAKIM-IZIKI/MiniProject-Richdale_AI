FROM python:3.9-slim

WORKDIR /app

# Copy requirements first (caching optimization)

RUN pip install --upgrade pip

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt



# Copy all files (except those in .dockerignore)
COPY . .

EXPOSE 7000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7000"]