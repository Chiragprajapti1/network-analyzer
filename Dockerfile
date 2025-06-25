# Base image with Python and system tools
FROM python:3.11-slim

# Install dependencies (including nmap)
RUN apt-get update && \
    apt-get install -y nmap && \
    apt-get clean

# Set working directory
WORKDIR /app

# Copy all project files into the container
COPY . /app

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose port
EXPOSE 5000

# Run the app
CMD ["python", "app.py"]
