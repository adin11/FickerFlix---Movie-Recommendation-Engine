# Use official Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies (git-lfs required if building with .git context)
RUN apt-get update && \
    apt-get install -y git git-lfs && \
    git lfs install

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all app files (including .csv and .npz files)
COPY . .

# Expose Streamlit default port (Railway will override this with $PORT)
EXPOSE 7860

# Streamlit environment settings
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_SERVER_ENABLECORS=false

# Start the Streamlit app using Railway's dynamic port
CMD ["sh", "-c", "streamlit run app.py --server.port=${PORT:-7860}"]
