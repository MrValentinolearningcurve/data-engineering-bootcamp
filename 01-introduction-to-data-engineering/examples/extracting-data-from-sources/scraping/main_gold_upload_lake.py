import csv
import json

import scrapy
from scrapy.crawler import CrawlerProcess
from google.cloud import storage
from google.oauth2 import service_account


URL = "https://ทองคําราคา.com/"


class MySpider(scrapy.Spider):
    name = "gold_price_spider"
    start_urls = [URL,]

    def parse(self, response):
        header = response.css("#divDaily h3::text").get().strip()
        print(header)

        table = response.css("#divDaily .pdtable")
        # print(table)

        rows = table.css("tr")
        # rows = table.xpath("//tr")
        # print(rows)

        with open("gold_prices.csv", "w") as f:
            writer = csv.writer(f)
            for row in rows:
                print(row.css("td::text").extract())
                # print(row.xpath("td//text()").extract())
                writer.writerow(row.css("td::text").extract())

        # keyfile = os.environ.get("KEYFILE_PATH")
        keyfile = "gentle-mapper-384408-ee64a189a3dc-gcs.json"
        service_account_info = json.load(open(keyfile))
        credentials = service_account.Credentials.from_service_account_info(service_account_info)
        project_id = "gentle-mapper-384408"

        storage_client = storage.Client(
            project=project_id,
            credentials=credentials,
        )
        bucket = storage_client.bucket("valen-140241")

        blob = bucket.blob("2023-05-07/gold_prices.csv")
        blob.upload_from_filename("gold_prices.csv")


if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(MySpider)
    process.start()