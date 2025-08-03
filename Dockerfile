# Use an official Python runtime as a base image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy all other files
COPY . .

# Expose the port Railway provides
EXPOSE 8080

# Run Streamlit using the correct port
CMD streamlit run app.py --server.port=$PORT --server.enableCORS=false
