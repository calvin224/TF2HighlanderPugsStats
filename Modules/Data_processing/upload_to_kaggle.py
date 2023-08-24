import os

# Directory containing your CSV files
csv_directory = r""  # Update with the directory path
dataset_slug = "kosuketf2/hlpugstats"  # Replace with your dataset slug

# Get a list of CSV files in the directory
csv_files = [os.path.join(csv_directory, f) for f in os.listdir(csv_directory) if f.endswith(".csv")]

# Create a new version of the dataset using Kaggle CLI with all CSV files
upload_command = f'kaggle datasets version -p "{csv_directory}" -m "Upload all CSV files"'
os.system(upload_command)

print("All CSV files uploaded to Kaggle.")



