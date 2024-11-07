<<<<<<< HEAD
# Use the official Python image from the Docker Hub
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install the necessary packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the .env file into the container
COPY .env .env

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run the application
=======
# Use the official Python image from the Docker Hub
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install the necessary packages
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run the application
>>>>>>> 4f66296194ac0ddcb31b9e9489986124843dd390
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]
