# coding:utf-8

import urllib
import urllib2
import re

import sys,os

class MMPhoto:
    def __init__(self):
        self.baseUrl = 'https://mm.taobao.com/json/request_top_list.htm?page='
        self.curPath = self.getCurrentPath()

    def getCurrentPath(self):
        path = sys.path[0]
        if os.path.isdir(path):
            return path
        elif os.path.isfile(path):
            return os.path.dirname(path)
    
    def getPage(self, page):
        url = self.baseUrl + str(page)
        #print url
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
        pattern = re.compile('<div.*?pic s60.*?<a href="(.*?)".*?<img src="(.*?)".*?</div>.*?<a.*?lady-name.*?href="(.*?)".*?>(.*?)</a>.*?<strong>(.*?)</strong>.*?<span>(.*?)</span>', re.S)
        items = re.findall(pattern, content)

        #infos = []
        #for item in items:
            #infos.append([item[0],item[1],item[2],item[3],item[4],item[5]])
            #print item[0],item[1],item[2],item[3],item[4],item[5]

        return items

    # Save img to file
    def saveImg(self, url, filename):
        #print url, filename
        u = urllib.urlopen(url)
        data = u.read()
        f = open(filename, 'wb')
        f.write(data)
        f.close()
        print "save image : " + filename + " OK"

    def saveInfo(self, content, filename):
        #print content, filename
        f = open(filename, 'wb')
        f.write(content.encode('gbk'))
        f.close()
        print "save text : " + filename + " OK"

    def saveMMImgs(self, infos):
        for item in infos:
            url = "https:" + item[1]
            path = self.curPath + "/" + item[3]
            exist = os.path.exists(path)
            #print path
            if not exist:
                os.mkdir(path)

            imgId = 0
            while True:
                filepath = path + "/" + str(imgId) + ".jpg"
                fileexist = os.path.exists(filepath)
                if not fileexist:
                    self.saveImg(url, filepath)
                    break
                imgId += 1

    def saveMMInfo(self, infos):
        for item in infos:
            path = self.curPath + "/" + item[3]
            exist = os.path.exists(path)
            if not exist:
                os.mkdir(path)

            infopath = path + "/" + item[3] + ".txt"
            mminfo = "name : " + item[3] + "\n"
            mminfo += "age : " + item[4] + "\n"
            mminfo += "location : " + item[5] + "\n"
            mminfo += "site : https:" + item[0] + "\n"
            self.saveInfo(mminfo, infopath)

    def start(self):
        print "Please input the max pages : "
        pages = raw_input()
        page = 1

        while (page <= int(pages)):
            print "=========Start crawl page : "+str(page)+"============"
            infos = self.getMMInfo(page)
            self.saveMMImgs(infos)
            self.saveMMInfo(infos)
            
            page += 1

mm = MMPhoto()
mm.start()
