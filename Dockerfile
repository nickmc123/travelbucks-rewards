FROM python:3.11-slim

WORKDIR /app

# Copy files
COPY requirements.txt .
COPY *.py .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 8080

# Run the application directly
CMD ["python", "main.py"]
