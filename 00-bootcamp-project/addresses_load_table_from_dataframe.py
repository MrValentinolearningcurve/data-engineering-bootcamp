# Ref: https://cloud.google.com/bigquery/docs/samples/bigquery-load-table-dataframe
## import
import json
import os
from datetime import datetime

import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account

## service_account
keyfile = os.environ.get("KEYFILE_PATH") 
service_account_info = json.load(open(keyfile))
credentials = service_account.Credentials.from_service_account_info(service_account_info)
project_id = "gentle-mapper-384408"
client = bigquery.Client(
    project=project_id,
    credentials=credentials,
)


job_config = bigquery.LoadJobConfig(
    write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
    schema=[
        bigquery.SchemaField("address_id", bigquery.SqlTypeNames.STRING),
        bigquery.SchemaField("address", bigquery.SqlTypeNames.STRING),
        bigquery.SchemaField("zipcode", bigquery.SqlTypeNames.INTEGER),
        bigquery.SchemaField("state", bigquery.SqlTypeNames.STRING),
        bigquery.SchemaField("country", bigquery.SqlTypeNames.STRING),
    ]
)

file_path = "data/addresses.csv"
#df = pd.read_csv(file_path, parse_dates=["created_at", "updated_at"])
#แปลง column created_at, updated_at เป็น dated
df = pd.read_csv(file_path)
df.info()

table_id = f"{project_id}.deb_bootcamp.addresses"
job = client.load_table_from_dataframe(df, table_id, job_config=job_config)
job.result() 

table = client.get_table(table_id)
print(f"Loaded {table.num_rows} rows and {len(table.schema)} columns to {table_id}")