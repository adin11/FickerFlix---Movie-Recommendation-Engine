# Use the official lightweight Python image.
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app/

# Install pip packages
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Expose port (Railway uses environment variable)
EXPOSE 8080

# Run streamlit and bind to 0.0.0.0 and port from env variable
CMD streamlit run app.py --server.address=0.0.0.0 --server.port=${PORT}
