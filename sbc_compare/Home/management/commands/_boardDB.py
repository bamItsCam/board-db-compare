from lxml import html
from datetime import datetime
import requests
from collections import defaultdict
from collections import OrderedDict
import time # for using delays in testing

# Note: The cache-concept implemented below now serves a different purpose than intended under django.
# Instead, it allows the same data to be used for both the product names as well as the attributes

class boardDB(object):
    HIGHEST_KNOWN_PRODUCT_NUMBER = 156
    CACHE_CHECK_PERIOD_HRS = 24
    
    # Public
    def __init__(self):
        print "init"
        self.productNamesCache = defaultdict(dict)
        self.productCache = defaultdict(dict)
        self.previousCacheTimestamp = None
    
    def getProductNames(self):
        productNamesDictionary = defaultdict(dict)
        allProducts = self._getProducts()
        productNamesDictionary.fromkeys(allProducts.keys(), None)
        
        for key, value in allProducts.iteritems():
            productNamesDictionary[key] = value['Name']            
        
        # I think we'd like the products to be in the same order every time they're shown
        self.productNamesCache = OrderedDict(sorted(productNamesDictionary.items()))
        
        return self.productNamesCache

    def getAttributes(self, productNumber):
        # given a protuct, return a dict of its attributes
        attributeDictionary = defaultdict(dict)
        allProducts = self._getProducts()
        attributeDictionary = allProducts.get(productNumber, {'Name': 'Invalid ID'})
        return attributeDictionary
        
    
    # Private
    def _getProducts(self):
        # Note: This function handles all the caching timestamp checks 
        currentTimestamp = datetime.utcnow()

        # initialization: if unknown when cache was last updated, update
        if( self.previousCacheTimestamp == None ):
            self._updateProductCache()
            
        # cache already exists: check if outdated w/ timestamp comp
        else:
            timeSinceLastCacheUpdate = currentTimestamp - self.previousCacheTimestamp
            print "Time since last cache update: " + str(timeSinceLastCacheUpdate)
            
            if( timeSinceLastCacheUpdate.total_seconds() > self.CACHE_CHECK_PERIOD_HRS * 3600 ):
                self._updateProductCache()
                
        return self.productCache
    
    def _updateProductCache(self):
        print "updateproductCache"
        self.productCache = self._getProductsSource()
        self.previousCacheTimestamp = datetime.utcnow()
    
    def _cleanProductAttributes( self, attribDict):
        # Remove unwanted entries
        if( 'Board name' in attribDict ):
            del attribDict['Board name']

        # merge 'usb otg port' and 'usb otg' entries, we will use the 'usb otg port' as the otg attribute key
        # case 1, 'usb otg port' dne, 'usb otg' dne: do nothing 
        # case 2, 'usb otg port' exists, 'usb otg' dne: do nothing
        # case 3, both exist: erase 'usb otg'
        if( 'usb otg port' in attribDict and 'usb otg' in attribDict ):
            del attribDict['usb otg']

        # case 4, 'usb otg port' dne, 'usb otg' does: copy 'usb otg' val into 'usb ogt port'
        elif( 'usb ogt port' not in attribDict and 'usb otg' in attribDict ):
            attribDict['usb ogt port'] = attribDict['usb otg']
            del attribDict['usb otg']

        return attribDict

    def _getProductsSource(self):
        print "getProductsSource"
        # Some product pages are removed, resulting in empty project pages. This bool addresses that issue
        isValidProductNumber = True
        allProductsDictionary = defaultdict(dict)
        
        # loop through each product page, getting the board name and attribute table
        productNumber = 1
        while( productNumber <= self.HIGHEST_KNOWN_PRODUCT_NUMBER or isValidProductNumber == True ):
            requestsPage = requests.get('https://www.board-db.org/product/' + str(productNumber) )
            # create the tree, replace unicode errors
            htmlTree = html.fromstring(unicode(requestsPage.content, errors='replace'))

            # Get the board name
            productName =  str(htmlTree.xpath('//div[@class="container-fluid"]/h1/text()')[0].strip())
            currentProductAttributesDict = defaultdict(dict)
            
            if( productName.lower() == 'Invalid board ID specified'.lower() ):
                isValidProductNumber = False
            else:
                isValidProductNumber = True #if a board exists beyond the HIGHEST_KNOWN_PRODUCT_NUMBER, this allows for including it
                
                # Now get the board attribute types and data
                # create list of keys (types) first
                attributesTypeList = []
                attributesTypeList =  htmlTree.xpath('//div[@class="table-responsive"]/table/tbody/tr/td[1]/text()')
                attributesTypeList = [entry.strip() for entry in attributesTypeList]
                attributesTypeList = filter(None, attributesTypeList)
                attributesTypeList.insert(0, 'Name')
                
                # then create a list of the values (data) second
                currentProductAttributesDataList = []
                currentProductAttributesDataList.insert(0, productName)    
                
                rowNumber = 1
                while( rowNumber < len(attributesTypeList) ):
                    currentAttribute =  htmlTree.xpath(u'//div[@class="table-responsive"]/table/tbody/tr[$row]/td[2]//text() | //div[@class="table-responsive"]/table/tbody/tr[$row]/td[2]/span/@class', row=rowNumber)
                    
                    # this is disgusting, don't do this
                    currentAttribute = [entry.strip().replace('Not supported', '').replace('Supported', '').replace('glyphicon glyphicon-remove icon-cell', 'No').replace('glyphicon glyphicon-ok icon-cell', 'Yes').replace('icon-cell', 'Unknown') for entry in currentAttribute]
                    
                    # get rid of empty entries due to above filtering
                    currentAttribute = filter(None, currentAttribute)
                    
                    # concatenate currentAttribute into a string (a final dict of dict of dicts would be cray, parsing will be dealt with on the front end)
                    currentAttribute = '; '.join(currentAttribute)
                    
                    currentProductAttributesDataList.append(currentAttribute)
                    rowNumber = rowNumber + 1
                
                #combine the key (types) and value (data) lists into a dict
                currentProductAttributesDict = dict(zip(attributesTypeList, currentProductAttributesDataList))

                currentProductAttributesDict = self._cleanProductAttributes(currentProductAttributesDict)
                
                allProductsDictionary[productNumber] = currentProductAttributesDict

            productNumber = productNumber + 1

        return allProductsDictionary

    def _printDict(self, dictionary):
        print "printDict"
        for key, value in dictionary.iteritems():
            print str(key) + ": " + value

