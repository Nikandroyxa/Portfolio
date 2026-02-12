"""
Access MotoGP 2024 Race Results from Google Cloud Storage

- Connecting to Google Cloud Storage
- Accessing cloud-stored data
- Loading CSV from cloud into pandas DataFrame
"""

# ### Libraries
import pandas as pd
from google.cloud import storage
from io import StringIO

# ### Cloud Storage Configuration
BUCKET_NAME= 'motogp-racing-data-2024'
FILE_NAME= 'motogp_2024_results.csv'
PROJECT_ID= 'motogp-racing-analytics'

# ### Main function to access data from cloud
def main():
    """Main function to access and analyze MotoGP data from cloud"""
       
    # Connect to Google Cloud Storage
    client= storage.Client(project= PROJECT_ID)
    print(f"Connected to project: {client.project}")
    print()
        
    # Access the bucket
    bucket= client.bucket(BUCKET_NAME)
    print(f"Bucket accessed: {bucket.name}")
    print()
        
    # Access the blob
    blob= bucket.blob(FILE_NAME)
    print(f"File found: {blob.name}")
    print()
        
    # Download the CSV data
    csv_data= blob.download_as_text()
    print(f"Downloaded {len(csv_data)} characters")
    print()
        
    # Load into pandas DataFrame
    df= pd.read_csv(StringIO(csv_data))
    print(f"Rows: {len(df)}")
    print(f"Columns: {len(df.columns)}")
    print(f"Column names: {list(df.columns)}")
    print()
        
    # Results
    print(df.head().to_string())
    print()
        
    print(df['Winning rider'].value_counts().to_string())
    print()
        
    # Summary
    print(f"Data source: gs://{BUCKET_NAME}/{FILE_NAME}")
    print(f"Total races: {len(df)}")
    print(f"Champion: {df['Winning rider'].value_counts().index[0]}")
    print(f"Total wins: {df['Winning rider'].value_counts().iloc[0]}")
        
    return df

if __name__== "__main__":
    df= main()