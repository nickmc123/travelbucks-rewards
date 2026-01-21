FROM python:3.11-slim

WORKDIR /app

# Copy files
COPY requirements.txt .
COPY main.py .
COPY start.sh .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Make script executable
RUN chmod +x start.sh

# Expose port
EXPOSE 8080

# Run the startup script (shell form to invoke shell)
CMD ./start.sh
