import redissave
import bd.WuManber.FindBooks
from bd.items import BdItem
class BooksPipeLine(object):
	def __init__(self):
		try:
			self.redis=redissave.Redis()
		except Exception,e:
			print "[user] error while connecting redis",e.message
		self.SearchBooks=bd.WuManber.FindBooks.FindBooks()
			
	def process_item(self,item,spider):
		string=item['tresponse']
		for text in string:
			SearchResult=self.SearchBooks.SearchBooks(text)
			#print "[user] search result",SearchResult
			for book in SearchResult[0].keys():#WuManber
				self.redis.add_ref(book,item['turl'],SearchResult[0][book])
			for book in SearchResult[1].keys():#Kmp
				self.redis.add_ref(book,item['turl'],SearchResult[1][book])
		return item
	