import operation3
import ebay
# import amazon


categoryMap1 = {
    'antiques': 'Collectibles',
    'art': 'Home, Garden, Tools',
    'baby': 'Toys, Kids, Baby',
    'books': 'Books',
    'business & industrial': 'Automotive, Industry',
    'cameras & photo': 'Electronics, Computers',
    'cell phones & accessories': 'Electronics, Computers',
    'clothing, shoes & accessories': 'Clothing, Shoes, Jewelry',
    'coins & paper money': 'Collectibles',
    'collectibles': 'Collectibles',
    'computers/tablets & networking': 'Electronics, Computers',
    'consumer electronics': 'Electronics, Computers',
    'crafts': 'Home, Garden, Tools',
    'dolls & bears': 'Toys, Kids, Baby',
    'dvds & movies': 'Movies, Music, Games',
    'ebay motors': 'Automotive, Industry',
    'entertainment memorabilia': 'Collectibles',
    'gift cards & coupons': 'Gift Cards',
    'health & beauty': 'Beauty, Health, Grocery',
    'home & garden': 'Home, Garden, Tools',
    'jewelry & watches': 'Clothing, Shoes, Jewelry',
    'music': 'Movies, Music, Games',
    'musical instruments & gear': 'Movies, Music, Games',
    'pet supplies': 'Home, Garden, Tools',
    'pottery & glass': 'Home, Garden, Tools',
    'real estate': 'Everything Else',
    'specialty services': 'Everything Else',
    'sporting goods': 'Sports, Outdoors',
    'sports mem, cards & fan shop': 'Collectibles',
    'stamps': 'Collectibles',
    'tickets & experiences': 'Everything Else',
    'toys & hobbies': 'Toys, Kids, Baby',
    'travel': 'Everything Else',
    'video games & consoles': 'Movies, Music, Games',
    'everything else': 'Everything Else'
    }

    
def queryEPID(barcode):
    priceResult = {}
    if barcode:
        productInfoEbay = ebay.queryProduct({'barcode': barcode})
        # print productInfoEbay
        if productInfoEbay.get('recommendedItem', {}):
            priceResult['market'] = 'eBay'
            # priceResult['expectation'] = productInfoEbay['expectation']
            # priceResult['marketPriceMin'] = max(0, productInfoEbay.get('rangeLow', 0))
            # priceResult['marketPriceMax'] = productInfoEbay.get('rangeHigh', 0)
            priceResult['title'] = productInfoEbay['recommendedItem'].get('title', '')
            priceResult['imageUrl'] = productInfoEbay['recommendedItem'].get('imgUrl', '')
            priceResult['userCat'] = productInfoEbay.get('userCat', '')
            priceResult['epid']= productInfoEbay.get('epid', '')
            # if 'new' in iteminfo.get('condition', '').lower():
                # priceresult['resellnew'] = productInfoEbay.get('resellnew', 0)
            # else:
                # priceresult['resellused'] = productInfoEbay.get('resellused', 0)
                        
    
    # if 'expectation' in priceResult:
        # if priceResult['expectation'] < 0.5:
            # priceResult['expectation'] = 0.5
        # if priceResult['marketPriceMax'] < 0.5:
            # priceResult['marketPriceMax'] = 0.5
        # if priceResult['marketPriceMin']< 0:
            # priceResult['marketPriceMin'] = 0


    return priceResult

    
    
def queryPriceAllCond(itemInfo):
    priceResult = {}
    if itemInfo:
        productInfoEbay = ebay.queryPriceAllCond2(itemInfo)
        # print productInfoEbay
        
        priceResult['userCat'] = productInfoEbay.get('userCat', '')
        priceResult['new'] = {}
        priceResult['new']['expectedPrice'] = round(productInfoEbay.get('expectationNew', 0), 2)
        priceResult['new']['marketPriceMin'] = round(productInfoEbay.get('rangeLowNew', 0), 2)
        priceResult['new']['marketPriceMax'] = round(productInfoEbay.get('rangeHighNew', 0), 2)
        
        priceResult['used'] = {}
        priceResult['used']['expectedPrice'] = round(productInfoEbay.get('expectationOld', 0), 2)
        priceResult['used']['marketPriceMin'] = round(productInfoEbay.get('rangeLowOld', 0), 2)
        priceResult['used']['marketPriceMax'] = round(productInfoEbay.get('rangeHighOld', 0), 2)
        
        
    #Regulate price
   
        if priceResult['new']['expectedPrice'] < 0.5: priceResult['new']['expectedPrice'] = 0.5 
        if priceResult['new']['marketPriceMin'] < 0: priceResult['new']['marketPriceMin'] = 0          
        if priceResult['new']['marketPriceMax'] < 0.5: priceResult['new']['marketPriceMax'] = 0.5 
            
        if priceResult['used']['expectedPrice'] < 0.5: priceResult['used']['expectedPrice'] = 0.5 
        if priceResult['used']['marketPriceMin'] < 0: priceResult['used']['marketPriceMin'] = 0           
        if priceResult['used']['marketPriceMax'] < 0.5: priceResult['used']['marketPriceMax'] = 0.5 
            

    return priceResult

    
    
