#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  8 18:12:39 2017

@author: ajinkya
"""

###### Module set up ###########
import whoosh.index as index
from whoosh.index import create_in
from whoosh.fields import *
from whoosh.analysis import StemmingAnalyzer
from whoosh import qparser, query, index
from whoosh.qparser import QueryParser
import os 
######## Defining items to index ########
schema = Schema(title = TEXT(stored = True), path =ID(stored=True),
                content=TEXT(analyzer= StemmingAnalyzer(), stored = True))
#### Intialize writer ##########
indexdir = os.path.join("/home/ajinkya/Documents/whoosh/",'indexdir')                                                                                                                                          
if not os.path.exists(indexdir): os.mkdir(indexdir)  
ix = create_in(indexdir, schema)
writer = ix.writer()
##### For parsing html files ####
from bs4 import BeautifulSoup
html1 = open("/home/ajinkya/Documents/whoosh/chatbot.html").read()
soup = BeautifulSoup(html1,"lxml")
paras_list = [item.getText() for item in soup.find_all("p")]

####### Adding items to schema ####
for i, items in enumerate (paras_list):
    writer.add_document(title = "para_{0}".format(i),
                        path = "http://example.com/page.html#item_{0}".format(i), content = items)

writer.commit()

####### Query parsing and relevent search ###
searcher = ix.searcher()
query = QueryParser("content", ix.schema, termclass = query.Variations).parse("customer", "support")
results = searcher.search(query,limit= None)
print("Found {0} results for your query \n\n".format(len(results)))
if len(results) == 0:
    print("Sorry! found no result for your query")
else :
    print("Here is the top hit: \n\n")
    print(results[0]['content'])

searcher.close()