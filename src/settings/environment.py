import os, time
from flask             import Flask
from flask_wtf.csrf    import CSRFProtect
from flask_sqlalchemy  import SQLAlchemy

app  = Flask(__name__)

class Config(object):
    DEBUG      = False
    TESTING    = False
    SECRET_KEY = ''
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED    = False
    WTF_CSRF_SSL_STRICT = False
    RUN_SETTING = {
        'host': '0.0.0.0',
        'port': 80
    }

    GOOGLE_SENDER_CONF = {
        'FROM_ADDRESS':'',
        'FROM_ADDRESS_PSW':'',
        'SMTP_SERVER':'smtp.gmail.com',
        'SMTP_PORT':'587',
    }

    ES_SETTING = {
        'CONNECTION':{
            'HOST':'',
            'PORT':9200,
            'ACCOUNT' :'',
            'PASSWORD':''
        },
        'INDEX_INFO':{
            'ARTICLE':{
                'INDEX_NAME':'',
                'MAPPING_FILEPATH':'/app/lib/es/Index_1.json'
            },
            'MEDIA':{
                'INDEX_NAME':'',
                'MAPPING_FILEPATH':'/app/lib/es/Index_2.json'
            },
        }
    }

    base_url = 'https://www.mygopen.com/'
    MYGOPEN_SETTINGS = {
        'HOST': {
            'url':base_url
        },
        'API':{
            'url':'{}feeds/posts/default/'.format(base_url), 
            'params_template':{
                'alt':'json-in-script',
                'max-results':'{}'.format(8),
                'start-index':'{}'.format(1),
                'callback':'jQuery112407998331020615_1588597963665',
                '_':'{}'.format(int(time.time()*1000))
            }
        },
        'RSS':{
            'url':'{}feeds/posts/default/'.format(base_url), 
        }
    }
    MYGOPEN_SETTINGS['HOST']['ARTICLE_LIST_TEMPLATE'] = '{}#Label1-p-{{}}'.format(MYGOPEN_SETTINGS['HOST']['url'])
    MYGOPEN_SETTINGS['RSS']['RSS_TEMPLATE'] = '{}-/{{}}'.format(MYGOPEN_SETTINGS['RSS'])
    
    FILE_EXTENSIONS = {
        'image':['jpg', 'jpeg', 'png', 'gif', 'bmp', 'heic', 'heif', 'tif', 'tiff', 'mng', 'xpm', 'psd', 'sai', 'psp', 'ufo', 'xcf', 'pcx', 'ppm', 'webp', 'pdf', 'svg'],
        'video':['webm', 'mkv', 'flv', 'flv', 'vob', 'ogv', 'ogg', 'drc', '', 'gifv', 'mng', 'avi', 'mov', 'qt', 'wmv', 'yuv', 'rm', 'rmvb', 'asf', 'amv', 'mp4,', 'm4p', 'm4v', 'mpg,', 'mp2,', 'mpeg,', 'mpe,', 'mpv', 'mpg,', 'mpeg,', 'm2v', 'm4v', 'svi', '3gp', '3g2', 'mxf', 'roq', 'nsv', 'flv', 'f4v', 'f4p', 'f4a', 'f4b']
    }

    IMAGE_FILE_EXTENSIONS = ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'heic', 'heif', 'tif', 'tiff', 'mng', 'xpm', 'psd', 'sai', 'psp', 'ufo', 'xcf', 'pcx', 'ppm', 'webp', 'pdf', 'svg']
    VIDEO_FILE_EXTENSIONS = ['webm', 'mkv', 'flv', 'flv', 'vob', 'ogv', 'ogg', 'drc', '', 'gifv', 'mng', 'avi', 'mov', 'qt', 'wmv', 'yuv', 'rm', 'rmvb', 'asf', 'amv', 'mp4,', 'm4p', 'm4v', 'mpg,', 'mp2,', 'mpeg,', 'mpe,', 'mpv', 'mpg,', 'mpeg,', 'm2v', 'm4v', 'svi', '3gp', '3g2', 'mxf', 'roq', 'nsv', 'flv', 'f4v', 'f4p', 'f4a', 'f4b']

    CALLABLE_API_SETTINGS = {
        'RUMOR_GROUPING':{}
    }

def formal_settings_154():
    app.config['ES_SETTING']['INDEX_INFO']['ARTICLE']['INDEX_NAME'] = ''

    app.config['CALLABLE_API_SETTINGS']['RUMOR_GROUPING']['BASE_URL'] = ''

def formal_settings_155():
    app.config['ES_SETTING']['INDEX_INFO']['ARTICLE']['INDEX_NAME'] = ''

    app.config['CALLABLE_API_SETTINGS']['RUMOR_GROUPING']['BASE_URL'] = ''

def formal_settings():
    app.config['GOOGLE_SENDER_CONF']['RECEIVER_LIST'] = [
        ''
    ]
    app.config['LINE_NOTIFY_TOKEN'] = ''# 不實訊息快篩平台-MyGoPen Web

    formal_init_dict = {
        '154':formal_settings_154,
        '155':formal_settings_155
    }
    formal_init_dict[os.environ['SERIAL']]()

def dev_settings():
    app.config['GOOGLE_SENDER_CONF']['RECEIVER_LIST'] = [
        '',
    ]
    app.config['LINE_NOTIFY_TOKEN'] = '' # douer-ddd

    app.config['ES_SETTING']['INDEX_INFO']['ARTICLE']['INDEX_NAME'] = ''

    app.config['CALLABLE_API_SETTINGS']['RUMOR_GROUPING']['BASE_URL'] = '' # 測試機

def general_settings():
    app.config['CALLABLE_API_SETTINGS']['RUMOR_GROUPING']['GET_GROUP_ID'] = '{}grouping/'.format(app.config['CALLABLE_API_SETTINGS']['RUMOR_GROUPING']['BASE_URL'])

app.config.from_object('settings.environment.Config')

dynamic_settings = {
    'FORMALITY':formal_settings,
    'DEV'      :dev_settings,
}
dynamic_settings[os.environ.get('API_PROPERTY')]()
general_settings()
csrf = CSRFProtect()
csrf.init_app(app)
app.url_map.strict_slashes = False

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS, GET, PATCH, DELETE, PUT')
    return(response)