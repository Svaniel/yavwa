FROM python:3.8-alpine

# Create a group and user
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# User to run with
USER appuser

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Add pip dir to PATH
ENV PATH=/home/appuser/.local/bin:$PATH

# Upgrade pip
# RUN /usr/local/bin/python -m pip install --upgrade pip

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Copy the application code into the container
COPY . .

# Set the environment variable for Flask
ENV FLASK_APP app.py
ENV FLASK_ENV development
ENV FLASK_RUN_PORT 5000
ENV FLASK_RUN_HOST 0.0.0.0

# Expose port 5000 for the Flask app
EXPOSE 5000

# Start the Flask app when the container starts
CMD ["flask", "run"]