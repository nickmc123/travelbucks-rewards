FROM python:3.11-slim

WORKDIR /app

# Copy files
COPY requirements.txt .
COPY main.py .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the app directly with Python (handles PORT env var internally)
CMD python main.py
