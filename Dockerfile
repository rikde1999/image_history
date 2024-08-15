FROM python:3.9

# Prevent Python from writing .pyc files to disk
ENV PYTHONDONTWRITEBYTECODE 1

# Ensure Python output is not buffered
ENV PYTHONUNBUFFERED 1

# Install system dependencies and create the working directory
RUN apt-get update && apt-get install -y \
    libpq-dev \
    build-essential

RUN mkdir /image_history
WORKDIR /image_history

# Install Python dependencies
COPY requirements.txt /image_history/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the project files into the container
COPY . /image_history/

# Expose port 8000 for Django to use
EXPOSE 8000

# Run the application
CMD ["sh", "-c", "python3 manage.py showmigrations && python3 manage.py runserver 0.0.0.0:8000"]
