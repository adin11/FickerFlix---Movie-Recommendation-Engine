# Use official Python image
FROM python:3.12

# Set working directory
WORKDIR /app

# Install git-lfs
RUN apt-get update && \
    apt-get install -y git-lfs && \
    git lfs install

# Copy all files
COPY . .

# Pull LFS files
RUN git lfs pull || echo "Not in a git repo. Skipping git lfs pull."

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port Streamlit runs on
EXPOSE 8501

# Command to run the app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
