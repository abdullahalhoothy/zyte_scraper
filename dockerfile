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

# Set the command to run your specific module
CMD ["python", "-m", "cron_jobs.aquire_data.canada_commercial_properties.step1_generate_data"]