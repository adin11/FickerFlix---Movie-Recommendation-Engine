# Use the official Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all app files (including .csv and .pkl files)
COPY . .

# Expose the default port (Railway will override it with $PORT)
EXPOSE 7860

# Streamlit settings
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_SERVER_ENABLECORS=false

# Run Streamlit on Railway's dynamic port
CMD ["sh", "-c", "streamlit run app.py --server.port=$PORT"]
