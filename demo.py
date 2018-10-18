#encoding: utf-8
import urllib2
import urllib
import re
import uuid
import cookielib
import os

class Spider:
	generatePath = "/Users/Jian.Huang/Desktop/python/"
	cookieFile = "cookie.txt"
	keyword = ""
	def fetchResource(self,url,data):
		user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'  
		headers = { 'User-Agent' : user_agent}
		request = urllib2.Request(url,headers = headers)
		cookie = cookielib.MozillaCookieJar(Spider.cookieFile)
		handler = urllib2.HTTPCookieProcessor(cookie)
		opener = urllib2.build_opener(handler)
		response = opener.open(request,timeout=20)
		return response.read()


	def analysisContent(self,content,titlePattern,picPattern,titleFileName,picFileName):
		self.saveTitle(content,titlePattern,titleFileName)
		self.savePicUrl(content,picPattern,picFileName)



	def saveTitle(self,content,pattern,titleFileName):
		f = open(titleFileName, 'w')
		items = re.findall(pattern,content)
		for item in items:
			f.write(item[1] + '\n')
		f.close()


	def savePicUrl(self,content,pattern,picFileName):
		f = open(picFileName, 'w')
		items = re.findall(pattern,content)
		for item in items:
			f.write('https:' + item[1] + '\n')
			self.downloadPic(Spider.keyword,'https:' + item[1])
		f.close()

	def downloadPic(self,picPackageName,url):
		res = urllib.urlopen(url).read()
		path = Spider.generatePath + picPackageName	+ '/' + str(uuid.uuid1()) + ".jpg"
		f = open(path , "wb")
		f.write(res)
		f.close()

if __name__ == "__main__":
	Spider.keyword = "冰淇淋"
	path = Spider.generatePath + Spider.keyword	+ '/'
	if not os.path.exists(path):
		os.mkdir(path)
	url = "https://search.jd.com/Search?"
	values = {"keyword":Spider.keyword,"enc":"utf-8","pvid":"e58654645f294225a86a921c7964a96e"}
	data = urllib.urlencode(values)
	url =  url + data
	titleFile = path + Spider.keyword + "_title.txt"
	picFile = path + Spider.keyword + "_pic.txt"
	titlePattern = re.compile('<div class="p-name p-name-type-2">(.*?)target="_blank" title="(.*?)" href=', re.S)
	picPattern = re.compile('<div class="p-img">(.*?)source-data-lazy-img="(.*?)" />?', re.S)
	spider = Spider()
	content = spider.fetchResource(url,"")
	spider.analysisContent(content,titlePattern,picPattern,titleFile,picFile)
    