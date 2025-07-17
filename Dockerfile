# Dockerfile for PyQt6 Offender Management App
FROM python:3.11-slim

# Set workdir
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy source code
COPY . .

# Default command: run app (có thể đổi thành test trong CI)
CMD ["python", "main.py"] 