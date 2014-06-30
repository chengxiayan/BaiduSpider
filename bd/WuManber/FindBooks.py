#!/usr/bin/python
#-*- coding: utf-8 -*-
import WM
import kmp
#针对书名的限制,书名后面必须接以下符号或文字
def BookNameConstraint(text,index):
    MatchStart=index
    ListP=["\n"," ","，",",","。","；",";","》","（",".","好看","不错","_","挺好的","很好看"]
    #如果是文字的结尾，
    if index==len(text):
	return True
    #如果是ListP中的任意字符，由于有中文，所以只能匹配
    for item in ListP:
	for i in range(len(item)):
	    if index>=len(text) or item[i]!=text[index]:
		break
	    else:
		index+=1
	else:
	    return True
	index=MatchStart
    return False    

class FindBooks(object):
	file_patten="pattens.txt"
	wu_pattens=[]
	kmp_pattens=[]
	Wu=WM.WuManber(BookNameConstraint)
	Kmp=kmp.KmpSearch(BookNameConstraint)
	def __init__(self):
		all_pattens=open(self.file_patten).readlines()
		for i,item in enumerate(all_pattens):
			item=item.strip(" \n")
			if len(item)<5:
				self.kmp_pattens.append(item)
			else:
				self.wu_pattens.append(item)
		self.Wu.InitPatten(self.wu_pattens)
		self.Kmp.InitPattens(self.kmp_pattens)
		
	def SearchBooks(self,string):
		rWu=self.Wu.Search(string)
		rKmp=self.Kmp.Search(string)
		return [rWu,rKmp]
if __name__=='__main__':
	s=FindBooks()
	text=open("test.txt").read()
	r=s.SearchBooks(text)
	print r
		