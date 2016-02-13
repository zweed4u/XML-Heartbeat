import urllib, time, tweepy, socket, sys, StringIO, gzip, zlib, json, os
import urllib2 as net
from time import gmtime, strftime
from xml.dom import minidom
from tweepy.auth import OAuthHandler
from datetime import datetime
from dateutil import tz

'''Twitter integration'''
#enter the corresponding information from your Twitter application:
CONSUMER_KEY = ''#keep the quotes, replace this with your consumer key
CONSUMER_SECRET = ''#keep the quotes, replace this with your consumer secret key
ACCESS_KEY = ''#keep the quotes, replace this with your access token
ACCESS_SECRET = ''#keep the quotes, replace this with your access token secret
auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

print 'Store?\n1.) Yeezy\n2.) Kith\n3.) BDGA\n4.) CNCPTS\n5.) Oneness\n6.) BlendsUS\n7.) liveStock CA\n8.) Yeezus\n9.) CNCPTS INTL\n10.) JustDon\n11.) NiceKicks\n12.) Xhibition\n13.) TLOP\n14.) OVO\n\nPlease enter a number: ' 

store = raw_input('')
print ""
if store=="1":
	url='http://shop.yeezysupply.com/sitemap_products_1.xml?from=1&to=9999999999'
	storeName='YEEZY_SUPPLY'
elif store=="2":
	url='http://kithnyc.com/sitemap_products_1.xml?from=1&to=9999999999'
	storeName='KITH'
elif store=="3":
	url='http://shop.bdgastore.com/sitemap_products_1.xml?from=1&to=9999999999'
	storeName='BDGA'
elif store=="4":
	url='http://shop.cncpts.com/sitemap_products_1.xml?from=1&to=9999999999'
	storeName='CNCPTS'
elif store=="5":
	url='http://oneness287.com/sitemap_products_1.xml?from=1&to=9999999999'
	storeName='ONENESS'
	#Cloudflare used! Need to set headers
	headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:43.0) Gecko/20100101 Firefox/43.0',}
	req = net.Request(url, headers=headers)
elif store=="6":
	storeName='BLENDSUS'
	url="http://www.blendsus.com/sitemap_products_1.xml?from=1&to=9999999999"
elif store=="7":
	storeName='LIVEstockCA'
	url="http://www.deadstock.ca/sitemap_products_1.xml?from=1&to=9999999999"
elif store=="8":
	storeName='YEEZUS_MERCH'
	url="http://yeezusmerch.com/sitemap_products_1.xml?from=1&to=9999999999"
elif store=="9":
	storeName='CNCPTS_INTL'
	url="http://cncptsintl.com/sitemap_products_1.xml?from=1&to=9999999999"
elif store=="10":
	storeName='JustDon'
	url="http://justdon.com/sitemap_products_1.xml?from=1&to=9999999999"
elif store=="11":
	storeName='NiceKicks'
	url='http://shopnicekicks.com/sitemap_products_1.xml?from=1&to=9999999999'
elif store=="12":
	storeName='Xhibition'
	url='http://www.xhibition.co/sitemap_products_1.xml?from=1&to=9999999999'
elif store=="13":
	storeName='TLOP'
	url='http://kanye-west-tlop.myshopify.com/sitemap_products_1.xml?from=1&to=9999999999'
elif store=="14":
	storeName='OVO'
	url='http://www.octobersveryown.com/sitemap.xml'
else:
	print "Rerun and enter one of the listed numbers above..."
	sys.exit()

print 'Timeout in seconds? (Polling)\n\nPlease enter a number: ' 
timeoutSec = raw_input('')
sleepTime=int(timeoutSec)
print '\n'

def UTCtoEST():
	zulu=strftime("%Y-%m-%d %H:%M:%S", gmtime())
	from_zone = tz.gettz('UTC')
	to_zone = tz.gettz('America/New_York')
	utc=datetime.strptime(zulu, "%Y-%m-%d %H:%M:%S")
	utc = utc.replace(tzinfo=from_zone)
	eastern = utc.astimezone(to_zone)
	return str(eastern) + ' EST'

