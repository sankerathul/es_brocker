total_unique_count = {
  "aggs": {
    "3": {
      "terms": {
        "field": "row_cat_data.categories_v2.keyword",
        "size": 100000,
        "order": {
          "1": "desc"
        }
      },
      "aggs": {
        "1": {
          "cardinality": {
            "field": "user_uuid.keyword"
          }
        }
      }
    }
  },
  "size": 0,
  "_source": {
    "excludes": []
  },
  "stored_fields": [
    "*"
  ],
  "script_fields": {},
  "docvalue_fields": [
    {
      "field": "@timestamp",
      "format": "date_time"
    }
  ],
  "query": {
    "bool": {
      "must": [
        {
          "match_all": {}
        },
        {
          "match_all": {}
        },
        {
          "exists": {
            "field": "row_cat_data.categories_v2.keyword"
          }
        },
        {
          "range": {
            "@timestamp": {
              "gte": 1597131572026,
              "lte": 1599723572026,
              "format": "epoch_millis"
            }
          }
        },
        {
          "exists": {
            "field": "row_cat_data.categories_v2.keyword"
          }
        }
      ],
      "filter": [],
      "should": [],
      "must_not": []
    }
  }
}