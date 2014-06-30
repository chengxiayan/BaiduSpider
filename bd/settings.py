# Scrapy settings for bd project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#
#from scrapy.dupefilter import BaseDupeFilter as bfilter
import bd.PipeLine.BooksPipeLine
BOT_NAME = 'bd'

SPIDER_MODULES = ['bd.spiders']
NEWSPIDER_MODULE = 'bd.spiders'

ITEM_PIPELINES={
	'bd.PipeLine.BooksPipeLine.BooksPipeLine':300
}
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'bd (+http://www.yourdomain.com)'
COOKIES_ENABLED= True
#DUPEFILTER_CLASS= bfilter