empty=0
def main():
	global empty
	socket.setdefaulttimeout(sleepTime)
	primList=[]
	secList=[]
	try:
		if store=="5":
			xml = net.urlopen(req).read()
		else:
			xml = urllib.urlopen(url).read()
	except socket.timeout:
		print '\ntimeout reading url on first pass\n'
	if xml=='':

		print UTCtoEST() +' :: '+storeName+' :: Empty sitemap'
		empty=1
		time.sleep(sleepTime)
		main();

	if '\x1f' in xml:						
		xml=zlib.decompress(bytes(bytearray(xml)),15+32)

	xmldoc = minidom.parseString(xml)
	loc_values = xmldoc.getElementsByTagName('loc')

	if empty==1:
		primList=[]
		secList=[]
		empty=0
	else:
		for loc_val in loc_values:
				item=(loc_val.firstChild.nodeValue)
				primList.append(item)
		for i in primList:
				secList.append(i)
	while len(secList)==len(primList):
		print UTCtoEST()+' :: '+storeName+' :: '+str(len(secList)) +' items indexed...'
		secList=[]
		try:
			if store=="5":
				xml = net.urlopen(req).read()
			else:
				xml = urllib.urlopen(url).read()
				if '\x1f' in xml:
					xml=zlib.decompress(bytes(bytearray(xml)),15+32)
		except IOError:
			print '\ntimeout reading url for second array - going on (using previous pass of xml)\n'
		if xml=='':
			print UTCtoEST()+' :: '+str(len(secList)) +' :: sitemap went empty...'
			#Went from parsable xml to empty xml - 
			#len(secList) should == 0
			#set timeout and on exception trigger tone to quell 'ERROR posting tweet'
			#except tweepy.TweepError as e:
    			#	print e.message[0]['message']
			api.update_status(status=UTCtoEST()+' :: ' + 'site offline @'+url.split('sitemap')[0])
			main();#return to top

		xmldoc = minidom.parseString(xml)
		loc_values = xmldoc.getElementsByTagName('loc')
		for loc_val in loc_values:
				item=(loc_val.firstChild.nodeValue)
				secList.append(item)
		time.sleep(sleepTime)

	primList=[x.encode('UTF8') for x in primList]
	#print "\n".join(s for s in primList if 'fieg' in s)
	secList=[x.encode('UTF8') for x in secList]

	if len(primList)>len(secList):
		print '\n'+UTCtoEST()
		removedLinks=list(set(primList) - set(secList))
		print str(len(primList)-len(secList)) + ' items removed=>'
		print "\n".join(removedLinks)
		for j in removedLinks:
			try:
				api.update_status(status=UTCtoEST()+' :: ' + 'REMOVED @'+j)
			except tweepy.TweepError as e:
    				print e.message[0]['message']
				print 'Error in posting tweet'
				#os.system('play --no-show-progress --null --channels 1 synth %s sine %f' % ( 2, 200))
				'''
				if e.message[0]['code']==186:
					#code for more than 140 char
					tweet=UTCtoEST()+' :: ' + 'REMOVED @'+j
					truncTweet=(tweet[:140])
					sendTrunc=raw_input('Send abbrev. tweet?\n"'+truncTweet+'" (y/n): ')
					if sendTrunc=='y':
						api.update_status(status=truncTweet)
					else:
						print 'Skipping tweet'
				'''
				continue
		main();

	elif len(secList)>len(primList):
		print '\n'+UTCtoEST()
		newLinks=list(set(secList) - set(primList))

		for i in newLinks:
			print i
			try:
				api.update_status(status=UTCtoEST()+' :: ' + '@'+i)
			except tweepy.TweepError as e:
    				print e.message[0]['message']
				print 'ERROR posting tweet'
				#os.system('play --no-show-progress --null --channels 1 synth %s sine %f' % ( 2, 200))
				'''
				if e.message[0]['code']==186:
					#code for more than 140 char
					tweet=UTCtoEST()+' :: ' + '@'+i
					#truncTweet=(tweet[:140])
					truncTweet=i
					sendTrunc=raw_input('Send abbrev. tweet?\n"'+truncTweet+'" (y/n): ')
					if sendTrunc=='y':
						api.update_status(status=truncTweet)
					else:
						print 'Skipping tweet'
				'''
				continue

		#Appending json to each new link - read json page here and fetch inven_qty/product id/size
		#Add permalink variable string url for each store to append variant to for cart links
		for link in newLinks:
			#print link
			'''ADD PROMPT FOR JSON y/n
			jsonurl=link+'.json'
			req = net.Request(jsonurl)
			#TRY HERE
			try:
				resp = net.urlopen(req)
				data = json.loads(resp.read())
				#titleOfProduct = data[u'product'][u'title']
				#numberOfSizes=len(data[u'product'][u'variants'])
				#print str(titleOfProduct)
				try:
					for sizes in data[u'product'][u'variants']:
						print '    '+str(sizes[u'title']) +' :: '+str(sizes[u'id'])#+' :: QTY: '+str(sizes[u'inventory_quantity'])
				except:
					print 'Error in parse of json dictionary. Check keys (title, id, inventory values)'
					#os.system('play --no-show-progress --null --channels 1 synth %s sine %f' % ( 2, 200))
					continue
			except:
				print 'Error in response of .json product link'
				#os.system('play --no-show-progress --null --channels 1 synth %s sine %f' % ( 2, 200))
				continue
			print '\n''
			'''
		main();
	else:
		print 'Lists are same length but broke out of while loop'
main();
