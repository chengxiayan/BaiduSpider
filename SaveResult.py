from bd.PipeLine.redissave import Redis
pattens_file="pattens.txt"
class BookRef(object):
    def __init__(self,bookname):
        self.m_bookname=bookname
        self.m_refs={}
        
def getallresult():
    booksname=[]
    rconn=Redis()
    with open(pattens_file) as f:
        booksname=f.readlines()
    for book in booksname:
        book=book.strip(" \n")
        result=rconn.get_refs(book)
        if len(result)>0:
            print book.decode('utf-8').encode('gbk'),result
if __name__=='__main__':
    getallresult()
                
        
        