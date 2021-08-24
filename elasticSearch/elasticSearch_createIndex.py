from elasticsearch import Elasticsearch
elastic_host = {"host": "localhost", "port": 9200}
es = Elasticsearch(hosts=[elastic_host])

import json
file = open('../prettified_output.json', mode='r')
items = json.load(file)
file.close()
id_num = 1
for item in items:
    print(id_num)
    es.index(index='factchecks', doc_type='news', id=id_num, body=item, request_timeout=45)
    id_num += 1