def queryCategory(strQuery):
   
    categoryResult = {}
    try:
        categoryList, _ = ebay.queryCategory(strQuery)
        print categoryList
        
        #Repacking the categoryList into WeTag app format. Is it faster or not?
        categoryResult = [{'catNum': a[0], 'catNameLong': ' ('.join(a[1].split(' (')[:-1])} for a in categoryList if a[2]]
    except Exception, e:
        print 'Error in function queryCategory(strQuery)'
        print e
        
    return categoryResult

    
    
def querySimilarItems(itemInfo):
    itemInfo['condition'] = 'mixed' 
    itemInfo['listingStatus'] = 'sold'
    similarItems = []
    try:
        queryResult = ebay.queryPrice(itemInfo)
        # print queryResult.keys()
        # print queryResult.get('firstPageItems', [])[:3]
        if not queryResult.get('firstPageItems', []):
            itemInfo['listingStatus'] = 'active'
            queryResult = ebay.queryPrice(itemInfo)
            
        for item in queryResult.get('firstPageItems', [])[:5]:
            similarItem = [{'title': item.get('title', ''),
                'url': item.get('link', ''),
                'image': item.get('imgurl', '')}]
            similarItems += similarItem
        
        
    except Exception, e:
        print 'Error in function queryCategory(strQuery)'
        print e
        
    return similarItems


# def queryPriceAllCond(itemInfo):
    # priceResult = {}
    # if itemInfo:
        # productInfoEbay = ebay.queryPriceAllCond2(itemInfo)
        # # print productInfoEbay
        
        # priceResult['userCat'] = productInfoEbay.get('userCat', '')
        # priceResult['new'] = {}
        # priceResult['new']['expectedPrice'] = round(productInfoEbay.get('expectationNew', 0), 2)
        # priceResult['new']['marketPriceMin'] = round(productInfoEbay.get('rangeLowNew', 0), 2)
        # priceResult['new']['marketPriceMax'] = round(productInfoEbay.get('rangeHighNew', 0), 2)
        
        # priceResult['used'] = {}
        # priceResult['used']['expectedPrice'] = round(productInfoEbay.get('expectationOld', 0), 2)
        # priceResult['used']['marketPriceMin'] = round(productInfoEbay.get('rangeLowOld', 0), 2)
        # priceResult['used']['marketPriceMax'] = round(productInfoEbay.get('rangeHighOld', 0), 2)
        
        
    # #Regulate price
   
        # if priceResult['new']['expectedPrice'] < 0.5: priceResult['new']['expectedPrice'] = 0.5 
        # if priceResult['new']['marketPriceMin'] < 0: priceResult['new']['marketPriceMin'] = 0          
        # if priceResult['new']['marketPriceMax'] < 0.5: priceResult['new']['marketPriceMax'] = 0.5 
            
        # if priceResult['used']['expectedPrice'] < 0.5: priceResult['used']['expectedPrice'] = 0.5 
        # if priceResult['used']['marketPriceMin'] < 0: priceResult['used']['marketPriceMin'] = 0           
        # if priceResult['used']['marketPriceMax'] < 0.5: priceResult['used']['marketPriceMax'] = 0.5 
            

    # return priceResult

        
    
def listingInfo(sku):
    listingDetails = operation3.ebayListingInfo(sku)
    listingDetails['userCat'] = categoryMap1.get(listingDetails.get('topCatName', '').lower(), '')
    
    return listingDetails
    