import operation3
import ebay
import ast
# import random
import amazon
import urllib
import httplib
from multiprocessing import Process, Queue


categoryMap1 = {
    'Amazon Instant Video': 'Everything Else',
    'Appliances': 'Appliances',
    'Apps for Android': 'Everything Else',
    'Arts Crafts & Sewing': 'Home, Garden, Tools',
    'Automotive': 'Automotive, Industry',
    'Baby': 'Toys, Kids, Baby',
    'Beauty': 'Beauty, Health, Grocery',
    'Books': 'Books',
    'Cell Phones & Accessories': 'Electronics, Computers',
    'Clothing & Accessories': 'Clothing, Shows, Jewelry',
    'Collectibles & Fine Art': 'Collectibles',
    'Computers': 'Electronics, Computers',
    'Credit Cards': 'Everything Else',
    'Electronics': 'Electronics, Computers',
    'Gift Cards Store': 'Gift Cards',
    'Grocery & Gourmet Food': 'Beauty, Health, Grocery',
    'Health & Personal Care': 'Beauty, Health, Grocery',
    'Home & Kitchen': 'Home, Garden, Tools',
    'Industrial & Scientific': 'Automotive, Industry',
    'Jewelry': 'Clothing, Shows, Jewelry',
    'Kindle Store': 'Everything Else',
    'Magazine Subscriptions': 'Books',
    'Movies & TV': 'Movies, Music, Games',
    'MP3 Music': 'Movies, Music, Games',
    'Music': 'Movies, Music, Games',
    'Musical Instruments': 'Movies, Music, Games',
    'Office Products': 'Home, Garden, Tools',
    'Patio Lawn & Garden': 'Home, Garden, Tools',
    'Pet Supplies': 'Home, Garden, Tools',
    'Shoes': 'Home, Garden, Tools',
    'Software': 'Electronics, Computers',
    'Sports & Outdoors': 'Sports, Outdoors',
    'Tools & Home Improvement': 'Home, Garden, Tools',
    'Toys & Games': 'Toys, Kids, Baby',
    'Video Games': 'Movies, Music, Games',
    'Watches': 'Clothing, Shows, Jewelry',
    'Wine': 'Home, Garden, Tools'
    }

    
categoryMapAmazon = {
    'Amazon Instant Video': 'Everything Else',
    'Appliances': 'Appliances',
    'Apps for Android': 'Everything Else',
    'Arts Crafts & Sewing': 'Home, Garden, Tools',
    'Automotive': 'Automotive, Industry',
    'Baby': 'Toys, Kids, Baby',
    'Beauty': 'Beauty, Health, Grocery',
    'Books': 'Books',
    'Cell Phones & Accessories': 'Electronics, Computers',
    'Clothing & Accessories': 'Clothing, Shows, Jewelry',
    'Collectibles & Fine Art': 'Collectibles',
    'Computers': 'Electronics, Computers',
    'Credit Cards': 'Everything Else',
    'Electronics': 'Electronics, Computers',
    'Gift Cards Store': 'Gift Cards',
    'Grocery & Gourmet Food': 'Beauty, Health, Grocery',
    'Health & Personal Care': 'Beauty, Health, Grocery',
    'Home & Kitchen': 'Home, Garden, Tools',
    'Industrial & Scientific': 'Automotive, Industry',
    'Jewelry': 'Clothing, Shows, Jewelry',
    'Kindle Store': 'Everything Else',
    'Magazine Subscriptions': 'Books',
    'Movies & TV': 'Movies, Music, Games',
    'MP3 Music': 'Movies, Music, Games',
    'Music': 'Movies, Music, Games',
    'Musical Instruments': 'Movies, Music, Games',
    'Office Products': 'Home, Garden, Tools',
    'Patio Lawn & Garden': 'Home, Garden, Tools',
    'Pet Supplies': 'Home, Garden, Tools',
    'Shoes': 'Home, Garden, Tools',
    'Software': 'Electronics, Computers',
    'Sports & Outdoors': 'Sports, Outdoors',
    'Tools & Home Improvement': 'Home, Garden, Tools',
    'Toys & Games': 'Toys, Kids, Baby',
    'Video Games': 'Movies, Music, Games',
    'Watches': 'Clothing, Shows, Jewelry',
    'Wine': 'Home, Garden, Tools'
    }
    
    
