#Searches for key word in xml product title
#Outputs product name and corresponding url

import urllib, time
from time import gmtime, strftime
from xml.dom import minidom
url='http://shop.cncpts.com/sitemap_products_1.xml?from=1&to=9999999999'

nameList=[]
urlList=[]
xml = urllib.urlopen(url).read()
xmldoc = minidom.parseString(xml)
title_values = xmldoc.getElementsByTagName('image:title')
for title_val in title_values:
		item=(title_val.firstChild.nodeValue)
		nameList.append(item)
#unicode elements to string eements
nameList=[x.encode('UTF8') for x in nameList]
#to lower case for uniformity and easy enumerate
nameList=[x.lower() for x in nameList]

loc_values = xmldoc.getElementsByTagName('loc')
for loc_val in loc_values:
		item=(loc_val.firstChild.nodeValue)
		urlList.append(item)
urlList=[x.encode('UTF8') for x in urlList]

indicesOfName = [i for i, s in enumerate(nameList) if 'yeezy' in s]

#print indicesOfName
j=1;
for i in indicesOfName:
	print '\n'
	print str(j)+'.) '+str(nameList[i])+' :: '+str(urlList[i+1])
	j+=1
#item not in document...
#wait and refresh/loop
if len(indicesOfName)==0:
	print 'Not here...'
	
