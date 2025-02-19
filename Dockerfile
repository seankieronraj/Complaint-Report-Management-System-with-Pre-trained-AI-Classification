# Use a lightweight Python base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Install Python and system dependencies directly
RUN apt-get update && apt-get install -y \
    git \
    && pip install --no-cache-dir \
        flask \
        transformers \
        torch \
        pytest

# Copy all project files into the container
COPY . .

# Expose port 5000 for the Flask app
EXPOSE 5000

# Run the Flask application
CMD ["python", "app.py"]
