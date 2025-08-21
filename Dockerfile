FROM python:3.10

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    git \
    git-lfs \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt
WORKDIR /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Initialize git lfs and clone model
RUN git lfs install
RUN git clone https://huggingface.co/m3hrdadfi/wav2vec2-large-xlsr-persian-v3 /app/wav2vec2V3

# Copy application code
COPY . /app

# Create files directory
RUN mkdir -p /app/files

# Expose port
EXPOSE 8010

CMD ["uvicorn", "app:app", "--host=0.0.0.0", "--port=8010"]
