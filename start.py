import json

from sslverify.djangocheck import django_checker_list
from sslverify.print_stuff import print_t
from sslverify.server_model import Server

data = {}

with open('ssl_verify_config.json') as json_file:
    data = json.load(json_file)
    for e in data["ssl_check"]:
        data[e["host"]]=Server(e["host"]).__str__()
    for e in data["url_check"]:
        a= Server(e["url"])
        a.add_django_check()
        data[e["url"]]=a.__str__()
with open('ssl_verify_config.json', 'w') as f:
    json.dump(data, f)
