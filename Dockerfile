# Use the official Python 3.12 image from the Docker Hub
FROM python:3.12

# Set the working directory in the container
# WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Set the entry point command to run the application
CMD ["python", "main.py"]