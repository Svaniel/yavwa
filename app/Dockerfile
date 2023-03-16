# Use an official Python runtime as a parent image
FROM python:3.8-alpine

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY . .

# Set the environment variable for Flask
ENV FLASK_APP app.py
# ENV FLASK_ENV development
# ENV FLASK_RUN_PORT 5000
# ENV FLASK_RUN_HOST 0.0.0.0

# Expose port 5000 for the Flask app
EXPOSE 5000

# Start the Flask app when the container starts
CMD ["flask", "run", "--host", "0.0.0.0"]
#CMD ["flask", "run"]
