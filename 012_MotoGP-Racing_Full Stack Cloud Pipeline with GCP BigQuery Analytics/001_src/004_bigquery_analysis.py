"""
BigQuery Analysis - Query MotoGP Data from Cloud Database

- Connecting to BigQuery
- Running SQL queries
- Loading data into pandas
- Comparing with Cloud Storage method

"""

import pandas as pd
from google.cloud import bigquery
from google.cloud import storage
from io import StringIO

# ### Configuration
PROJECT_ID= 'motogp-racing-analytics'
DATASET_ID= 'motogp_data'
TABLE_ID= 'race_results_2024'
BUCKET_NAME= 'motogp-racing-data-2024'
FILE_NAME= 'motogp_2024_results.csv'

def query_bigquery():
    """Query data from BigQuery database"""
      
    # Connect to BigQuery
    client= bigquery.Client(project= PROJECT_ID)
    print(f"Project: {client.project}")
    print()
    
    # Query 1: Count Total Races
    print("Query 1: Total Races")
    query= f"""
        SELECT COUNT(*) as total_races
        FROM {PROJECT_ID}.{DATASET_ID}.{TABLE_ID}
    """
    result= client.query(query).to_dataframe()
    print(f"Total races: {result['total_races'].iloc[0]}")
    print()
    
    # Query 2: Wins by Rider
    print("Query 2: Wins by Rider")
    query= f"""
        SELECT 
            string_field_4 as winning_rider,
            COUNT(*) as total_wins
        FROM {PROJECT_ID}.{DATASET_ID}.{TABLE_ID}
        WHERE string_field_4 IS NOT NULL
        GROUP BY string_field_4
        ORDER BY total_wins DESC
    """
    df_wins= client.query(query).to_dataframe()
    print(df_wins.to_string(index= False))
    print()
    
    # Query 3: Get all Data
    print("Query 3: Loading All Data")
    query= f"""
        SELECT * 
        FROM {PROJECT_ID}.{DATASET_ID}.{TABLE_ID}
    """
    df_bigquery= client.query(query).to_dataframe()
    print(f"Loaded {len(df_bigquery)} rows, {len(df_bigquery.columns)} columns")
    print()
    
    return df_bigquery

def load_from_storage():
    """Load data from Cloud Storage for comparison"""

    storage_client= storage.Client(project= PROJECT_ID)
    bucket= storage_client.bucket(BUCKET_NAME)
    blob= bucket.blob(FILE_NAME)
    csv_data= blob.download_as_text()
    df_storage= pd.read_csv(StringIO(csv_data))
    print(f"Loaded {len(df_storage)} rows, {len(df_storage.columns)} columns")
    print()
    
    return df_storage

def compare_methods(df_bigquery, df_storage):
    """Compare BigQuery and Cloud Storage methods"""
    
    print(f"BigQuery: {len(df_bigquery)} rows x {len(df_bigquery.columns)} columns")
    print(f"Cloud Storage: {len(df_storage)} rows x {len(df_storage.columns)} columns")
    print()
    
def main():
    """Main function"""
    
    # Query from BigQuery
    df_bigquery= query_bigquery()
    
    # Load from Cloud Storage
    df_storage= load_from_storage()
    
    # Compare methods
    compare_methods(df_bigquery, df_storage)
    
    return df_bigquery, df_storage

if __name__ == "__main__":
    df_bigquery, df_storage= main()