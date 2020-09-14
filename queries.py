get_count = {
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

get_intent_score = {
  "aggs": {
    "3": {
      "terms": {
        "field": "row_cat_data.categories_v2.keyword",
        "size": 100000,
        "order": {
          "_count": "desc"
        }
      },
      "aggs": {
        "5": {
          "range": {
            "field": "categories.intents.Commercial",
            "ranges": [
              {
                "from": 0,
                "to": 25
              },
              {
                "from": 25,
                "to": 50
              },
              {
                "from": 50,
                "to": 75
              },
              {
                "from": 75,
                "to": 101
              }
            ],
            "keyed": true
          },
          "aggs": {
            "6": {
              "cardinality": {
                "field": "user_uuid.keyword"
              }
            }
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
              "gte": 1597504982966,
              "lte": 1600096982966,
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