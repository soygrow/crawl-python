"""
 " time : 2017-05-08
 " author : soygrow
 " function : Get stories form BaiDuTieBa
 " reference : http://cuiqingcai.com/990.html
"""
# _*_ coding:utf-8 _*_

import urllib
import urllib2
import re

class Tool:
    removeImg = re.compile('<img.*?>| {7}|')
    removeAddr = re.compile('<a.*?>|</a')
    replaceLine = re.compile('<tr>|<div>|</div>|</p>')
    replaceTD = re.compile('<td>')
    replacePara = re.compile('<p.*?>')
    replaceBR = re.compile('<br><br>|<br>')
    removeExtraTag = re.compile('<.*?>')
    br = '<br>'
    tag = '<.*?>'
    def replace(self, content):
        content = re.sub(self.removeImg, "", content)
        content = re.sub(self.removeAddr, "", content)
        content = re.sub(self.replaceLine, "\n", content)
        content = re.sub(self.replaceTD, "\t", content)
        content = re.sub(self.replaceBR, "\n    ", content)
        content = re.sub(self.removeExtraTag, "", content)
        return content

class BDTB:
    def __init__(self, seelZ):
        baseUrl = 'https://tieba.baidu.com/p/3138733512'
        self.baseUrl = baseUrl
        self.seelZ = '?see_lz=' + str(seelZ)
        self.tool = Tool()

    def getPage(self, pageNum):
        try:
            url = self.baseUrl + self.seelZ + "&pn=" + str(pageNum)
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            page = response.read().decode('utf-8')
            return page
        except urllib2.URLError, e:
            if hasattr(e, "reason"):
                print "Connect to baidu error, reason:", e.reason
                return None

    def getTitle(self, content):
        pattern = re.compile('<div.*?content clearfix.*?<h3.*?core_title_txt.*?px">(.*?)</h3>', re.S)
        result = re.search(pattern, content)
        if result:
            title = result.group(1).strip()
            return title
        else:
            return None

    def getTotalPages(self, content):
        pattern = re.compile('<li.*?l_reply_num.*?<span.*?red.*?</span>.*?<span.*?"red">(.*?)</span>')
        result = re.search(pattern, content)
        if result:
            pages = result.group(1).strip()
            return pages
        else:
            return None

    def getInfo(self, content):
        reg = '<div.*?d_author.*?<li.*?d_name.*?<a.*?p_author_name.*?>(.*?)</a>.*?</div>.*?<div id="post_content_.*?>(.*?)</div>.*?<div.*?"post-tail-wrap".*?<span.*?"tail-info">(.*?)</span>.*?<span.*?"tail-info">(.*?)</span>'
        pattern = re.compile(reg, re.S)
        print "==================="
        items = re.findall(pattern, content)
        infos = []
        for item in items:
            print item[0] + " " + item[2] + " " + item[3]
            #print item[1]
            print self.tool.replace(item[1])
            print "\n"

    def start(self):
        content = self.getPage(1)
        title = self.getTitle(content)
        print title

        pages = self.getTotalPages(content)
        print "Total pages is " + pages

        page = 1;
        print pages
        while (page <= pages):
            print pages
            print "==================BDTB page : " + str(page) + "======================"
            text = self.getPage(page)
            self.getInfo(text)

            page += 1            
        
bdtb = BDTB(1)
bdtb.start()

        