def queryEPID(barcode):
    priceResult = {}
    try:
        if barcode:
            status, productInfoEbay = ebay.queryProduct({'barcode': barcode})
            # print productInfoEbay
            # print status
            if status:
                alertSubject = "Wetag App Algo Alert: Nonzero status returned from function ebay.queryProduct({'barcode': barcode})."
                operation3.emailalert(alertSubject, '', ['jwang6@gmail.com', 'wetag.auto@gmail.com','5104493252@tmomail.net']) 
           
            if productInfoEbay.get('recommendedItem', {}):
                priceResult['market'] = 'eBay'
                # priceResult['expectation'] = productInfoEbay['expectation']
                # priceResult['marketPriceMin'] = max(0, productInfoEbay.get('rangeLow', 0))
                # priceResult['marketPriceMax'] = productInfoEbay.get('rangeHigh', 0)
                priceResult['title'] = productInfoEbay['recommendedItem'].get('title', '')
                priceResult['imageUrl'] = productInfoEbay['recommendedItem'].get('imgUrl', '')
                priceResult['userCat'] = productInfoEbay.get('userCat', 'everything else')
                priceResult['epid']= productInfoEbay.get('epid', '')
                # if 'new' in iteminfo.get('condition', '').lower():
                    # priceresult['resellnew'] = productInfoEbay.get('resellnew', 0)
                # else:
                    # priceresult['resellused'] = productInfoEbay.get('resellused', 0)
            
            else:
                # print 'Here'
                productInfoAmazon = amazon.searchAmazon({'barcode': barcode})
                if productInfoAmazon.get('itemList'):
                    priceResult['market'] = 'Amazon'
                    priceResult['title'] = productInfoAmazon['itemList'][0].get('title', '')
                    priceResult['imageUrl'] = productInfoAmazon['itemList'][0].get('imgurl', '')
                    priceResult['userCat'] = categoryMap1.get(productInfoAmazon.get('category', ''), 'everything else')
                    priceResult['asin']= productInfoAmazon['itemList'][0].get('asin', '')
                
        
        # if 'expectation' in priceResult:
            # if priceResult['expectation'] < 0.5:
                # priceResult['expectation'] = 0.5
            # if priceResult['marketPriceMax'] < 0.5:
                # priceResult['marketPriceMax'] = 0.5
            # if priceResult['marketPriceMin']< 0:
                # priceResult['marketPriceMin'] = 0

    except Exception, e:
        print 'Error in function queryEPID(barcode)'
        print e
        #Email alert
        alertSubject = 'Wetag App Algo Alert: Error in function queryEPID(barcode)' 
        operation3.emailalert(alertSubject, e.message, ['jwang6@gmail.com', 'wetag.auto@gmail.com','5104493252@tmomail.net'])

    return priceResult
    
    
