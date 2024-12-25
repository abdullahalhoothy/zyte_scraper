FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the canada commercial properties cron jobs
COPY cron_jobs/aquire_data/canada_commercial_properties/ ./cron_jobs/aquire_data/canada_commercial_properties/

# Run the canada commercial properties cron jobs
CMD ["sh", "-c", "\
    python -m cron_jobs.aquire_data.canada_commercial_properties.step1_generate_data && \
    python -m cron_jobs.aquire_data.canada_commercial_properties.step2_transform_to_csv" ]
