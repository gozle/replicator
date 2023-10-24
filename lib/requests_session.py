import requests.adapters
from django.conf import settings

# from connection.proxies.proxies import *

session = requests.Session()
adapter = requests.adapters.HTTPAdapter(pool_maxsize=50)
session.mount('http://', adapter)
session.mount('https://', adapter)
# proxy = random.choice(proxies)

# session.proxies = {
#    'http': "http://" + proxy,
#    'https': "http://" + proxy,
# }

session.headers = {
   'User-Agent': settings.USER_AGENT
}
