"""
 " time : 2017-05-04
 " author : soygrow
 " function : Get stories form QiuShiBaiKe
 " reference : http://cuiqingcai.com/990.html
"""

# coding=utf-8
import urllib
import urllib2
import cookielib
import re

class QSBK:
    def __init__(self):
        self.page_index = 1
        self.user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
        self.headers = {'User-Agent' : self.user_agent}
        self.stories = []
        self.enable = False

    # Get the indicated page information
    def getPage(self, page_index):
        try:
            url = 'http://www.qiushibaike.com/hot/page/' + str(page_index)
            request = urllib2.Request(url, headers = self.headers)
            response = urllib2.urlopen(request)
            page_code = response.read().decode('utf-8')
            return page_code

        except urllib2.URLRrror, e:
            if hasattr(e, "reason"):
                print "Connect QSBK error, reason : ", e.reason
                return None

    # Get the page info and strip the name, agree, and content
    def getPageItems(self, page_index):
        page_code = self.getPage(page_index)
        if not page_code:
            print "Load page failed."
            return None

        #pattern = re.compile('h2>(.*?)</h2.*?content">(.*?)</.*?number">(.*?)</', re.S)
        pattern = re.compile('<div.*?author.*?<h2>(.*?)</h2>.*?<div .*?content.*?<span>(.*?)</span>.*?/div>.*?<span.*?stats-vote.*?<i.*?number">(.*?)</i>', re.S)
        items = re.findall(pattern, page_code)
        #print items

        page_stories = []
        for item in items:
            text = item[1]
            haveBR = re.search("<br/>", item[1])
            if haveBR:
                replaceBR = re.compile('<br/>')
                text = re.sub(replaceBR, "\n", item[1])
            page_stories.append([item[0].strip(),text.strip(),item[2].strip()])
        return page_stories

    def loadPage(self):
        if self.enable == True:
            if len(self.stories) < 2:
                page_stories = self.getPageItems(self.page_index)
                if page_stories:
                    self.stories.append(page_stories)
                    self.page_index += 1

    # Get one story when you push Entry
    def getOneStory(self, page_stories, page):
        for story in page_stories:
            input = raw_input()
            self.loadPage()
            if input == "Q":
                self.enable = False
                return
            print u"Page : %d\tPublish : %s\tAgree : %s\n%s" %(page,story[0],story[2],story[1])

    # Start function
    def start(self):
        print "===Reading QSBK, push Entry to show a new story, Q for exit==="
        self.enable = True
        self.loadPage()
        now_page = 0
        while self.enable:
            if len(self.stories) > 0:
                page_stories = self.stories[0]
                now_page += 1
                del self.stories[0]
                self.getOneStory(page_stories, now_page)


spider = QSBK()
spider.start()
