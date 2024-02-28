# Use a lightweight Python image
FROM python:3.10.12

# Set working directory
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

RUN apt-get update && apt-get install -y sqlite3 

# Copy project files
COPY . .

# Expose port for Django app
EXPOSE 8000

# Run migrations and start the development server
RUN bash scripts/setup.sh
CMD ["python", "manage.py", "runserver"]
