import json
import os

from google.cloud import bigquery
from google.oauth2 import service_account


DATA_FOLDER = "data"

# keyfile = os.environ.get("KEYFILE_PATH")
keyfile = "gentle-mapper-384408-798d770d1940.json"
service_account_info = json.load(open(keyfile))
credentials = service_account.Credentials.from_service_account_info(service_account_info)
project_id = "gentle-mapper-384408"
client = bigquery.Client(
    project=project_id,
    credentials=credentials,
)


def load_without_partiton(data):
    job_config = bigquery.LoadJobConfig(
        skip_leading_rows=1,
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
        source_format=bigquery.SourceFormat.CSV,
        autodetect=True,
    )

    file_path = f"{DATA_FOLDER}/{data}.csv"
    with open(file_path, "rb") as f:
        table_id = f"{project_id}.deb_bootcamp.{data}"
        job = client.load_table_from_file(f, table_id, job_config=job_config)
        job.result()

    table = client.get_table(table_id)
    print(f"Loaded {table.num_rows} rows and {len(table.schema)} columns to {table_id}")

data = [
    "promos",
    "products",
    "order_items",
    "addresses"
]

for i in data:
    load_without_partiton(i)



def load_withpartition(dt, data, clustering_fields=[]):
    if clustering_fields:
        job_config = bigquery.LoadJobConfig(
            skip_leading_rows=1,
            write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
            source_format=bigquery.SourceFormat.CSV,
            autodetect=True,
            time_partitioning=bigquery.TimePartitioning(
                type_=bigquery.TimePartitioningType.DAY,
                field="created_at",
            ),
            clustering_fields=clustering_fields,
        )
    else:
        job_config = bigquery.LoadJobConfig(
            skip_leading_rows=1,
            write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
            source_format=bigquery.SourceFormat.CSV,
            autodetect=True,
            time_partitioning=bigquery.TimePartitioning(
                type_=bigquery.TimePartitioningType.DAY,
                field="created_at",
            ),
        )
    partition = dt.replace("-", "")
    file_path = f"{DATA_FOLDER}/{data}.csv"
    with open(file_path, "rb") as f:
        table_id = f"{project_id}.deb_bootcamp.{data}${partition}"
        job = client.load_table_from_file(f, table_id, job_config=job_config)
        job.result()

    table = client.get_table(table_id)
    print(f"Loaded {table.num_rows} rows and {len(table.schema)} columns to {table_id}")

load_withpartition("2020-10-23", "users", ["first_name", "last_name"])
load_withpartition("2021-02-10", "orders")
load_withpartition("2021-02-10", "events") 
