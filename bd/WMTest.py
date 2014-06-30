#!/usr/bin/python
#-*-coding:utf-8-*-
from WuManber import WM
import os
pattens_file=open("p.txt").readlines()
for i,item in enumerate(pattens_file):
    if item[-1]=='\n':
        pattens_file[i]=item[:-1]
search_file=open("1.html").read()
s=WM.WuManber()
s.initPatten(pattens_file)
r=s.Search(search_file)
print r
for p in pattens_file:
    cnt=0
    for item in r:
        if p==item[0]:
            cnt+=1
    print "%s,%d"%((p.decode("utf-8")).encode("gbk"),cnt)