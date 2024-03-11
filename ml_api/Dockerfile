FROM python:3.11

# Set environment variables
ENV FLASK_ENV=development
ENV FLASK_APP=api
ENV FLASK_DEBUG=1

# Install Apache, 'apxs', and mod-wsgi
RUN apt-get update && \
    apt-get install -y apache2 apache2-dev libapache2-mod-wsgi-py3

# Install mod_wsgi using pip
RUN pip install mod_wsgi

WORKDIR /usr/src/app

# Create a non-root user and group
RUN groupadd -r aditya-group && useradd -r -g aditya-group aditya

# Set ownership of the application directory to the non-root user
RUN chown -R aditya:aditya-group /usr/src/app

# Copy the requirements file and install dependencies
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Copy the 'api' directory into the container
COPY . .

# Expose the port
EXPOSE 8081

# Specify the non-root user for Apache and mod_wsgi-express
USER aditya

# Configure and start Apache with mod-wsgi
CMD ["mod_wsgi-express", "start-server", "--startup-log", "--log-to-terminal", "--port", "8081", "--user", "aditya", "wsgi.py"]