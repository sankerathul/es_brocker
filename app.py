from queries import total_unique_count
# from responsesample import response

from datetime import datetime, timedelta
import time

import numpy as np
import pandas as pd

from elasticsearch import Elasticsearch
import json, requests

elastic_client = Elasticsearch(['http://18.130.251.121/'])

higher_limit = datetime.now()
lower_limit = higher_limit - timedelta(days=30)

print(higher_limit, lower_limit)

higher_limit_unix = int(time.mktime(higher_limit.timetuple())*1000)
lower_limit_unix = int(time.mktime(lower_limit.timetuple())*1000)

print(higher_limit_unix,lower_limit_unix)

total_unique_count["query"]["bool"]["must"][3]["range"]['@timestamp']['gte'] = lower_limit_unix
total_unique_count["query"]["bool"]["must"][3]["range"]['@timestamp']['lte'] = higher_limit_unix

response = elastic_client.search(index="logstash-*", body=total_unique_count)

doc_count = response['hits']['total']
row_aggregations = response['aggregations']
row_buckets = row_aggregations["3"]["buckets"]

result = dict()
result["count"] = list()

val = 0
for ag in row_buckets:
    temp = dict()
    temp["key"] = ag["key"]
    temp["doc_count"] = ag["doc_count"]
    temp["unique_count"] = ag["1"]["value"]
    result["count"].append(temp)

print(doc_count)
print("Bucket Count", len(row_buckets))
print(result)



