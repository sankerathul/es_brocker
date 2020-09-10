from queries import total_unique_count

from datetime import datetime, timedelta
import time

import numpy as np
import pandas as pd

from elasticsearch import Elasticsearch
import json, requests

elastic_client = Elasticsearch(['http://18.130.251.121/'])

search_param = {"query": {"match_all": {}}}

response = elastic_client.search(index="logstash-*", body=search_param)

print(response)


# higher_limit = datetime.now()
# lower_limit = higher_limit - timedelta(days=30)

# # print(higher_limit)
# # print(lower_limit)

# print("UNIX")
# print(int(time.mktime(higher_limit.timetuple())*1000))
# print(int(time.mktime(lower_limit.timetuple())*1000))

# print(total_unique_count["query"]["bool"]["must"][3]["range"]['@timestamp']['gte'])
# print(total_unique_count["query"]["bool"]["must"][3]["range"]['@timestamp']['lte'])