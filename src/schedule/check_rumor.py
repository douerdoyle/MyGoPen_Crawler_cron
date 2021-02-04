if __name__ == '__main__':
    import sys
    sys.path.append('../')
import time, traceback, json, os, requests, pandas
from datetime          import datetime, timedelta
from copy              import deepcopy
from uuid              import uuid1
from pprint            import pprint
from datetime          import datetime
from lib.es.elastic    import Elastic, ESQuery
from lib.MyGoPen_tools import check_same_process_still_running, cc
from collections       import OrderedDict
from settings.environment import app

msg_type_file_ext = {
    'image':'jpg',
    'video':'mp4',
    'audio':'m4a'
}

def check_rumor_func():
    script_name = os.path.basename(__file__)

    es = Elastic(host=['118.163.94.26'], 
            port=17377, 
            username='fakenews',
            password='dtt@fakenews')

    query_template = {
        "from":0,
        "size":1,
        "sort":[
            {
                "create_time":"asc"
            }
        ],
        "query":{
            "bool":{
                "must":[
                    {
                        "term":{
                            "source":'mygopen'
                        }
                    },
                    {
                        "exists":{
                            'field':'file'
                        }
                    },
                    {
                        "exists":{
                            'field':'message'
                        }
                    }
                ]
            }
        }
    }
    query_template['size'] = 10000
    create_time_gt_old = None
    create_time_gt = (datetime.strptime(es.search(query_template, 'fakenews@rumor_grouping')['hits']['hits'][0]['_source']['create_time'], '%Y-%m-%d %H:%M:%S') - timedelta(seconds=1)).strftime('%Y-%m-%d %H:%M:%S')
    dictionary_list_1 = []
    dictionary_list_2 = []
    while True:
        if create_time_gt_old and create_time_gt_old==create_time_gt:
            break
        print(create_time_gt)
        query = deepcopy(query_template)
        query['query']['bool']['must'].append(
            {
                "range":{
                    "create_time":{
                        "gt":create_time_gt
                    }
                }
            }
        )
        search_result = es.search(query, 'fakenews@rumor_grouping')
        if not search_result['hits']['hits']:
            break
        query['from']+=query['size']
        for data in search_result['hits']['hits']:
            dictionary = OrderedDict()
            dictionary['id'] = data['_id']
            dictionary.update(data['_source'])
            if len(dictionary['file'])==1:
                dictionary_list_1.append(dictionary)
            else:
                dictionary_list_2.append(dictionary)
        create_time_gt_old = deepcopy(create_time_gt)
        create_time_gt = datetime.strptime(es.search(query_template, 'fakenews@rumor_grouping')['hits']['hits'][-1]['_source']['create_time'], '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')

    ddddd = {
        'rumor_grouping檢查-一個檔案.xlsx':dictionary_list_1[:100],
        'rumor_grouping檢查-多個檔案.xlsx':dictionary_list_2[:100],
    }
    for excel_filename, dictionary_list in ddddd.items():
        excel_output_path = './rumor_grouping檢查-一個檔案.xlsx'
        content = json.dumps(dictionary_list_1, ensure_ascii=False, indent=4)
        tmp_json_path = 'tmp.json'
        f = open(tmp_json_path, 'w')
        f.write(content)
        f.close()
        pandas.read_json(tmp_json_path).to_excel(excel_output_path, sheet_name='rumor_grouping', index=False)
        if os.path.exists(tmp_json_path):
            os.remove(tmp_json_path)

if __name__ == "__main__":
    check_rumor_func()