if __name__ == '__main__':
    import sys
    sys.path.append('../')
import os, hashlib, time, traceback
from pprint            import pprint
from datetime          import datetime
from lib.es.elastic    import Elastic
from lib.MyGoPen_tools import get_MyGoPen_article_list, format_api_rsp
from lib.email_sender  import GmailSender
from lib.line_notify   import LineNotifyManager
from settings.environment import app

lnm = LineNotifyManager(app.config['LINE_NOTIFY_TOKEN'])

def mygopen_crawler_func():
    script_name = os.path.basename(__file__)
    try:
        es = Elastic(host=[app.config['ES_SETTING']['CONNECTION']['HOST']], 
                port=app.config['ES_SETTING']['CONNECTION']['PORT'], 
                username=app.config['ES_SETTING']['CONNECTION']['ACCOUNT'],
                password=app.config['ES_SETTING']['CONNECTION']['PASSWORD'])

        if not es.check_index_exist(app.config['ES_SETTING']['INDEX_INFO']['ARTICLE']['INDEX_NAME']):
            es.create_index(app.config['ES_SETTING']['INDEX_INFO']['ARTICLE']['INDEX_NAME'], app.config['ES_SETTING']['INDEX_INFO']['ARTICLE']['MAPPING_FILEPATH'])
        if not es.check_index_exist(app.config['ES_SETTING']['INDEX_INFO']['MEDIA']['INDEX_NAME']):
            es.create_index(app.config['ES_SETTING']['INDEX_INFO']['MEDIA']['INDEX_NAME'], app.config['ES_SETTING']['INDEX_INFO']['MEDIA']['MAPPING_FILEPATH'])

        query = {
            'from' : 0, 
            'size' : 1,
            "sort" : [
                { "article_publish_time" : "desc" }
            ]
        }

        es_dictionary_list = es.search(query, app.config['ES_SETTING']['INDEX_INFO']['ARTICLE']['INDEX_NAME'])['hits']['hits']
        es_newest_article_time = None if not es_dictionary_list else datetime.strptime(es_dictionary_list[0]['_source']['article_publish_time'], '%Y-%m-%d %H:%M:%S')
        offset_n = 0
        limit_n = 10

        finish_status = False
        while not finish_status:
            print('爬取 MyGoPen Web 中, offset_n: {}'.format(offset_n))
            article_list = get_MyGoPen_article_list(offset_n, limit_n)
            offset_n+=limit_n
            if not article_list:
                break

            for article_dict_index, article_dict in enumerate(article_list):
                print('爬取 MyGoPen Web 中，offset_n: {}, {}/{}'.format(offset_n, article_dict_index, len(article_list)))
                dictionary = format_api_rsp(article_dict, es)
                if es_newest_article_time and datetime.strptime(dictionary['article_publish_time'], '%Y-%m-%d %H:%M:%S')<=es_newest_article_time:
                    finish_status = True
                    break
                if not dictionary['article_url']:
                    pprint(dictionary)
                    print('無法透過API取得文章網址')
                    continue
                dictionary['_type'] = '_doc'
                dictionary['_index'] = app.config['ES_SETTING']['INDEX_INFO']['ARTICLE']['INDEX_NAME']
                m = hashlib.md5()
                m.update(dictionary['article_url'].encode("utf-8"))
                dictionary['_id'] = m.hexdigest()
                es.batch_load([dictionary])
    except Exception as e:
        error_msg = '\n'.join(
            [
                '{}'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
                '{}'.format(traceback.format_exc())
            ]
        )
        print(error_msg)
        lnm.send_msg(error_msg)
        gs = GmailSender(
            'MyGoPen排程出現錯誤-{}'.format(script_name),
            app.config['GOOGLE_SENDER_CONF']['RECEIVER_LIST'],
            error_msg
            )
        gs.send_email()

if __name__ == "__main__":
    mygopen_crawler_func()