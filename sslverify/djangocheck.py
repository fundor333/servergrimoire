import logging

import requests

from sslverify import print_stuff

logger = logging.getLogger("CheckDjango")

pc = print_stuff.PrintColor()


def single_django_checker(url, path="/life", dict_out={"status": "alive and kicking"})->(bool,str,str,int):
    try:
        r = requests.get(url + path)
    except requests.exceptions.MissingSchema:
        r = requests.get(f"http://{url}{path}")
    if 200 <= r.status_code < 400:
        try:
            if r.json() == dict_out:
                output_strng = True, url, "", r.status_code
            else:
                output_strng = False, url, r.json()['status'], r.status_code
        except ValueError as e:
            output_strng = False, url, e, r.status_code
    else:
        output_strng = False, url, "", r.status_code
    logger.info(output_strng)
    return output_strng


def django_checker_list(servers=[{}]):
    output_array = []
    for e in servers:
        output_array.append(single_django_checker(e["url"], e.get("path", "/life"),
                                                    e.get("message_out", {"status": "alive and kicking"})))
    return output_array
