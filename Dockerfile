# Use the official Python Alpine image
FROM python:3.11-alpine

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Copy requirements.txt and install dependencies
COPY requirements.txt /requirements.txt
RUN apk add --update --no-cache --virtual .tmp gcc libc-dev linux-headers \
    && pip install --no-cache-dir -r /requirements.txt \
    && apk del .tmp

# Create the /app directory and set it as the working directory
RUN mkdir /app
WORKDIR /app

# Copy the application code to the container
COPY ./app /app

# Create the /scripts directory
RUN mkdir /scripts

# Copy entrypoint.sh script to /scripts/
COPY entrypoint.sh /scripts/

# Make the entrypoint.sh script executable
RUN chmod +x /scripts/entrypoint.sh

# Create directories for media, static, and staticfiles
RUN mkdir -p /vol/web/media /vol/web/static /vol/web/staticfiles

# Create a non-root user
RUN adduser -D user

# Set ownership and permissions for /vol directory
RUN chown -R user:user /vol
RUN chmod -R 755 /vol/web

# Switch to the non-root user
USER user

# Set the default command to run the entrypoint.sh script
CMD ["/scripts/entrypoint.sh"]