def queryEPIDMT(barcode):
    #Multithreading version
    def searchAmazon(q, itemInfo):
        q.put(amazon.searchAmazon(itemInfo))
        
    priceResult = {}
    try:
        if barcode:
            #Start the parallel process for amazon search.
            q1 = Queue()
            p = Process(target= searchAmazon, args= (q1,{'barcode': barcode})) 
            p.start()
                
            
            status, productInfoEbay = ebay.queryProduct({'barcode': barcode})
            # print productInfoEbay
            # print status
            if status:
                alertSubject = "Wetag App Algo Alert: Nonzero status returned from function ebay.queryProduct({'barcode': barcode})."
                operation3.emailalert(alertSubject, '', ['jwang6@gmail.com', 'wetag.auto@gmail.com','5104493252@tmomail.net']) 
           
            if productInfoEbay.get('recommendedItem', {}):
                priceResult['market'] = 'eBay'
                # priceResult['expectation'] = productInfoEbay['expectation']
                # priceResult['marketPriceMin'] = max(0, productInfoEbay.get('rangeLow', 0))
                # priceResult['marketPriceMax'] = productInfoEbay.get('rangeHigh', 0)
                priceResult['title'] = productInfoEbay['recommendedItem'].get('title', '')
                priceResult['imageUrl'] = productInfoEbay['recommendedItem'].get('imgUrl', '')
                priceResult['userCat'] = productInfoEbay.get('userCat', 'everything else')
                priceResult['epid']= productInfoEbay.get('epid', '')
                # if 'new' in iteminfo.get('condition', '').lower():
                    # priceresult['resellnew'] = productInfoEbay.get('resellnew', 0)
                # else:
                    # priceresult['resellused'] = productInfoEbay.get('resellused', 0)
                p.terminate()
                
            else:
                # print 'Here'
                productInfoAmazon = q1.get()
                # productInfoAmazon = amazon.searchAmazon({'barcode': barcode})
                if productInfoAmazon.get('itemList'):
                    priceResult['market'] = 'Amazon'
                    priceResult['title'] = productInfoAmazon['itemList'][0].get('title', '')
                    priceResult['imageUrl'] = productInfoAmazon['itemList'][0].get('imgurl', '')
                    priceResult['userCat'] = categoryMap1.get(productInfoAmazon.get('category', ''), 'everything else')
                    priceResult['asin']= productInfoAmazon['itemList'][0].get('asin', '')
                
            p.join()
        
        # if 'expectation' in priceResult:
            # if priceResult['expectation'] < 0.5:
                # priceResult['expectation'] = 0.5
            # if priceResult['marketPriceMax'] < 0.5:
                # priceResult['marketPriceMax'] = 0.5
            # if priceResult['marketPriceMin']< 0:
                # priceResult['marketPriceMin'] = 0

    except Exception, e:
        print 'Error in function queryEPID(barcode)'
        print e
        #Email alert
        alertSubject = 'Wetag App Algo Alert: Error in function queryEPID(barcode)' 
        operation3.emailalert(alertSubject, e.message, ['jwang6@gmail.com', 'wetag.auto@gmail.com','5104493252@tmomail.net'])

    return priceResult

    
    
def queryPriceAllCond(itemInfo):
    priceResult = {}
    
    try:
        if itemInfo:
            status, productInfoEbay = ebay.queryPriceAllCond2(itemInfo)
            # print productInfoEbay
            if status:
                alertSubject = "Wetag App Algo Alert: Nonzero status returned from function ebay.queryPriceAllCond2(itemInfo)."
                operation3.emailalert(alertSubject, '', ['jwang6@gmail.com', 'wetag.auto@gmail.com','5104493252@tmomail.net']) 
            
            # print productInfoEbay
            #If New or Old price is not available and barcode exists, try amazon.
            if ((not productInfoEbay.get('expectationNew', 0)) or (not productInfoEbay.get('expectationOld', 0))) and itemInfo.get('barcode', ''):
                productInfoAmazon = amazon.searchAmazon(itemInfo)
                # print 'Here'
                #If we cannot get userCat from ebay, get it from amazon.
                if productInfoEbay.get('userCat', ''):
                    priceResult['userCat'] = productInfoEbay['userCat']
                else:
                    priceResult['userCat'] = categoryMapAmazon.get(productInfoAmazon.get('category', ''), 'Everything Else')
          
                #If ebay does not have expectionNew
                if not productInfoEbay.get('expectationNew', 0):
                    #If amazon does have new item price.
                    if productInfoAmazon.get('pricenew', 0):
                        print productInfoAmazon.get('pricenew', 0)
                        priceResult['new'] = {}
                        priceResult['new']['expectedPrice'] = round(productInfoAmazon['pricenew']*0.7, 2)
                        priceResult['new']['marketPriceMin'] = round(productInfoAmazon['pricenew']*0.5, 2)
                        priceResult['new']['marketPriceMax'] = round(productInfoAmazon['pricenew'], 2)
                    #If amazon does not have new item price, try used and trade-in price.
                    else:  
                        priceAmazonOld = max(productInfoAmazon.get('priceused', 0), productInfoAmazon.get('pricetradein', 0))
                        priceResult['new'] = {}
                        priceResult['new']['expectedPrice'] = round(priceAmazonOld, 2)
                        priceResult['new']['marketPriceMin'] = round(priceAmazonOld*0.75, 2)
                        priceResult['new']['marketPriceMax'] = round(priceAmazonOld*1.25, 2)
                #If ebay does have expectionNew
                else:
                    priceResult['new'] = {}
                    priceResult['new']['expectedPrice'] = round(productInfoEbay.get('expectationNew', 0), 2)
                    priceResult['new']['marketPriceMin'] = round(productInfoEbay.get('rangeLowNew', 0), 2)
                    priceResult['new']['marketPriceMax'] = round(productInfoEbay.get('rangeHighNew', 0), 2)
                
                #If ebay does not have expectionOld
                if not productInfoEbay.get('expectationOld', 0):   
                    #Get amazon used item price from priceused, pricetradein or pricenew.
                    priceAmazonOld = max(productInfoAmazon.get('priceused', 0), productInfoAmazon.get('pricetradein', 0))
                    if not priceAmazonOld:
                        priceAmazonOld = productInfoAmazon.get('pricenew', 0)*0.6
                    priceResult['used'] = {}
                    priceResult['used']['expectedPrice'] = round(priceAmazonOld, 2)
                    priceResult['used']['marketPriceMin'] = round(priceAmazonOld*0.75, 2)
                    priceResult['used']['marketPriceMax'] = round(priceAmazonOld*1.25, 2)
                #If ebay does have expectionOld
                else:
                    priceResult['used'] = {}
                    priceResult['used']['expectedPrice'] = round(productInfoEbay.get('expectationOld', 0), 2)
                    priceResult['used']['marketPriceMin'] = round(productInfoEbay.get('rangeLowOld', 0), 2)
                    priceResult['used']['marketPriceMax'] = round(productInfoEbay.get('rangeHighOld', 0), 2)
                                    
            else:   #If we can get verything from ebay or there is no barcode info.   
                priceResult['userCat'] = productInfoEbay.get('userCat', 'everything else')
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
            
    except Exception, e:
        print 'Error in function querySimilarItems(itemInfo)'
        print e
        #Email alert
        alertSubject = 'Wetag App Algo Alert: Error in function queryPriceAllCond(itemInfo)' 
        operation3.emailalert(alertSubject, e.message, ['jwang6@gmail.com', 'wetag.auto@gmail.com','5104493252@tmomail.net'])

    return priceResult
    
    
    
       
