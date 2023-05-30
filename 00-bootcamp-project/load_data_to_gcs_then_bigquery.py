import json
import os

from google.cloud import bigquery, storage
from google.oauth2 import service_account


DATA_FOLDER = "data"
BUSINESS_DOMAIN = "greenery"
location = "asia-southeast1"

# keyfile = os.environ.get("KEYFILE_PATH")

keyfile_gcs = "gentle-mapper-384408-ee64a189a3dc-GCS.json"
service_account_info_gcs = json.load(open(keyfile_gcs))
credentials_gcs = service_account.Credentials.from_service_account_info(
    service_account_info_gcs
)

keyfile_bigquery = "gentle-mapper-384408-798d770d1940.json"
service_account_info_bigquery = json.load(open(keyfile_bigquery))
credentials_bigquery = service_account.Credentials.from_service_account_info(
    service_account_info_bigquery
)

def load_data_to_gcs_load_bigquery(data):
    project_id = "gentle-mapper-384408"
    # Load data from Local to GCS
    bucket_name = "deb-bootcamp-140241"
    storage_client = storage.Client(
        project=project_id,
        credentials=credentials_gcs,
    )
    bucket = storage_client.bucket(bucket_name)

    file_path = f"{DATA_FOLDER}/{data}.csv"
    destination_blob_name = f"{BUSINESS_DOMAIN}/{data}/{data}.csv"
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(file_path)

    # Load data from GCS to BigQuery
    bigquery_client = bigquery.Client(
        project=project_id,
        credentials=credentials_bigquery,
        location=location,
    )
    table_id = f"{project_id}.deb_bootcamp.{data}"
    job_config = bigquery.LoadJobConfig(
        skip_leading_rows=1,
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
        source_format=bigquery.SourceFormat.CSV,
        autodetect=True, # detect schema
    )
    job = bigquery_client.load_table_from_uri(
        f"gs://{bucket_name}/{destination_blob_name}",
        table_id,
        job_config=job_config,
        location=location,
    )
    job.result()

    table = bigquery_client.get_table(table_id)
    print(f"Loaded {table.num_rows} rows and {len(table.schema)} columns to {table_id}")

data = [
    "addresses",
    "order_items",
    "products",
    "promos"
]

for i in data:
    load_data_to_gcs_load_bigquery(i)