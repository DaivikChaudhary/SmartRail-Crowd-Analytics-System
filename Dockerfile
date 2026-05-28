
# # =========================================================
# # SmartRail Production Dockerfile
# # =========================================================

# FROM python:3.11-slim

# # Prevent cache files
# ENV PYTHONDONTWRITEBYTECODE=1
# ENV PYTHONUNBUFFERED=1

# # Working directory inside container
# WORKDIR /app

# # Install system dependencies
# RUN apt-get update && apt-get install -y \
#     ffmpeg \
#     libgl1 \
#     libglib2.0-0 \
#     gcc \
#     g++ \
#     && apt-get clean

# # Copy requirements first for caching
# COPY requirements.txt .

# # Install Python dependencies
# RUN pip install --upgrade pip && \
#     pip install --default-timeout=120 --no-cache-dir -r requirements.txt

# # Copy COMPLETE project
# COPY app/ /app

# # Expose ports
# EXPOSE 8000
# EXPOSE 8501



# FROM python:3.11

# WORKDIR /app

# COPY . .

# RUN pip install --no-cache-dir -r requirements.txt

# EXPOSE 8000
# EXPOSE 8501
FROM python:3.11

WORKDIR /app

COPY requirements.txt .

RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["sh", "-c", "uvicorn run_api:app --host 0.0.0.0 --port ${PORT:-8000}"]