def queryCategory(strQuery, format = 'short'):
    '''
    Query ebay categories from item title. Only categories with non-zero percentage are returned.
    --Input
        strQuery: <str> item title
    --Ouput
        categoryResult: <list> category long names and category numbers.
    '''
    
    categoryResult = {}
    alertSubject = ''
    alertBody = ''
    
    try:
        try:
            status, categoryList = ebay.queryCategoryAPI(strQuery)
        except Exception, e:
            print e
            status = 1
            alertBody += e.message
        if not status:
            categoryResult = [{'catNum': a[0], 'catNameLong': a[1]} for a in categoryList if a[2]]
            # ABFlag = random.randint(0,9)
            # if ABFlag < 5:
                # for cat in categoryResult:
                    # if 'Other' in cat.get('catNameLong') and cat.get('catNameLong').count('>') == 1:
                        # cat['catNameLong'] = '*'+cat.get('catNameLong')
                    # else:
                        # cat['catNameLong'] = '*'+' > '.join(cat.get('catNameLong').split(' > ')[1:])
                   # if ABFlag < 5:
            if not (format == 'long'):
                for cat in categoryResult:
                    if 'Other' in cat.get('catNameLong') and cat.get('catNameLong').count('>') == 1:
                        cat['catNameLong'] = cat.get('catNameLong')
                    else:
                        cat['catNameLong'] = ' > '.join(cat.get('catNameLong').split(' > ')[1:])
        else: #Fall back solution: web scraping
            #Email error first.
            alertSubject = 'Wetag App Algo Alert: Error in function queryCategory(strQuery) eBayAPI method'
            try:
                operation3.emailalert(alertSubject, alertBody, ['jwang6@gmail.com', 'wetag.auto@gmail.com','5104493252@tmomail.net'])   
            except:
                pass
            try:
                status, categoryList, _ = ebay.queryCategory(strQuery)
            except Exception, e:
                print e
                status = 1
                alertBody += e.message
                if not status:
                    #Repacking the categoryList into WeTag app format. Is it faster or not?
                    categoryResult = [{'catNum': a[0], 'catNameLong': ' ('.join(a[1].split(' (')[:-1])} for a in categoryList if a[2]]
                else:
                    alertSubject = 'Wetag App Algo Alert: Error in function queryCategory(strQuery) eBay web scraping method'
                    operation3.emailalert(alertSubject, alertBody, ['jwang6@gmail.com', 'wetag.auto@gmail.com','5104493252@tmomail.net'])

    except Exception, e:
        print 'Error in function queryCategory(strQuery)'
        print e
        #Email alert
        alertSubject = 'Wetag App Algo Alert: Error in function queryCategory(strQuery)' 
        operation3.emailalert(alertSubject, e.message, ['jwang6@gmail.com', 'wetag.auto@gmail.com','5104493252@tmomail.net'])
        
    return categoryResult

    
