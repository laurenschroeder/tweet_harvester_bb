# -*- coding: utf-8 -*-
"""
Created on Sun Aug 13 21:41:19 2017

@author: schro
"""
name="Elena"
name2="Mark"
import re
test="I am kinda over Paul. #BBLIFE"
names=["Cody","Matt","Raven","Elena","Mark","Alex","Paul", "Christmas", "Josh", "Jason", "Kevin"]
for name in names:
    for name2 in names:
        if (name+" to "+name2+":") in test:
            a = re.search(".*?\:\s(.*)#.*",test) 
            print(a.group(1))
#is returning foobar['infoNeededHere']ddd