# coding:utf-8

import urllib
import urllib2
import re

class MMPhoto:
    def __init__(self):
       self.baseUrl = 'https://mm.taobao.com/json/request_top_list.htm?page='
    
    def getPage(self, page):
        url = self.baseUrl + str(page)
        print url
        try:
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            pageCode = response.read().decode('gbk')
            return pageCode
        except urllib2.URLError, e:
            if hasattr(e, "reason"):
                print "Connect taobao error, reason : ", e.reason
                return None

    def getMMInfo(self, page):
        content = self.getPage(page)
        print content
        pattern = re.compile('<div class="pic s60"><a href="(.*?)".*?<img src="(.*?)"</div>')
        items = re.findall(pattern, content)
        print items

        for item in items:
            print item[0],item[1],item[2]#,item[3]


    def start(self):
        print "Please input the max pages : "
        pages = raw_input()
        page = 1
        while (page < pages):
            print "===============Start crawl page : "+str(page)+"================"
            self.getMMInfo(page)

            page += 1
            break;

mm = MMPhoto()
mm.start()