def queryCategoryMT(strQuery, format = 'short'):
    '''
    Query ebay categories from item title. Only categories with non-zero percentage are returned.
    --Input
        strQuery: <str> item title
    --Ouput
        categoryResult: <list> category long names and category numbers.
    '''
    
    
    #Multithreading version
    def categoryML(q, title):
        conn = httplib.HTTPConnection("127.0.0.1:5000")
        ms = urllib.quote_plus(title.replace('/',''))
        conn.request("GET", "/"+ms)
        r1 = conn.getresponse()
        resultStr = r1.read()
        try:
            catResult = ast.literal_eval(resultStr)
        except Exception, e:
            print 'Error in multi-thread function categoryML.'
            print title
            print e
            print resultStr
            q.put({})
        q.put(catResult)
        
        
        
    categoryResult = {}
    alertSubject = ''
    alertBody = ''
    
    try:
        
        try: #get result from offline algo.
            q1 = Queue()
            p  = Process(target= categoryML, args= (q1, strQuery))
            p.start()
        except Exception, e:
            print 'Offline category query algo error!'
            print e
            categoryListML = []
   
        try: #get result from ebay api or web scraping.
            status, categoryList = ebay.queryCategoryAPI(strQuery)
        except Exception, e:
            print e
            status = 1
            alertBody += e.message
        if not status:
            print categoryList
            categoryResult = [{'catNum': a[0], 'catNameLong': a[1], 'algoType': 1} for a in categoryList if a[2]]
            # ABFlag = random.randint(0,9)
            # if ABFlag < 5:
                # for cat in categoryResult:
                    # if 'Other' in cat.get('catNameLong') and cat.get('catNameLong').count('>') == 1:
                        # cat['catNameLong'] = '*'+cat.get('catNameLong')
                    # else:
                        # cat['catNameLong'] = '*'+' > '.join(cat.get('catNameLong').split(' > ')[1:])
                   # if ABFlag < 5:
            if not (format == 'long'):
                for cat in categoryResult:
                    if 'Other' in cat.get('catNameLong') and cat.get('catNameLong').count('>') == 1:
                        # cat['catNameLong'] = cat.get('catNameLong')
                        continue
                    else:
                        cat['catNameLong'] = ' > '.join(cat.get('catNameLong').split(' > ')[1:])
        else: #Fall back solution: web scraping
            #Email error first.
            alertSubject = 'Wetag App Algo Alert: Error in function queryCategory(strQuery) eBayAPI method'
            try:
                operation3.emailalert(alertSubject, alertBody, ['jwang6@gmail.com', 'wetag.auto@gmail.com','5104493252@tmomail.net'])   
            except: pass
            try:
                status, categoryList, _ = ebay.queryCategory(strQuery)
                print categoryList
                print status
            except Exception, e:
                print e
                status = 1
                alertBody += e.message
            if not status:
                #Repacking the categoryList into WeTag app format. Is it faster or not?
                categoryResult = [{'catNum': a[0], 'catNameLong': 'unknown > ' + ' ('.join(a[1].split(' (')[:-1]),  'algoType': 1} for a in categoryList if a[2]]
            else:
                alertSubject = 'Wetag App Algo Alert: Error in function queryCategory(strQuery) eBay web scraping method'
                try:
                    operation3.emailalert(alertSubject, alertBody, ['jwang6@gmail.com', 'wetag.auto@gmail.com','5104493252@tmomail.net'])
                except: pass
        print categoryResult         
        p.join()            
        categoryListML = q1.get()
        print categoryListML
        categoryResultML = [{'catNum': a.get('catNum', ''),  'catNameLong': a.get('catNameLong', ''),  'algoType': 0} for a in categoryListML[:3]]        
        if not (format == 'long'):
            for cat in categoryResultML:
                if 'Other' in cat.get('catNameLong') and cat.get('catNameLong').count('>') == 1:
                    # cat['catNameLong'] = cat.get('catNameLong')
                    continue
                else:
                    cat['catNameLong'] = ' > '.join(cat.get('catNameLong').split(' > ')[1:])
        categoryResultFinal = categoryResultML
        catNumList = [a.get('catNum', '') for a in categoryResultFinal]
        catNameList = [a.get('catNameLong', '') for a in categoryResultFinal]
        # print catNumList
        print categoryResult
        pos = 1
        for cat in categoryResult:
            catNum = cat.get('catNum', '').strip
            catName = cat.get('catNameLong', '') 
            if catNum in catNumList:
                matchPos = catNumList.index(catNum)
                categoryResultFinal[matchPos]['algoType'] = 2
                pos = matchPos + 2
            elif catName in catNameList:
                matchPos = catNameList.index(catName)
                categoryResultFinal[matchPos]['algoType'] = 2
                pos = matchPos + 2
            else:
                categoryResultFinal = categoryResultFinal[:pos] + [cat] + categoryResultFinal[pos:] 
                pos += 2
                if len(categoryResultFinal) == 5:
                    break
        
                    
    except Exception, e:
        print 'Error in function queryCategory(strQuery)'
        print e
        #Email alert
        alertSubject = 'Wetag App Algo Alert: Error in function queryCategory(strQuery)' 
        operation3.emailalert(alertSubject, e.message, ['jwang6@gmail.com', 'wetag.auto@gmail.com','5104493252@tmomail.net'])
        
    return categoryResultFinal
    

    
    
