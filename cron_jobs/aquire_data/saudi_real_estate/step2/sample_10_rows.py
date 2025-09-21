import pandas as pd

# Path to the CSV file
csv_path = (
    "cron_jobs/aquire_data/saudi_real_estate/ignore/raw_saudi_real_estate.csv"
)


# Read the CSV, filter category_id = 8 and sample 50 rows
sampled_df = pd.read_csv(csv_path)
filtered_df = sampled_df[sampled_df["category_id"] == 8]
sampled_df = filtered_df.sample(n=50, random_state=42)

# Save the sampled rows to a new CSV file
output_path = "cron_jobs/aquire_data/saudi_real_estate/ignore/sampled_saudi_real_estate.csv"
sampled_df.to_csv(output_path, index=False)
