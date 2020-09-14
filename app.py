from queries import get_count, get_intent_score

from datetime import datetime, timedelta
import time

import numpy as np
import pandas as pd

from elasticsearch import Elasticsearch
import json, requests

fields = ["Informational","Transactional","Commercial"]

elastic_client = Elasticsearch(['http://18.130.251.121/'])

default_higher_limit = datetime.now()
default_lower_limit = default_higher_limit - timedelta(days=30)

def get_bucket_aggregate(higher_limit = default_higher_limit, lower_limit = default_lower_limit):
    # print(higher_limit, lower_limit)

    higher_limit_unix = int(time.mktime(higher_limit.timetuple())*1000)
    lower_limit_unix = int(time.mktime(lower_limit.timetuple())*1000)

    # print(higher_limit_unix,lower_limit_unix)

    get_count["query"]["bool"]["must"][3]["range"]['@timestamp']['gte'] = lower_limit_unix
    get_count["query"]["bool"]["must"][3]["range"]['@timestamp']['lte'] = higher_limit_unix

    response = elastic_client.search(index="logstash-*", body=get_count)

    doc_count = response['hits']['total']
    print("Doc Count", doc_count)
    row_buckets = response['aggregations']["3"]["buckets"]

    result = dict()
    result_df = pd.DataFrame()

    main_cat = list()
    sub1 = []
    sub2 = []
    sub3 = []

    doc_count_list = list()
    uniq_count_list = list()


    for ag in row_buckets:
        key = ag["key"]
        key_list = key.split("/")

        main_cat.append(key_list[0])

        try:
            sub1.append(key_list[1])
        except:
            sub1.append("")

        
        try:
            sub2.append(key_list[2])
        except:
            sub2.append("")

        
        try:
            sub3.append(key_list[3])
        except:
            sub3.append("")

        doc_count_list.append(ag["doc_count"])
        uniq_count_list.append(ag["1"]["value"])
        result[ag["key"]] = {"doc_count" : ag["doc_count"] ,  "unique_count" : ag["1"]["value"]}

    result_df["Categories"] = main_cat
    result_df["Sub1"] = sub1
    result_df["Sub2"] = sub2
    result_df["Sub3"] = sub3
    result_df["Doc_count"] = doc_count_list
    result_df["Unique_count"] = uniq_count_list

    for f in fields:
        field = "categories.intents.{}".format(f)

        get_intent_score["aggs"]["2"]["aggs"]["3"]["range"]["field"] = field
        get_intent_score["query"]["bool"]["must"][3]["range"]['@timestamp']['gte'] = lower_limit_unix
        get_intent_score["query"]["bool"]["must"][3]["range"]['@timestamp']['lte'] = higher_limit_unix

        response = elastic_client.search(index="logstash-*", body=get_intent_score)


        row_buckets = response['aggregations']["2"]["buckets"]
        # print(row_buckets)

        temp1 = list()
        temp2 = list()
        temp3 = list()
        temp4 = list()

        for ag in row_buckets:
            key = ag["key"]
            val = ag["3"]["buckets"]
            tmp = {}

            temp1.append(val["0.0-25.0"]["doc_count"])
            temp2.append(val["25.0-50.0"]["doc_count"])
            temp3.append(val["50.0-75.0"]["doc_count"])
            temp4.append(val["75.0-101.0"]["doc_count"])


            for k in val.keys():
                tmp[k] = val[k]["doc_count"]
            
            result[key][f] = tmp 

        result_df["{}_0-25".format(f)] = temp1
        result_df["{}_25-50".format(f)] = temp2
        result_df["{}_50-75".format(f)] = temp3
        result_df["{}_75-100".format(f)] = temp4
    
    # print(result_df)
    file_name = "es_result_{}_{}.csv".format(lower_limit_unix,higher_limit_unix)
    result_df.to_csv(file_name, encoding='utf-8')

    result = json.dumps(result, ensure_ascii=False).encode('utf8')
    result = json.loads(result)

    return result,file_name