def querySimilarItems(itemInfo):
    itemInfo['condition'] = 'mixed' 
    itemInfo['listingStatus'] = 'sold'
    similarItems = []
    try:
        status, queryResult = ebay.queryPrice(itemInfo)
        # print queryResult.keys()
        # print queryResult.get('firstPageItems', [])[:3]
        if status:
            #Email alert
            alertSubject = 'Wetag App Algo Alert: Nonzero status returned from function ebay.queryPrice(itemInfo), sold item search.'
            operation3.emailalert(alertSubject, '', ['jwang6@gmail.com', 'wetag.auto@gmail.com','5104493252@tmomail.net']) 
            
        if not queryResult.get('firstPageItems', []):
            itemInfo['listingStatus'] = 'active'
            status, queryResult = ebay.queryPrice(itemInfo)
            if status:
                #Email alert
                alertSubject = 'Wetag App Algo Alert: Nonzero status returned from function ebay.queryPrice(itemInfo), active item search.'
                operation3.emailalert(alertSubject, '', ['jwang6@gmail.com', 'wetag.auto@gmail.com','5104493252@tmomail.net']) 
            
        for item in queryResult.get('firstPageItems', [])[:5]:
            similarItem = [{'title': item.get('title', ''),
                'url': item.get('link', ''),
                'image': item.get('imgurl', '')}]
            similarItems += similarItem
        
        
    except Exception, e:
        print 'Error in function querySimilarItems(itemInfo)'
        print e
        #Email alert
        alertSubject = 'Wetag App Algo Alert: Error in function querySimilarItems(itemInfo)' 
        operation3.emailalert(alertSubject, e.message, ['jwang6@gmail.com', 'wetag.auto@gmail.com','5104493252@tmomail.net'])
        
    return similarItems

    

        
# #This function is not used so far and commented out because it does not conforms to our alert standard.
# def listingInfo(sku):
    # listingDetails = operation3.ebayListingInfo(sku)
    # listingDetails['userCat'] = categoryMap1.get(listingDetails.get('topCatName', '').lower(), 'everything else')
    
    # return listingDetails
    