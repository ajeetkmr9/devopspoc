# Use the official Python image as a base image
FROM python:3.11.7-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the FastAPI application into the container
COPY . .

# Expose the port that FastAPI will run on
EXPOSE 8002

RUN chmod +x ./app_start.sh && /app/app_start.sh

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002", "--reload"]
