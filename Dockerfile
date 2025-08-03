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

# Expose the default port (can be overwritten by Railway)
EXPOSE 7860

# Don't set STREAMLIT_SERVER_PORT statically — let $PORT pass through
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_SERVER_ENABLECORS=false

# Run the Streamlit app using the runtime $PORT
CMD ["sh", "-c", "streamlit run app.py --server.port=${PORT}"]
