# Use the base image Python 3.12
FROM python:3.12

# Set the working directory
WORKDIR /app

# Copy the project files
COPY requirements.txt .
COPY entrypoint.sh .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
COPY . .

# Expose the port your application runs on
EXPOSE 8000

# Ensure entrypoint.sh is executable
RUN chmod +x entrypoint.sh

# Set the entrypoint
ENTRYPOINT ["./entrypoint.sh"]