import redis
import exception
class Redis(object):
    host="172.20.250.251"
    port=9999
    db=1
    def __init__(self):
        self.rconn=redis.Redis(host=self.host,port=self.port,db=self.db)
        if self.rconn is None:
            raise exception.MyException("connect redis error")
        self.rconn.incr("refid",1)
    def add_ref(self,bookname,url,num):
        refid=self.rconn.get("refid")
        strref="ref:"+refid
        self.rconn.hmset(strref,{"url":url,"refnum":num})
        self.rconn.rpush(bookname,strref)
        print "[user]push book",bookname
        self.rconn.incr("refid",1)
        
    def get_refs(self,bookname):
        result=[]
        refs=self.rconn.lrange(bookname,0,-1)
        for item in refs:
            url=self.rconn.hget(item,"url")
            num=self.rconn.hget(item,"refnum")
            result.append([url,num])
        return result