def testAttributeLookup():
    boardDB.CACHE_CHECK_PERIOD_HRS = 0.0014 # change caching period to 5 seconds for testing
    boardDB.HIGHEST_KNOWN_PRODUCT_NUMBER = 156 # changed to fewer products for testing
    db = boardDB()
    db._printDict(db.getProductNames())
    db._printDict(db.getAttributes(1))

def testCacheUpdateSpeed():
    db = boardDB()
    startTime = datetime.utcnow()
    db.getProductNames()
    endTime = datetime.utcnow()
    totalTime = endTime - startTime
    print "Time since last cache update: " + str(totalTime)

            
def testProductNamesCacheDriver():
    boardDB.CACHE_CHECK_PERIOD_HRS = 0.0014 # change caching period to 5 seconds for testing
    boardDB.HIGHEST_KNOWN_PRODUCT_NUMBER = 3 # changed to fewer products for testing
    db = boardDB()
    db._printDict(db.getProductNames())
    db._printDict(db.getProductNames())
    print "starting sleep"
    time.sleep(10)
    print "stopping sleep"
    db._printDict(db.getProductNames())
    db2 = boardDB()
    db._printDict(db.getProductNames())

#testAttributeLookup()
#testCacheUpdateSpeed()
#testProductNamesCacheDriver()