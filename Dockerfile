FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    firefox-esr \
    imagemagick \
    wget \
    xvfb \
    && rm -rf /var/lib/apt/lists/*

# Set ImageMagick policy to allow operations
RUN sed -i 's/<policy domain="path" rights="none" pattern="@\*"/<policy domain="path" rights="read|write" pattern="@*"/' /etc/ImageMagick-6/policy.xml 2>/dev/null || true

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir streamlit

# Copy the rest of the application
COPY . .

# Create necessary directories
RUN mkdir -p .mp Songs fonts

# Expose Streamlit port
EXPOSE 8501

# Default command: run the CLI
CMD ["python", "src/main.py"]
