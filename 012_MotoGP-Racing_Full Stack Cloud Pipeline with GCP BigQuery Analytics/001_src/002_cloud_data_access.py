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

# ### Set up & Connect to Google Cloud Storage
bucket_name= 'motogp-racing-data-2024'
file_name= 'motogp_2024_results.csv'
client= storage.Client(project= 'motogp-racing-analytics')
print(f"Project: {client.project}")

# ### Access the Bucket & File
bucket= client.bucket(bucket_name)
print(f"Bucket accessed: {bucket.name}")

blob= bucket.blob(file_name)

print(f"File found: {blob.name}")
print(f"Size: {blob.size} bytes")

# ### Download CSV as text
csv= blob.download_as_text()
print(f"First 100 characters: {csv[:100]}...")

# ### Load CSV into df
df= pd.read_csv(StringIO(csv))

print(f"Rows: {len(df)}")
print(f"Columns: {len(df.columns)}")
print(f"Column names: {list(df.columns)}")
print(df.head())
print(df['Winning rider'].value_counts())




