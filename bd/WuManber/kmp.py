#!/usr/bin/python
#-*-coding:utf-8-*-
def DefConstraint(text,index):
    return True

class KmpSearch(object):
    def __init__(self,ConstraintFunc=DefConstraint):
        self.m_ConstraintFunc=ConstraintFunc
    def InitPattens(self,pattens):
        self.m_pattens=pattens
        self.m_nexts=[]
        for item in pattens:
            self.m_nexts.append(self.GetNext(item))
        #print self.m_nexts
    def GetNext(self,p):
        PattensLen=len(p)
        next=[0]*(PattensLen+1)
        next[0]=-1
        for i in range(1,PattensLen+1):
            n=next[i-1]
            while n>=0 and p[n]!=p[i-1]:
                n=next[n] 
            if n<0:
                next[i]=0
            elif p[n]==p[i-1]:
                next[i]=n+1
        return next
            
    def SearchSingle(self,string,PattenIndex):
        LenString=len(string)
        j=0
        i=0
        result=0
        PattenNext=self.m_nexts[PattenIndex]
        PattenStr=self.m_pattens[PattenIndex]
        while i<LenString:
            if j<0 or string[i]==PattenStr[j]:
                i+=1
                if j>=0:
                    j+=1
                    if j==len(PattenStr):
                        if self.m_ConstraintFunc(string,i):
                            result+=1
                        j=PattenNext[j]
                else:
                    j=0
            else:
                j=PattenNext[j]
        return result
    
    def Search(self,string):
        result={}
        for i,item in enumerate(self.m_pattens):
            r=self.SearchSingle(string,i)
            if r>0:
                result[item]=r
        return result
if __name__=='__main__':
    s="""中国程夏衍程夏衍程，中国中程夏衍程"""
    p=["程夏衍程","中国中"]
    k=KmpSearch()
    k.InitPattens(p)
    r=k.Search(s)
    print r
                
                