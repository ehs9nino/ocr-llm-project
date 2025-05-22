FROM python:3.12-slim

WORKDIR /app

# Install system dependencies

RUN apt-get update && apt-get install -y \
    libglib2.0-0 libsm6 libxext6 libxrender-dev libgl1 \
    gcc g++ make swig \
    && rm -rf /var/lib/apt/lists/*


# Copy dependencies and install
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy app code
COPY . .

ENV PORT=5000
EXPOSE $PORT

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
