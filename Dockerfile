# Use the official Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all app files
COPY . .

# Expose the port (Railway assigns one via $PORT env variable)
EXPOSE 7860

# Set environment variable for Streamlit
ENV STREAMLIT_SERVER_PORT=$PORT
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_SERVER_ENABLECORS=false

# Run the Streamlit app
CMD ["sh", "-c", "streamlit run app.py --server.port=$PORT"]
