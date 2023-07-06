# Dockerfile

# Base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy source code to container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port on which the Flask server will run
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Create the SQLite database file
RUN python -c "from app import create_tables; create_tables()"

# Run the application
CMD [ "flask", "run" ]

