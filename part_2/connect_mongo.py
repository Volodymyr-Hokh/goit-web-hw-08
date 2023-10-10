import configparser
import urllib.parse

from mongoengine import connect

config = configparser.ConfigParser()
r = config.read('config.ini')

mongo_user = urllib.parse.quote_plus(config.get('DB', 'user'))
mongodb_pass = urllib.parse.quote_plus(config.get('DB', 'pass'))
db_name = config.get('DB', 'db_name')
domain = config.get('DB', 'domain')
connect(host=f"""mongodb+srv://{mongo_user}:{mongodb_pass}@{domain}/{db_name}?retryWrites=true&w=majority""")
