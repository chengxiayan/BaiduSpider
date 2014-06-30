#!/usr/bin/python
#-*- coding: utf-8 -*-
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.http import Request
from scrapy.http import FormRequest
from bd.items import BdItem
import cookielib
import os,re
import urllib
#http://tieba.baidu.com/f/user/passport?jumpUrl=http://tieba.baidu.com/f?kw=%D0%A1%CB%B5%CD%C6%BC%F6&pn=0&statsInfo=frs_pager#login_anchor
class BdSpider(BaseSpider):
	name="baidu"
	usrname="395318621@qq.com"
	passwd="cxy64725032425"
	usrnick="c395318621"
	allowed_domains = ['baidu.com']
	logined=False
	token=''
	curpage=0
	def __init__(self,keywords,startpage,endpage):
		#self.testurl="http://tieba.baidu.com/f?kw=%s&pn=%d"%(keywords,(startpage-1)*50)
		UrlCode=urllib.quote(keywords)
		self.testurl="http://tieba.baidu.com/f?kw=%s&pn=%d"%(UrlCode,(int(startpage)-1)*50)
		print "[user]",self.testurl
		self.startpage=int(startpage)
		self.endpage=int(endpage)
		
	def start_requests(self):
		cookiename='baidu%s.cookie'%(self.usrname)
		cj=cookielib.LWPCookieJar()
		try:
			cj.revert(cookiename)
			self.logined=True
			print "Has logined before"
		except Exception,e:
			print e
		if self.logined:
			return [Request(url=testurl,callback=self.check_page)]
		else:
			qurl="https://passport.baidu.com/v2/api/?getapi&class=login&tpl=mn&tangram=false"
			return [Request(url=qurl,callback=self.get_cookie,dont_filter=True)]
	def get_cookie(self,response):
		print "int get_cookie"
		qurl="https://passport.baidu.com/v2/api/?getapi&class=login&tpl=mn&tangram=false"
		return [Request(url=qurl,callback=self.get_tocken,dont_filter=True)]

	def get_tocken(self,response):
		print "in get_tocken"
		login_tokenStr = """bdPass.api.params.login_token='(.*?)';"""
		login_tokenObj = re.compile(login_tokenStr,re.DOTALL)
		matched_objs=login_tokenObj.findall(response.body)
		print response
		if matched_objs:
			self.token=matched_objs[0]
			print "token:",self.token
			post_data = {'username':self.usrname,
                       	'password':self.passwd,
                        'token':self.token,
                        'charset':'UTF-8',
                        'callback':'parent.bd12Pass.api.login._postCallback',
                        'index':'0',
                        'isPhone':'false',
                        'mem_pass':'on',
                        'loginType':'1',
                        'safeflg':'0',
                        'staticpage':'https://passport.baidu.com/v2Jump.html',
                        'tpl':'mn',
                        'u':self.testurl,
                        'verifycode':'',}
                #path = 'http://passport.baidu.com/?login'
        	path = 'http://passport.baidu.com/v2/api/?login'
        	headers = {
                  "Accept": "image/gif, */*",
                  "Referer": "https://passport.baidu.com/v2/?login&tpl=mn&u=%s"%(self.testurl),
                  "Accept-Language": "zh-cn",
                  "Content-Type": "application/x-www-form-urlencoded",
                  "Accept-Encoding": "gzip, deflate",
                  "User-Agent": "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727)",
                  "Host": "passport.baidu.com",
                  "Connection": "Keep-Alive",
                  "Cache-Control": "no-cache"}
        	return [FormRequest(url=path,formdata=post_data,headers=headers,callback=self.check_page) ]

	def check_page(self,response):
		print "[user]in check_page"
		#self.start_urls.append(self.testurl)
		return [Request(url=self.testurl,callback=self.parse,dont_filter=True)]

	def checkLogin(self,response):
		reUser=re.compile(self.usrnick)
		matched=reUser.findall(response.body)
		if matched is not None:
			print "[user] login baidu ok"
			return True
		else:
			print "[user] login failed"
			return False
	def parse(self,response):
		baseurl="http://tieba.baidu.com"
		if self.checkLogin(response):
			response_selector=HtmlXPathSelector(response)
			next_link=response_selector.select('//div[@id="frs_list_pager"]/a[@class="next"]/@href')
			if next_link:
				print "[user]next_link:",next_link.extract()[0]
				link=baseurl+next_link.extract()[0]
				rePage=re.compile(r'pn=(\d+)')
				print "[user]link",link
				p=rePage.findall(link)
				print "rePage",p
				if p:
					page=int(p[0])/50+1
					print "dealing with page:%d"%(page)
					#test
					if page<=self.endpage and page>=self.startpage:
						yield Request(url=link,callback=self.parse)
			tie=response_selector.select(u'//div[contains(@class,"threadlist_text threadlist_title j_th_tit  notStarList")]/a[contains(@class,"j_th_tit")]/@href')
			#print "ite",tie
			for item in tie.extract():
				print "[user]tie",item
				yield Request(url=baseurl+item,callback=self.parse_tie)
		else:
			print "[user]checklogin failed"

	def parse_tie(self,response):
		print "[user] in parse_tie"
		response_selector=HtmlXPathSelector(response)
		yield self.get_it(response)

		szPage=response_selector.select(u'//li[@class="l_reply_num"]/span[@class="red"]/text()')
		if not szPage:
			print "[user] get page num failed"
		else:
			pages=int(szPage.extract()[1])
			#test
			if pages>10:
				pages=10
			for i in range(2,pages+1):
				yield Request(url=response.url+"?pn=%d"%(i),callback=self.parse_others)

	def parse_others(self,response):
		print "[user] in parse_others"
		yield self.get_it(response)

	def get_it(self,response):
		print "[user] in get_item"
		item=BdItem()
		response_selector=HtmlXPathSelector(response)
		title=response_selector.select(u'//div[@id="j_core_title_wrap"]\
			/div[contains(@class,"core_title")]/h1/text()').extract()[0]
		if len(title)>1:
			print "[user] parse tie title failed"
		item['turl']=response.url
		item['ttitle']=title[0]
		"""
		dirRe=re.compile(r"/p/(\d+)")
		pageRe=re.compile(r"pn=(\d+)")
		dirname=dirRe.findall(response.url)[0]
		page=pageRe.findall(response.url)
		if len(page) is 0:
			page=['1']
		try:
			os.mkdir(dirname)
		except Exception as e:
			pass
		"""
		content=response_selector.select(u'//div[contains(@class,"d_post_content_main")]/div[contains(@class,"p_content_nameplate")]/cc/div/text()').extract()
		if len(content)==0:
			print "[user] get content failed."
		item['tresponse']=[]
		for text in content:
			item['tresponse'].append(text.encode("utf8"))
		return item
