FROM python:3.9-slim

WORKDIR /app

# Install git and any other necessary system dependencies
RUN apt-get update && \
    apt-get install -y git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Clone the repository
RUN git clone https://github.com/abdullahalhoothy/zyte_scraper .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the canada commercial properties cron jobs
CMD ["sh", "-c", "\
    python -m cron_jobs.aquire_data.canada_commercial_properties.step1_generate_data && \
    python -m cron_jobs.aquire_data.canada_commercial_properties.step2_transform_to_csv"]

# Other steps are already scheduled in the cron_jobs_runner.py file