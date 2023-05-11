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
    source_format=bigquery.SourceFormat.CSV,
    autodetect=True,
    time_partitioning=bigquery.TimePartitioning(
        type_=bigquery.TimePartitioningType.DAY,
        field="created_at",
    )
)
dt = "2021-02-10"
partition = dt.replace("-", "")
data = "events"
file_path = "data/events.csv"
with open(file_path, "rb") as f:
    table_id = f"{project_id}.deb_bootcamp.{data}"
    job = client.load_table_from_file(f, table_id, job_config=job_config)
    job.result()

table = client.get_table(table_id)
print(f"Loaded {table.num_rows} rows and {len(table.schema)} columns to {table_id}")