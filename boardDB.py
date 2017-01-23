from lxml import html
from datetime import datetime
import requests
from collections import defaultdict
import time # for using delays in testing

class boardDB(object):
	HIGHEST_KNOWN_PRODUCT_NUMBER = 2
	CACHE_CHECK_PERIOD_HRS = 24
	
	# Public
	def __init__(self):
		print "init"
		self.productNamesCache = defaultdict(dict)
		self.productNamesandAttributesCache = defaultdict(dict)
		self.lastNameandAttributeCachedTimestamp = None
	
	def getProductNames(self):
		productNamesDictionary = defaultdict(dict)
		allProducts = self.getProductNamesandAttributes()
		productNamesDictionary.fromkeys(allProducts.keys(), None)
		
		for key, value in allProducts.iteritems():
			productNamesDictionary[key] = value['Name']			
		
		self.productNamesCache = productNamesDictionary
		
		return self.productNamesCache
		
	def getProductNamesandAttributes(self):
		currentTimestamp = datetime.utcnow()

		# initialization: if unknown when cache was last updated, update
		if( self.lastNameandAttributeCachedTimestamp == None ):
			self._updateProductNamesandAttributesCache()
			
		# cache already exists: check if outdated w/ timestamp
		timeSinceLastCacheUpdate = currentTimestamp - self.lastNameandAttributeCachedTimestamp
		print "Time since last cache update: " + str(timeSinceLastCacheUpdate)
		
		if( timeSinceLastCacheUpdate.total_seconds() > self.CACHE_CHECK_PERIOD_HRS * 3600 ):
			self._updateProductNamesandAttributesCache()
		
		return self.productNamesCache
		
	# Private
	def _updateProductNamesCache(self):
		print "updateProductsCache"
		self.productNamesCache = self._getProductNamesSource()
		self.lastNameCachedTimestamp = datetime.utcnow()
		
	def _getProductNamesSource(self):
		print "getProductNamesSource"
		productNamesDictionary = defaultdict(dict)
		allProducts = self._getAllProductNamesandAttributesFromSource()
		productNamesDictionary.fromkeys(allProducts.keys(), None)
		
		for key, value in allProducts.iteritems():
			productNamesDictionary[key] = value['Name']			
		
		return productNamesDictionary
	
	def _updateProductNamesandAttributesCache(self):
		print "updateProductNamesandAttributesCache"
		self.productNamesandAttributesCache = self._getAllProductNamesandAttributesFromSource()
		self.lastNameandAttributeCachedTimestamp = datetime.utcnow()
	
	def _getAllProductNamesandAttributesFromSource(self):
		print "getAllProductNamesandAttributesFromSource"
		invalidProductNumber = False
		allProductsDictionary = defaultdict(dict)
		
		# loop through each product page, getting the board name and attribute table
		productNumber = 0
		while( productNumber <= self.HIGHEST_KNOWN_PRODUCT_NUMBER or invalidProductNumber == False ):
			requestsPage = requests.get('https://www.board-db.org/product/' + str(productNumber) )
			htmlTree = html.fromstring(requestsPage.content)
			productName =  str(htmlTree.xpath('//div[@class="container-fluid"]/h1/text()')[0].strip())
			currentProductAttributesDict = defaultdict(dict)
			
			if( productName.lower() == 'Invalid board ID specified'.lower() ):
				invalidProductNumber = True
			else:
				#invalidProductNumber = False #this should be uncommented
				# create list of keys first
				currentProductAttributesTypeList = []
				currentProductAttributesTypeList =  htmlTree.xpath('//div[@class="table-responsive"]/table/tbody/tr/td[1]/text()')
				currentProductAttributesTypeList = [entry.strip() for entry in currentProductAttributesTypeList]
				currentProductAttributesTypeList = filter(None, currentProductAttributesTypeList)
				currentProductAttributesTypeList.insert(0, 'Name')
				
				# then create a list of the values second
				currentProductAttributesDataList = []
				currentProductAttributesDataList.insert(0, productName)	
				
				rowNumber = 1
				while( rowNumber < len(currentProductAttributesTypeList) ):
					currentAttribute =  htmlTree.xpath('//div[@class="table-responsive"]/table/tbody/tr[$row]/td[2]//text() | //div[@class="table-responsive"]/table/tbody/tr[$row]/td[2]/span/@style', row=rowNumber)
					
					# this is disgusting, don't do this
					currentAttribute = [entry.strip().replace('Not supported', '').replace('color: red; margin-left: 3px;', 'Not supported') for entry in currentAttribute]
					
					# get rid of empty entries due to above filtering
					currentAttribute = filter(None, currentAttribute)
					
					# concatenate currentAttribute into a string 
					currentAttribute = '; '.join(currentAttribute)
					
					currentProductAttributesDataList.append(currentAttribute)
					rowNumber = rowNumber + 1
				
				#combine two lists into one dict
				currentProductAttributesDict = dict(zip(currentProductAttributesTypeList, currentProductAttributesDataList))
				
				allProductsDictionary[productNumber] = currentProductAttributesDict

			productNumber = productNumber + 1
			
		return allProductsDictionary

	def _printDict(self, dictionary):
		print "printDict"
		for key, value in dictionary.iteritems():
			print str(key) + ": " + value


def testProductDataCacheDriver():
	db = boardDB()
	db._printDict(db.getProductNames())
			
def testProductNamesCacheDriver():
	boardDB.CACHE_CHECK_PERIOD_HRS = 0.0014 # change caching period to 5 seconds for testing
	db = boardDB()
	db._printDict(db.getProductNames())
	db._printDict(db.getProductNames())
	print "starting sleep"
	time.sleep(10)
	print "stopping sleep"
	db._printDict(db.getProductNames())
	db2 = boardDB()
	db._printDict(db.getProductNames())

testProductDataCacheDriver()	
#testProductNamesCacheDriver()