from queries import get_count, get_intent_score
# from responsesample import response1,response2

from datetime import datetime, timedelta
import time

import numpy as np
import pandas as pd

from elasticsearch import Elasticsearch
import json, requests

fields = ["Informational","Transactional","Commercial"]

elastic_client = Elasticsearch(['http://18.130.251.121/'])

higher_limit = datetime.now()
lower_limit = higher_limit - timedelta(days=30)

# print(higher_limit, lower_limit)

higher_limit_unix = int(time.mktime(higher_limit.timetuple())*1000)
lower_limit_unix = int(time.mktime(lower_limit.timetuple())*1000)

# print(higher_limit_unix,lower_limit_unix)

# get_count["query"]["bool"]["must"][3]["range"]['@timestamp']['gte'] = lower_limit_unix
# get_count["query"]["bool"]["must"][3]["range"]['@timestamp']['lte'] = higher_limit_unix

# response1 = elastic_client.search(index="logstash-*", body=get_count)

# doc_count = response1['hits']['total']
# row_buckets = response1['aggregations']["3"]["buckets"]

# result = dict()
# result = dict()

# for ag in row_buckets:
#     result[ag["key"]] = {"doc_count" : ag["doc_count"] ,  "unique_count" : ag["1"]["value"]}


for f in fields:
    field = "categories.intents.Transactional.{}".format(f)

    get_count["aggs"]["2"]["3"]["range"]["field"] = field
    get_intent_score["query"]["bool"]["must"]["range"]['@timestamp']['gte'] = lower_limit_unix
    get_intent_score["query"]["bool"]["must"]["range"]['@timestamp']['lte'] = higher_limit_unix

    response = elastic_client.search(index="logstash-*", body=get_intent_score)


    row_buckets = response['aggregations']["2"]["buckets"]
    # print(row_buckets)

    # for ag in row_buckets:
    #     key = ag["key"]
    #     val = ag["3"]["buckets"]
    #     tmp = {}
    #     for k in val.keys():
    #         tmp[k] = val[k]["doc_count"]
        
    #     result[key]["informational"] = tmp 


# print(result)