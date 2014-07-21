import operation3
import urllib2
import urllib
import cookielib
from lxml import etree

# userInput = {'barcode': '0818406569', 'title': 'Blackjack: Play Like The Pros', 'condition': 'Used-good'}


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
    
categoryMap2 = {
    'antiques': 'Collectibles',
    'art': 'Home, Garden, Tools',
    'baby': 'Toys, Kids, Baby',
    'books': 'Books',
    'business industrial': 'Automotive, Industry',
    'cameras photo': 'Electronics, Computers',
    'cell phones accessories': 'Electronics, Computers',
    'clothing, shoes accessories': 'Clothing, Shoes, Jewelry',
    'coins paper money': 'Collectibles',
    'collectibles': 'Collectibles',
    'computers tablets networking': 'Electronics, Computers',
    'consumer electronics': 'Electronics, Computers',
    'crafts': 'Home, Garden, Tools',
    'dolls bears': 'Toys, Kids, Baby',
    'dvds movies': 'Movies, Music, Games',
    'ebay motors': 'Automotive, Industry',
    'entertainment memorabilia': 'Collectibles',
    'gift cards coupons': 'Gift Cards',
    'health beauty': 'Beauty, Health, Grocery',
    'home garden': 'Home, Garden, Tools',
    'jewelry watches': 'Clothing, Shoes, Jewelry',
    'music': 'Movies, Music, Games',
    'musical instruments gear': 'Movies, Music, Games',
    'pet supplies': 'Home, Garden, Tools',
    'pottery glass': 'Home, Garden, Tools',
    'real estate': 'Everything Else',
    'specialty services': 'Everything Else',
    'sporting goods': 'Sports, Outdoors',
    'sports mem, cards fan shop': 'Collectibles',
    'stamps': 'Collectibles',
    'tickets experiences': 'Everything Else',
    'toys hobbies': 'Toys, Kids, Baby',
    'travel': 'Everything Else',
    'video games consoles': 'Movies, Music, Games',
    'everything else': 'Everything Else'
    }
         
    



#http://www.ebay.com/sch/i.html?_nkw=the+davinci+code&_sop=12
#&_sop=12 means best match; &LH_BIN=1 means buy it now; &LH_ItemCondition=4 means used, 3 means new; LH_PreFloc=1 means US Only
#on productised item page. ?&tabs=15 for all items. &LH_BIN=1 for buy it now
def queryProduct(itemInfo):
#search for best matched price to sell on ebay
#itemInfo is dict with keys: barcode, title, condition
#

    epInfo = {}
    
    # opener = urllib2.build_opener(urllib2.HTTPRedirectHandler)
    
    # itemInfo = {'barcode': '0818406569', 'title': 'Blackjack: Play Like The Pros', 'condition': 'Used-good'}
    # itemInfo = {'barcode': '0321611136', 'title': 'Blackjack: Play Like The Pros', 'condition': 'Used-good'}
    # # # itemInfo = {'barcode': '4043972146181', 'title': 'Blackjack: Play Like The Pros', 'condition': 'Used-good'}
    # # itemInfo = {'barcode': '4043972146181', 'title': 'Blackjack: Play Like The Pros', 'condition': 'New'}
    # itemInfo = {'barcode': '', 'title': 'Tomtom XL 340TM', 'condition': 'Used-good'}
    # # itemInfo = {'barcode': '', 'title': 'iphone 4 black', 'condition': 'Used-good'}
    # itemInfo = {'barcode': '', 'title': 'iphone 4 white', 'condition': 'New'}
    # # itemInfo = {'barcode': '', 'title': 'Blackjack: Play Like The Pros', 'condition': 'New'}
    # # itemInfo = {'barcode': '', 'title': 'Blackjack: Play Like The Pros', 'condition': 'Used-good'}
    
    print itemInfo
    
    # cookie = cookielib.CookieJar()   
    # opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    # opener.addheaders = [('User-agent', 'Chrome/21.0.1180.57 Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/537.1 (KHTML, like Gecko) Safari/537.1')]
    # # opener.addheaders = [('User-agent', 'Chrome/21.0.1180.57')]
    

    if itemInfo.get('barcode', ''):
        barcode = itemInfo['barcode'].lstrip('0');
        if len(barcode)==9 or len(barcode)==11:
            barcode = '0' + barcode #A simple hack to compensate the mistakenly stripped zero for isbn or upc.
        searchUrl = 'http://www.ebay.com/sch/i.html?_nkw='+barcode
    elif itemInfo.get('title', ''):
        searchUrl = ('http://www.ebay.com/sch/i.html?_nkw='+urllib.quote(itemInfo['title'].strip()))
    else:
        return epInfo
   
    # #Simplify condition to 'free' and 'used' two levels for now.
    # if 'new' in itemInfo.get('condition', '').lower():
        # condition = 'new'
    # else:
        # condition = 'used'
        
    
    # binStr = '&LH_BIN=1'
    # matchStr = '&_sop=12'
    # locStr = '&LH_PrefLoc=1'
    # nItemsStr = '&_ipg=200'
    # completedStr = '&LH_Complete=1'
    # soldStr = '&LH_Sold=1'
    # viewStr = '&_dmd=1' #1 for list view, #2 for gallery view
    # if 'new' in itemInfo.get('condition', '').lower():
        # condUrlStr = '&LH_ItemCondition=3'          
    # else:
        # condUrlStr = '&LH_ItemCondition=4'
    # queryUrl = matchStr+condUrlStr+locStr+nItemsStr+viewStr+completedStr+soldStr
    # searchUrl += queryUrl
    # searchUrlOrig = searchUrl #Saved for calculating category default value.
    print searchUrl 
    
    # req = opener.open(searchUrl) 
    # redirUrl = req.geturl()
    strHTML, redirUrl = operation3.url2strmore(searchUrl)
    print redirUrl
    recommendedItem = {}
    if '/ctg/' in redirUrl:
        #Get the recommended item
        # strHTML = req.read()
        epid = ''
        if redirUrl.split('/')[-1].isdigit():
            epid = redirUrl.split('/')[-1]
        
        if strHTML:
            recommendedItem['link'] = redirUrl
            root = etree.HTML(strHTML)
            titleTags = root.xpath('//h3[@class="tpc-titr"]')
            if titleTags:
                recommendedItem['title'] = titleTags[0].text
                    
            imgTags = root.xpath('//div[@id="v4-15"]//img')
            # print imgTags
            if imgTags:
                imgUrl = imgTags[0].get('xrc', '')
                # print imgUrl
                if imgUrl:
                    recommendedItem['imgUrl'] = imgUrl
            
            # Category number
            category = ''
            catTags = root.xpath('//li[@itemprop="offers"]/a')
            if catTags:
                category = catTags[0].get('href', '').split('_pcategid=')[-1].split('&')[0]
                print category
            
            
            # User Category
            userCat = ''
            topCatTags = root.xpath('//meta[@name = "keywords"]')
            if topCatTags:
                topCatStr = topCatTags[0].get('content')
                topCatStr = topCatStr.split(', ebay, listings')[0].split(',')[-1].strip()
                userCat = categoryMap2.get(topCatStr.lower(), '')
                print userCat
            
            
            #Get the brand new and used prices for the recommended item.
            recommendedTags = root.xpath('//table[@class="bb-btbl"]')
            usedFound = 0
            for recommendedTag in recommendedTags:
                conditionStr = ''.join(recommendedTag.xpath('.//div[@class="bb-cd"]//div[@class="bb-rtd"]//text()')).strip()
                # print conditionStr
                if 'brand new' in conditionStr.lower() or conditionStr.lower()[:3] == 'new':
                    priceStr = ''.join(recommendedTag.xpath('.//div[@class="bb-l"]//strong//text()'))
                    # print etree.tostring(recommendedTag.xpath('.//div[@class="bb-l"]')[0])
                    # print priceStr
                    if priceStr:
                        recommendedItem['marketNew'] = float(priceStr.strip().replace('$', '').replace(',',''))
                        # print conditionStr
                        # print recommendedItem['marketNew']
                elif conditionStr.lower() == 'good' or conditionStr.lower() == 'used':
                    usedFound = 1
                    priceStr = ''.join(recommendedTag.xpath('.//div[@class="bb-l"]//strong//text()'))
                    #print etree.tostring(recommendedTag.xpath('.//div[@class="bb-l"]')[0])
                    # print priceStr
                    if priceStr:
                        recommendedItem['marketUsed'] = float(priceStr.strip().replace('$', '').replace(',',''))
                        # print conditionStr
                        # print recommendedItem['marketUsed']
                elif (not usedFound) and ('refurbished' not in conditionStr.lower()):
                    usedFound = 1
                    priceStr = ''.join(recommendedTag.xpath('.//div[@class="bb-l"]//strong//text()'))
                    # print recommendedTag.xpath('.//div[@class="bb-l"]//strong')
                    #print etree.tostring(recommendedTag)
                    # print priceStr
                    if priceStr:
                        recommendedItem['marketUsed'] = float(priceStr.strip().replace('$', '').replace(',',''))
                        # print conditionStr
                        # print recommendedItem['marketUsed']
            #print recommendedItem
                
            # pricesUrl = redirUrl + queryUrl.replace('&', '?', 1)
            # print pricesUrl
            # req = opener.open(pricesUrl)
            # strHTML = req.read()
            
            # searchResult = parseProductPageSold(strHTML)
            # #If no result found for 'new' items, used 'used' for search instead.
            # if (not searchResult.get('firstPageItems', [])) and (condition == 'new'):
                # print 'No condition new sold items found, search for used items.'
                # pricesUrl = pricesUrl.replace('&LH_ItemCondition=3', '&LH_ItemCondition=4')
                # print pricesUrl
                # req = opener.open(pricesUrl) 
                # strHTML = req.read()
                # if strHTML:
                    # searchResult = parseProductPageSold(strHTML)
            # print searchResult
            
            epInfo['category'] = category
            epInfo['userCat'] = userCat
            epInfo['recommendedItem'] = recommendedItem
            epInfo['epid'] = epid
            # resellValue['firstPageItems'] = searchResult.get('firstPageItems', {})
            # Always get the new title from the product page function.
            epInfo['title'] = recommendedItem.get('title', '')
            # if itemInfo.get('title'):
                # resellValue['title'] = itemInfo['title']
            # else:
                # resellValue['title'] = recommendedItem.get('title', '')
            # if searchResult.get('resellPrice', 0):
                # if condition == 'new':
                    # resellValue['resellNew'] = searchResult['resellPrice']
                    # print resellValue['resellNew'] 
                    # # if recommendedItem.get('marketNew', 0) and recommendedItem.get('marketNew', 0)<resellValue['resellNew']:
                        # # resellValue['resellNew'] = recommendedItem['marketNew']
                # else:
                    # resellValue['resellUsed'] = searchResult['resellPrice']
                    # print resellValue['resellNew'] 
                    # # if recommendedItem.get('marketUsed', 0) and recommendedItem.get('marketUsed', 0)<resellValue['resellUsed']:
                        # # resellValue['resellUsed'] = recommendedItem['marketUsed']
            
            # print resellValue
     
    # else:
        # #print 'I am here'
        # # Log in to ebay
        # cookie = cookielib.CookieJar()   
        # opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
        # opener.addheaders = [('User-agent', 'Chrome/21.0.1180.57 Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/537.1 (KHTML, like Gecko) Safari/537.1')]
        # # opener.addheaders = [('User-agent', 'Chrome/21.0.1180.57')]
    
        
        # category = ''
        # categories, opener = queryCategory(itemInfo['title'].strip())
        # if categories:
            # category = categories[0][0]
        # # print category
            
        # # ebayCred = operation3.getDBLogin('ebayalpwan1')
        # # log = {'MfcISAPICommand': 'SignInWelcome', 'co_partnerId': 502, 'userid': ebayCred['username'], 'pass': ebayCred['password']}
        # # signUrl = 'https://signin.ebay.com/ws/eBayISAPI.dll'
        # # login_data = urllib.urlencode(log)
        # # req = opener.open(signUrl)
        # # req = opener.open(signUrl, login_data)
        # # category = ''
        # # if 'accountsummary' in req.url.lower():
            # # catSearchStr = '&cpg=4&aid=4&keywords='+urllib.quote(itemInfo['title'].strip())
            # # catSearchUrl = 'http://cgi5.ebay.com/ws/eBayISAPI.dll?NewListing'+catSearchStr
            # # req = opener.open(catSearchUrl)
            # # strHTML = req.read()
            # # root = etree.HTML(strHTML)
            # # optionTags = root.xpath('//div[@id="cat1_inp"]//option')
            # # #print optionTags
            # # if optionTags:
                # # category = optionTags[0].get('value', '')
                # # print optionTags[0].text
        # searchUrl = searchUrl.replace('sch/', 'sch/'+category+'/')
        # # req = opener.open(searchUrl)
        # # req = opener.open('http://cgi5.ebay.com/ws/eBayISAPI.dll?NewListing&cpg=4&aid=4&keywords=test123')
        # # print 'searchUrl'
        # # print req.url
        # # strHTML = req.read()
        # # f = open('ebay01.html', 'w')
        # # f.write(strHTML)
        # # f.close()
        
        # req = opener.open(searchUrl)
        # strHTML = req.read()
        # # f = open('ebay02.html', 'w')
        # # f.write(strHTML)
        # # f.close()
        
        
        
        # searchResult = parseCompletedPage(strHTML, req.url)        
        # #If no result found for 'new' items, used 'used' for search instead.
        # if (not searchResult.get('firstPageItems', [])) and (condition == 'new'):
            # print 'No condition new sold items found, search for used items.'
            # searchUrl = searchUrl.replace('&LH_ItemCondition=3', '&LH_ItemCondition=4')
            # print searchUrl
            # req = opener.open(searchUrl) 
            # strHTML = req.read()
            # if strHTML:
                # searchResult = parseCompletedPage(strHTML, req.url) 

        # # print 'searchResult:'
        # # print searchResult
        # resellValue['category'] = category
        # resellValue['userCat'] = searchResult.get('userCat', '')
        # resellValue['recommendedItem'] = {}
        # resellValue['firstPageItems'] = searchResult.get('firstPageItems', [])
        # if itemInfo.get('title', ''):
            # resellValue['title'] = itemInfo['title']
        # elif itemInfo.get('barcode', '') and len(resellValue['firstPageItems']):
            # resellValue['title'] = resellValue['firstPageItems'][0]['title']
        # if searchResult.get('resellPrice', 0):
            # if 'new' in itemInfo.get('condition', '').lower():
                # resellValue['resellNew'] = searchResult['resellPrice']
                # # if recommendedItem.get('marketNew', 0) and recommendedItem.get('marketNew', 0)<resellValue['resellNew']:
                    # # resellValue['resellNew'] = recommendedItem['marketNew']
            # else:
                # resellValue['resellUsed'] = searchResult['resellPrice']
                # # if recommendedItem.get('marketUsed', 0) and recommendedItem.get('marketUsed', 0)<resellValue['resellUsed']:
                    # # resellValue['resellUsed'] = recommendedItem['marketUsed']
    
    # #Get the range:
    # Nitems = len(resellValue.get('firstPageItems', {}))
    # print 'Sold items: %d' % Nitems
    # sortedItems = sorted(resellValue['firstPageItems'], key=lambda d: (d.get('marketNew', 0)+d.get('marketUsed',0)))
    # if Nitems:
        # if Nitems > 1:
            # pointLow = min(float(Nitems-1)/4, 1)*0.25
            # pointHigh = 0.75
            # # pointExp = 0.25+ max(min(float(Nitems-10)/90, 1), 0)*0.125
            # pointExp = 0.25
            # pricePerLow = operation3.percentile(sortedItems, pointLow, key=lambda d: (d.get('marketNew', 0)+d.get('marketUsed',0)))*0.75
            # pricePerExp = operation3.percentile(sortedItems, pointExp, key=lambda d: (d.get('marketNew', 0)+d.get('marketUsed',0)))
            # pricePerHigh = operation3.percentile(sortedItems, pointHigh, key=lambda d: (d.get('marketNew', 0)+d.get('marketUsed',0)))
            # resellValue['rangeLow'] = (pricePerLow-3)*0.8
            # resellValue['rangeHigh'] = (pricePerHigh-3)*0.8
            # resellValue['expectation'] = (pricePerExp-3)*0.8
            # if (resellValue['rangeHigh']-resellValue['expectation'])>(resellValue['expectation']-resellValue['rangeLow'])*2:
                # resellValue['rangeHigh'] = resellValue['rangeLow']+(resellValue['expectation']-resellValue['rangeLow'])*3
            # print 'pointLow: %.2f, %.2f' % (pointLow, resellValue['rangeLow'])
            # print 'pointHigh: %.2f, %.2f' % (pointHigh, resellValue['rangeHigh'])
            # print 'pointExp: %.2f, %.2f' % (pointExp, resellValue['expectation'])
        # else:
            # resellValue['rangeHigh'] = (sortedItems[0].get('marketNew', 0)+sortedItems[0].get('marketUsed', 0)-3)*0.8
            # resellValue['rangeLow'] = (sortedItems[0].get('marketNew', 0)+sortedItems[0].get('marketUsed', 0)-3)*0.8*0.5
            # resellValue['expectation'] = (sortedItems[0].get('marketNew', 0)+sortedItems[0].get('marketUsed', 0)-3)*0.8*2/3
            # print 'pointLow: %.2f' % (resellValue['rangeLow'])
            # print 'pointHigh: %.2f' % (resellValue['rangeHigh'])
            # print 'pointExp: %.2f' % (resellValue['expectation'])
        
        # if 'new' in itemInfo.get('condition', '').lower():
            # print 'listNew: 0.5, %.2f' % resellValue.get('resellNew', 0)
        # else:
            # print 'listUsed: 0.5, %.2f' % resellValue.get('resellUsed', 0)
                
    # else:
        # #Get category default values if the search cannot find a match.
        # if resellValue.get('category', ''):
            # #print resellValue
            # #Get the url for all items inside the category
            # searchUrl = (searchUrlOrig.split('_nkw', 1)[0]+searchUrlOrig.split('_nkw', 1)[-1].split('&', 1)[-1]).replace('sch/', 'sch/'+category+'/')
            # req = opener.open(searchUrl)
            # print req.url
            
            # strHTML = req.read()
                    
            # f = open('ebay.html', 'w')
            # f.write(strHTML)
            # f.close()
            
            # searchResult = parseCompletedPage(strHTML, req.url)  
            # if searchResult.get('resellPrice', 0):
                # if 'new' in itemInfo.get('condition', '').lower():
                    # resellValue['resellNew'] = searchResult['resellPrice']
                # else:
                    # resellValue['resellUsed'] = searchResult['resellPrice']
                    
            # Nitems = len(searchResult.get('firstPageItems', []))
            # print 'Default items in category: %d' % Nitems
            # if Nitems:
                # resellValue['default'] = 1;
                # sortedItems = sorted(searchResult['firstPageItems'], key=lambda d: (d.get('marketNew', 0)+d.get('marketUsed',0)))
                # pointExp = 0.25
                # pricePerExp = operation3.percentile(sortedItems, pointExp, key=lambda d: (d.get('marketNew', 0)+d.get('marketUsed',0)))
                # # print pointExp
                # resellValue['rangeHigh'] = (pricePerExp-3)*0.8*1.5
                # resellValue['rangeLow'] = (pricePerExp-3)*0.8*0.75
                # resellValue['expectation'] = (pricePerExp-3)*0.8
                # print 'pointLow: %.2f' % (resellValue['rangeLow'])
                # print 'pointHigh: %.2f' % (resellValue['rangeHigh'])
                # print 'pointExp: %.2f' % (resellValue['expectation'])
                
                # if 'new' in itemInfo.get('condition', '').lower():
                    # print 'listNew: 0.5, %.2f' % resellValue.get('resellNew', 0)
                # else:
                    # print 'listUsed: 0.5, %.2f' % resellValue.get('resellUsed', 0)
            
            # print searchResult
                
            
    
    
    
    
        # print resellValue
            
            
        # f = open('ebay.html', 'w')
        # f.write(strHTML)
        # f.close()

    
    return epInfo
            
##End of queryProduct(itemInfo)    
    

    
    
#http://www.ebay.com/sch/i.html?_nkw=the+davinci+code&_sop=12
#&_sop=12 means best match; &LH_BIN=1 means buy it now; &LH_ItemCondition=4 means used, 3 means new; LH_PreFloc=1 means US Only
#on productised item page. ?&tabs=15 for all items. &LH_BIN=1 for buy it now
def queryPriceAllCond2(itemInfo):
#search for best matched price to sell on ebay
#itemInfo is dict with keys: barcode, title, category
#

    resellValue = {}
    
    # opener = urllib2.build_opener(urllib2.HTTPRedirectHandler)
    
    # itemInfo = {'barcode': '0818406569', 'title': 'Blackjack: Play Like The Pros', 'condition': 'Used-good'}
    # itemInfo = {'barcode': '0321611136', 'title': 'Blackjack: Play Like The Pros', 'condition': 'Used-good'}
    # # # itemInfo = {'barcode': '4043972146181', 'title': 'Blackjack: Play Like The Pros', 'condition': 'Used-good'}
    # # itemInfo = {'barcode': '4043972146181', 'title': 'Blackjack: Play Like The Pros', 'condition': 'New'}
    # itemInfo = {'barcode': '', 'title': 'Tomtom XL 340TM', 'condition': 'Used-good'}
    # # itemInfo = {'barcode': '', 'title': 'iphone 4 black', 'condition': 'Used-good'}
    # itemInfo = {'barcode': '', 'title': 'iphone 4 white', 'condition': 'New'}
    # # itemInfo = {'barcode': '', 'title': 'Blackjack: Play Like The Pros', 'condition': 'New'}
    # # itemInfo = {'barcode': '', 'title': 'Blackjack: Play Like The Pros', 'condition': 'Used-good'}
    
    # print itemInfo
    
    cookie = cookielib.CookieJar()   
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    opener.addheaders = [('User-agent', 'Chrome/21.0.1180.57 Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/537.1 (KHTML, like Gecko) Safari/537.1')]
    # opener.addheaders = [('User-agent', 'Chrome/21.0.1180.57')]
    

    if itemInfo.get('barcode', ''):
        barcode = itemInfo['barcode'].lstrip('0');
        if len(barcode)==9 or len(barcode)==11:
            barcode = '0' + barcode #A simple hack to compensate the mistakenly stripped zero for isbn or upc.
        searchUrl = 'http://www.ebay.com/sch/i.html?_nkw='+barcode
    elif itemInfo.get('title', ''):
        searchUrl = ('http://www.ebay.com/sch/i.html?_nkw='+urllib.quote(itemInfo['title'].strip()))
    else:
        return resellValue
   
    condition = 'new'
    #Simplify condition to 'new' and 'used' two levels for now.
    # if 'new' in itemInfo.get('condition', '').lower():
        # condition = 'new'
    # else:
        # condition = 'used'
        
    #Get category from itemInfo
    category = itemInfo.get('category', '')
    
    binStr = '&LH_BIN=1'
    matchStr = '&_sop=12'
    locStr = '&LH_PrefLoc=1'
    nItemsStr = '&_ipg=200'
    completedStr = '&LH_Complete=1'
    soldStr = '&LH_Sold=1'
    viewStr = '&_dmd=1' #1 for list view, #2 for gallery view
    condNewStr = '&LH_ItemCondition=3'
    condUsedStr = '&LH_ItemCondition=4'
    # if 'new' in itemInfo.get('condition', '').lower():
        # condUrlStr = '&LH_ItemCondition=3'          
    # else:
        # condUrlStr = '&LH_ItemCondition=4'
        
        
    #Check for condition new first
    queryUrl = matchStr+condNewStr+locStr+nItemsStr+viewStr+completedStr+soldStr
    searchUrl += queryUrl
    searchUrlOrig = searchUrl #Saved for calculating category default value.
    searchUrl = searchUrl.replace('sch/', 'sch/'+category+'/')
    # print searchUrl
    
    req = opener.open(searchUrl) 
    redirUrl = req.geturl()
    # print redirUrl
    recommendedItem = {}
    if '/ctg/' in redirUrl:
        #Get the recommended item
        strHTML = req.read()
        if strHTML:
            recommendedItem['link'] = redirUrl
            root = etree.HTML(strHTML)
            titleTags = root.xpath('//h3[@class="tpc-titr"]')
            if titleTags:
                recommendedItem['title'] = titleTags[0].text
                    
            imgTags = root.xpath('//div[@id="v4-15"]//img')
            # print imgTags
            if imgTags:
                imgUrl = imgTags[0].get('xrc', '')
                # print imgUrl
                if imgUrl:
                    recommendedItem['imgUrl'] = imgUrl
            
            # Category number
            catTags = root.xpath('//li[@itemprop="offers"]/a')
            if catTags:
                category = catTags[0].get('href', '').split('_pcategid=')[-1].split('&')[0]
                # print category
            
            
            # User Category
            userCat = ''
            topCatTags = root.xpath('//meta[@name = "keywords"]')
            if topCatTags:
                topCatStr = topCatTags[0].get('content')
                topCatStr = topCatStr.split(', ebay, listings')[0].split(',')[-1].strip()
                # print topCatStr
                userCat = categoryMap2.get(topCatStr.lower(), '')
                # print userCat
            
     
            
            #Get the brand new and used prices for the recommended item.
            recommendedTags = root.xpath('//table[@class="bb-btbl"]')
            usedFound = 0
            for recommendedTag in recommendedTags:
                conditionStr = ''.join(recommendedTag.xpath('.//div[@class="bb-cd"]//div[@class="bb-rtd"]//text()')).strip()
                # print conditionStr
                if 'brand new' in conditionStr.lower() or conditionStr.lower()[:3] == 'new':
                    priceStr = ''.join(recommendedTag.xpath('.//div[@class="bb-l"]//strong//text()'))
                    # print etree.tostring(recommendedTag.xpath('.//div[@class="bb-l"]')[0])
                    # print priceStr
                    if priceStr:
                        recommendedItem['marketNew'] = float(priceStr.strip().replace('$', '').replace(',',''))
                        # print conditionStr
                        # print recommendedItem['marketNew']
                elif conditionStr.lower() == 'good' or conditionStr.lower() == 'used':
                    usedFound = 1
                    priceStr = ''.join(recommendedTag.xpath('.//div[@class="bb-l"]//strong//text()'))
                    #print etree.tostring(recommendedTag.xpath('.//div[@class="bb-l"]')[0])
                    # print priceStr
                    if priceStr:
                        recommendedItem['marketUsed'] = float(priceStr.strip().replace('$', '').replace(',',''))
                        # print conditionStr
                        # print recommendedItem['marketUsed']
                elif (not usedFound) and ('refurbished' not in conditionStr.lower()):
                    usedFound = 1
                    priceStr = ''.join(recommendedTag.xpath('.//div[@class="bb-l"]//strong//text()'))
                    # print recommendedTag.xpath('.//div[@class="bb-l"]//strong')
                    #print etree.tostring(recommendedTag)
                    # print priceStr
                    if priceStr:
                        recommendedItem['marketUsed'] = float(priceStr.strip().replace('$', '').replace(',',''))
                        # print conditionStr
                        # print recommendedItem['marketUsed']
            #print recommendedItem
                
            pricesUrl = redirUrl + queryUrl.replace('&', '?', 1)
            # print pricesUrl
            req = opener.open(pricesUrl)
            strHTML = req.read()
            # f = open('ebay.html', 'w')
            # f.write(strHTML)
            # f.close()
            if strHTML:
                searchResultNew = parseProductPageSold(strHTML)
            
            # print searchResult
            
            #Search for old condition
            pricesUrl = pricesUrl.replace(condNewStr, condUsedStr)
            req = opener.open(pricesUrl) 
            strHTML = req.read()
            if strHTML:
                searchResultOld = parseProductPageSold(strHTML)
            
            
            
            #If no result found for 'new' items, used 'used' for search instead.
            # if (not searchResult.get('firstPageItems', [])) and (condition == 'new'):
                # # print 'No condition new sold items found, search for used items.'
                # pricesUrl = pricesUrl.replace('&LH_ItemCondition=3', '&LH_ItemCondition=4')
                # # print pricesUrl
                # req = opener.open(pricesUrl) 
                # strHTML = req.read()
                # if strHTML:
                    # searchResult = parseProductPageSold(strHTML)
                    
                    
            # print searchResult
            resellValue['category'] = category
            resellValue['userCat'] = userCat
            resellValue['recommendedItem'] = recommendedItem
            resellValue['firstPageItemsNew'] = searchResultNew.get('firstPageItems', {})
            resellValue['firstPageItemsOld'] = searchResultOld.get('firstPageItems', {})
            if not resellValue['firstPageItemsNew']:
                resellValue['firstPageItemsNew'] = resellValue['firstPageItemsOld']
            # Always get the new title from the product page function.
            resellValue['title'] = recommendedItem.get('title', '')
            # if itemInfo.get('title'):
                # resellValue['title'] = itemInfo['title']
            # else:
                # resellValue['title'] = recommendedItem.get('title', '')
                
            resellValue['resellNew'] = searchResultNew.get('resellPrice',  0)
            resellValue['resellOld'] = searchResultOld.get('resellPrice',  0)
            if not resellValue['resellNew']:
                resellValue['resellNew'] = resellValue['resellOld'] 
            
            # if searchResult.get('resellPrice', 0):
                # if condition == 'new':
                    # resellValue['resellNew'] = searchResult['resellPrice']

                    # # if recommendedItem.get('marketNew', 0) and recommendedItem.get('marketNew', 0)<resellValue['resellNew']:
                        # # resellValue['resellNew'] = recommendedItem['marketNew']
                # else:
                    # resellValue['resellUsed'] = searchResult['resellPrice']

                    # if recommendedItem.get('marketUsed', 0) and recommendedItem.get('marketUsed', 0)<resellValue['resellUsed']:
                        # resellValue['resellUsed'] = recommendedItem['marketUsed']
            
            # print resellValue
     
    else:
        # #print 'I am here'
        # # Log in to ebay
        # cookie = cookielib.CookieJar()   
        # opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
        # opener.addheaders = [('User-agent', 'Chrome/21.0.1180.57 Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/537.1 (KHTML, like Gecko) Safari/537.1')]
        # # opener.addheaders = [('User-agent', 'Chrome/21.0.1180.57')]
    
        
        if not category:
            if itemInfo.get('title', ''):
                categories, opener = queryCategory(itemInfo['title'].strip())
            elif itemInfo.get('barcode', ''):
                categories, opener = queryCategory(barcode)
            if categories:
                category = categories[0][0]
            searchUrl = searchUrl.replace('sch/', 'sch/'+category+'/')
            req = opener.open(searchUrl)


        strHTML = req.read()
        # f = open('ebay.html', 'w')
        # f.write(strHTML)
        # f.close()
        
        
        if strHTML:
            searchResultNew = parseCompletedPage(strHTML, req.url)
            
        searchUrl = searchUrl.replace(condNewStr, condUsedStr)
        req = opener.open(searchUrl) 
        strHTML = req.read()
        if strHTML:
            searchResultOld = parseCompletedPage(strHTML, req.url) 

        # searchResult = parseCompletedPage(strHTML, req.url)        
        # #If no result found for 'new' items, used 'used' for search instead.
        # if (not searchResult.get('firstPageItems', [])) and (condition == 'new'):
            # # print 'No condition new sold items found, search for used items.'
            # searchUrl = searchUrl.replace('&LH_ItemCondition=3', '&LH_ItemCondition=4')
            # # print searchUrl
            # req = opener.open(searchUrl) 
            # strHTML = req.read()
            # if strHTML:
                # searchResult = parseCompletedPage(strHTML, req.url) 

        # print 'searchResult:'
        # print searchResult
        resellValue['category'] = category
        if searchResultNew.get('userCat', ''):
            resellValue['userCat'] = searchResultNew.get('userCat', '')
        elif searchResultOld.get('userCat', ''):
            resellValue['userCat'] = searchResultOld.get('userCat', '')
        resellValue['recommendedItem'] = {}
        resellValue['firstPageItemsNew'] = searchResultNew.get('firstPageItems', {})
        resellValue['firstPageItemsOld'] = searchResultOld.get('firstPageItems', {})
        # if itemInfo.get('title', ''):
            # resellValue['title'] = itemInfo['title']
        # elif itemInfo.get('barcode', '') and len(resellValue['firstPageItems']):
            # resellValue['title'] = resellValue['firstPageItems'][0]['title']
            
        resellValue['resellNew'] = searchResultNew.get('resellPrice',  0)
        resellValue['resellOld'] = searchResultOld.get('resellPrice',  0)
        if not resellValue['resellNew']:
            resellValue['resellNew'] = resellValue['resellOld'] 
            
        # if searchResult.get('resellPrice', 0):
            # if 'new' in itemInfo.get('condition', '').lower():
                # resellValue['resellNew'] = searchResult['resellPrice']
                # # if recommendedItem.get('marketNew', 0) and recommendedItem.get('marketNew', 0)<resellValue['resellNew']:
                    # # resellValue['resellNew'] = recommendedItem['marketNew']
            # else:
                # resellValue['resellUsed'] = searchResult['resellPrice']
                # # if recommendedItem.get('marketUsed', 0) and recommendedItem.get('marketUsed', 0)<resellValue['resellUsed']:
                    # # resellValue['resellUsed'] = recommendedItem['marketUsed']
    
    #Get the range for New:
    newSoldFound = True
    Nitems = len(resellValue.get('firstPageItemsNew', {}))
    # print 'Sold items: %d' % Nitems
    sortedItems = sorted(resellValue['firstPageItemsNew'], key=lambda d: (d.get('marketNew', 0)+d.get('marketUsed',0)))
    if Nitems:
        if Nitems > 1:
            pointLow = min(float(Nitems-1)/4, 1)*0.25
            pointHigh = 0.75
            # pointExp = 0.25+ max(min(float(Nitems-10)/90, 1), 0)*0.125
            pointExp = 0.25
            pricePerLow = operation3.percentile(sortedItems, pointLow, key=lambda d: (d.get('marketNew', 0)+d.get('marketUsed',0)))*0.75
            pricePerExp = operation3.percentile(sortedItems, pointExp, key=lambda d: (d.get('marketNew', 0)+d.get('marketUsed',0)))
            pricePerHigh = operation3.percentile(sortedItems, pointHigh, key=lambda d: (d.get('marketNew', 0)+d.get('marketUsed',0)))
            #Removing the (x-3)*0.8 method for the local based app.
            # resellValue['rangeLowNew'] = (pricePerLow-3)*0.8
            resellValue['rangeLowNew'] = pricePerLow
            resellValue['rangeHighNew'] = pricePerHigh
            resellValue['expectationNew'] = pricePerExp
            if (resellValue['rangeHighNew']-resellValue['expectationNew'])>(resellValue['expectationNew']-resellValue['rangeLowNew'])*2:
                resellValue['rangeHighNew'] = resellValue['rangeLowNew']+(resellValue['expectationNew']-resellValue['rangeLowNew'])*3
            # print 'pointLow: %.2f, %.2f' % (pointLow, resellValue['rangeLow'])
            # print 'pointHigh: %.2f, %.2f' % (pointHigh, resellValue['rangeHigh'])
            # print 'pointExp: %.2f, %.2f' % (pointExp, resellValue['expectation'])
        else:
            resellValue['rangeHighNew'] = sortedItems[0].get('marketNew', 0)+sortedItems[0].get('marketUsed', 0)
            resellValue['rangeLowNew'] = (sortedItems[0].get('marketNew', 0)+sortedItems[0].get('marketUsed', 0))*0.5
            resellValue['expectationNew'] = (sortedItems[0].get('marketNew', 0)+sortedItems[0].get('marketUsed', 0))*2/3
            # print 'pointLow: %.2f' % (resellValue['rangeLow'])
            # print 'pointHigh: %.2f' % (resellValue['rangeHigh'])
            # print 'pointExp: %.2f' % (resellValue['expectation'])
        
        # if 'new' in itemInfo.get('condition', '').lower():
            # # print 'listNew: 0.5, %.2f' % resellValue.get('resellNew', 0)
            # pass
        # else:
            # # print 'listUsed: 0.5, %.2f' % resellValue.get('resellUsed', 0)
            # pass
    else: 
        newSoldFound = False

      
    #Get the range for Old:
    Nitems = len(resellValue.get('firstPageItemsOld', {}))
    # print 'Sold items: %d' % Nitems
    sortedItems = sorted(resellValue['firstPageItemsOld'], key=lambda d: (d.get('marketNew', 0)+d.get('marketUsed',0)))
    if Nitems:
        if Nitems > 1:
            pointLow = min(float(Nitems-1)/4, 1)*0.25
            pointHigh = 0.75
            # pointExp = 0.25+ max(min(float(Nitems-10)/90, 1), 0)*0.125
            pointExp = 0.25
            pricePerLow = operation3.percentile(sortedItems, pointLow, key=lambda d: (d.get('marketNew', 0)+d.get('marketUsed',0)))*0.75
            pricePerExp = operation3.percentile(sortedItems, pointExp, key=lambda d: (d.get('marketNew', 0)+d.get('marketUsed',0)))
            pricePerHigh = operation3.percentile(sortedItems, pointHigh, key=lambda d: (d.get('marketNew', 0)+d.get('marketUsed',0)))
            resellValue['rangeLowOld'] = pricePerLow
            resellValue['rangeHighOld'] = pricePerHigh
            resellValue['expectationOld'] = pricePerExp
            if (resellValue['rangeHighOld']-resellValue['expectationOld'])>(resellValue['expectationOld']-resellValue['rangeLowOld'])*2:
                resellValue['rangeHighOld'] = resellValue['rangeLowOld']+(resellValue['expectationOld']-resellValue['rangeLowOld'])*3
            # print 'pointLow: %.2f, %.2f' % (pointLow, resellValue['rangeLow'])
            # print 'pointHigh: %.2f, %.2f' % (pointHigh, resellValue['rangeHigh'])
            # print 'pointExp: %.2f, %.2f' % (pointExp, resellValue['expectation'])
        else:
            resellValue['rangeHighOld'] = sortedItems[0].get('marketNew', 0)+sortedItems[0].get('marketUsed', 0)
            resellValue['rangeLowOld'] = (sortedItems[0].get('marketNew', 0)+sortedItems[0].get('marketUsed', 0))*0.5
            resellValue['expectationOld'] = (sortedItems[0].get('marketNew', 0)+sortedItems[0].get('marketUsed', 0))*2/3
            # print 'pointLow: %.2f' % (resellValue['rangeLow'])
            # print 'pointHigh: %.2f' % (resellValue['rangeHigh'])
            # print 'pointExp: %.2f' % (resellValue['expectation'])
        
        # if 'new' in itemInfo.get('condition', '').lower():
            # # print 'listNew: 0.5, %.2f' % resellValue.get('resellNew', 0)
            # pass
        # else:
            # # print 'listUsed: 0.5, %.2f' % resellValue.get('resellUsed', 0)
            # pass
                
        
                   
    else:
        #Get category default values if the search cannot find a match.
        if resellValue.get('category', ''):
            #print resellValue
            #Get the url for all items inside the category
            #Here the condition in searchUrl is old. ToDo: make it more explicit and clear.
            searchUrl = (searchUrlOrig.split('_nkw', 1)[0]+searchUrlOrig.split('_nkw', 1)[-1].split('&', 1)[-1]).replace('sch/', 'sch/'+category+'/')
            req = opener.open(searchUrl)
            # print req.url
            strHTML = req.read()
                    
            # f = open('ebay.html', 'w')
            # f.write(strHTML)
            # f.close()
            
            searchResult = parseCompletedPage(strHTML, req.url)  
            resellValue['resellUsed'] = searchResult.get('resellPrice', 0)
            if not newSoldFound:
                resellValue['resellNew']  =  resellValue['resellOld']  
     
            # if searchResult.get('resellPrice', 0):
                # if 'new' in itemInfo.get('condition', '').lower():
                    # resellValue['resellNew'] = searchResult['resellPrice']
                # else:
                    # resellValue['resellUsed'] = searchResult['resellPrice']
                    
            Nitems = len(searchResult.get('firstPageItems', []))
            # print 'Default items in category: %d' % Nitems
            if Nitems:
                resellValue['default'] = 1;
                sortedItems = sorted(searchResult['firstPageItems'], key=lambda d: (d.get('marketNew', 0)+d.get('marketUsed',0)))
                pointExp = 0.25
                pricePerExp = operation3.percentile(sortedItems, pointExp, key=lambda d: (d.get('marketNew', 0)+d.get('marketUsed',0)))
                # print pointExp
                resellValue['rangeHighOld'] = pricePerExp*1.5
                resellValue['rangeLowOld'] = pricePerExp*0.75
                resellValue['expectationOld'] = pricePerExp
                # print 'pointLow: %.2f' % (resellValue['rangeLow'])
                # print 'pointHigh: %.2f' % (resellValue['rangeHigh'])
                # print 'pointExp: %.2f' % (resellValue['expectation'])
                
                # if 'new' in itemInfo.get('condition', '').lower():
                    # print 'listNew: 0.5, %.2f' % resellValue.get('resellNew', 0)
                # else:

                    # print 'listUsed: 0.5, %.2f' % resellValue.get('resellUsed', 0)
            
            # print searchResult
                
    # print newSoldFound
    if not newSoldFound:
        resellValue['rangeHighNew'] = resellValue.get('rangeHighOld', 0)
        resellValue['rangeLowNew'] = resellValue.get('rangeLowOld', 0)
        resellValue['expectationNew'] = resellValue.get('expectationOld', 0)





        # print resellValue
            
            
        # f = open('ebay.html', 'w')
        # f.write(strHTML)
        # f.close()

    
    return resellValue
            
##End of queryPriceAllCond2(itemInfo)

        
         
#http://www.ebay.com/sch/i.html?_nkw=the+davinci+code&_sop=12
#&_sop=12 means best match; &LH_BIN=1 means buy it now; &LH_ItemCondition=4 means used, 3 means new; LH_PreFloc=1 means US Only
#on productised item page. ?&tabs=15 for all items. &LH_BIN=1 for buy it now
def queryPriceAllCond(itemInfo):
#search for best matched price to sell on ebay
#itemInfo is dict with keys: barcode, title, condition
#

    resellValue = {}
    
    # opener = urllib2.build_opener(urllib2.HTTPRedirectHandler)
    
    # itemInfo = {'barcode': '0818406569', 'title': 'Blackjack: Play Like The Pros', 'condition': 'Used-good'}
    # itemInfo = {'barcode': '0321611136', 'title': 'Blackjack: Play Like The Pros', 'condition': 'Used-good'}
    # # # itemInfo = {'barcode': '4043972146181', 'title': 'Blackjack: Play Like The Pros', 'condition': 'Used-good'}
    # # itemInfo = {'barcode': '4043972146181', 'title': 'Blackjack: Play Like The Pros', 'condition': 'New'}
    # itemInfo = {'barcode': '', 'title': 'Tomtom XL 340TM', 'condition': 'Used-good'}
    # # itemInfo = {'barcode': '', 'title': 'iphone 4 black', 'condition': 'Used-good'}
    # itemInfo = {'barcode': '', 'title': 'iphone 4 white', 'condition': 'New'}
    # # itemInfo = {'barcode': '', 'title': 'Blackjack: Play Like The Pros', 'condition': 'New'}
    # # itemInfo = {'barcode': '', 'title': 'Blackjack: Play Like The Pros', 'condition': 'Used-good'}
    
    # print itemInfo
    
    cookie = cookielib.CookieJar()   
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    opener.addheaders = [('User-agent', 'Chrome/21.0.1180.57 Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/537.1 (KHTML, like Gecko) Safari/537.1')]
    # opener.addheaders = [('User-agent', 'Chrome/21.0.1180.57')]
    

    if itemInfo.get('barcode', ''):
        barcode = itemInfo['barcode'].lstrip('0');
        if len(barcode)==9 or len(barcode)==11:
            barcode = '0' + barcode #A simple hack to compensate the mistakenly stripped zero for isbn or upc.
        searchUrl = 'http://www.ebay.com/sch/i.html?_nkw='+barcode
    elif itemInfo.get('title', ''):
        searchUrl = ('http://www.ebay.com/sch/i.html?_nkw='+urllib.quote(itemInfo['title'].strip()))
    else:
        return resellValue
   
    condition = 'new'
    #Simplify condition to 'new' and 'used' two levels for now.
    # if 'new' in itemInfo.get('condition', '').lower():
        # condition = 'new'
    # else:
        # condition = 'used'
        
    
    binStr = '&LH_BIN=1'
    matchStr = '&_sop=12'
    locStr = '&LH_PrefLoc=1'
    nItemsStr = '&_ipg=200'
    completedStr = '&LH_Complete=1'
    soldStr = '&LH_Sold=1'
    viewStr = '&_dmd=1' #1 for list view, #2 for gallery view
    condNewStr = '&LH_ItemCondition=3'
    condUsedStr = '&LH_ItemCondition=4'
    # if 'new' in itemInfo.get('condition', '').lower():
        # condUrlStr = '&LH_ItemCondition=3'          
    # else:
        # condUrlStr = '&LH_ItemCondition=4'
        
        
    #Check for condition new first
    queryUrl = matchStr+condNewStr+locStr+nItemsStr+viewStr+completedStr+soldStr
    searchUrl += queryUrl
    searchUrlOrig = searchUrl #Saved for calculating category default value.
    # print searchUrl
    
    req = opener.open(searchUrl) 
    redirUrl = req.geturl()
    # print redirUrl
    recommendedItem = {}
    if '/ctg/' in redirUrl:
        #Get the recommended item
        strHTML = req.read()
        if strHTML:
            recommendedItem['link'] = redirUrl
            root = etree.HTML(strHTML)
            titleTags = root.xpath('//h3[@class="tpc-titr"]')
            if titleTags:
                recommendedItem['title'] = titleTags[0].text
                    
            imgTags = root.xpath('//div[@id="v4-15"]//img')
            # print imgTags
            if imgTags:
                imgUrl = imgTags[0].get('xrc', '')
                # print imgUrl
                if imgUrl:
                    recommendedItem['imgUrl'] = imgUrl
            
            # Category number
            category = ''
            catTags = root.xpath('//li[@itemprop="offers"]/a')
            if catTags:
                category = catTags[0].get('href', '').split('_pcategid=')[-1].split('&')[0]
                # print category
            
            
            # User Category
            userCat = ''
            topCatTags = root.xpath('//meta[@name = "keywords"]')
            if topCatTags:
                topCatStr = topCatTags[0].get('content')
                topCatStr = topCatStr.split(', ebay, listings')[0].split(',')[-1].strip()
                # print topCatStr
                userCat = categoryMap2.get(topCatStr.lower(), '')
                # print userCat
            
     
            
            #Get the brand new and used prices for the recommended item.
            recommendedTags = root.xpath('//table[@class="bb-btbl"]')
            usedFound = 0
            for recommendedTag in recommendedTags:
                conditionStr = ''.join(recommendedTag.xpath('.//div[@class="bb-cd"]//div[@class="bb-rtd"]//text()')).strip()
                # print conditionStr
                if 'brand new' in conditionStr.lower() or conditionStr.lower()[:3] == 'new':
                    priceStr = ''.join(recommendedTag.xpath('.//div[@class="bb-l"]//strong//text()'))
                    # print etree.tostring(recommendedTag.xpath('.//div[@class="bb-l"]')[0])
                    # print priceStr
                    if priceStr:
                        recommendedItem['marketNew'] = float(priceStr.strip().replace('$', '').replace(',',''))
                        # print conditionStr
                        # print recommendedItem['marketNew']
                elif conditionStr.lower() == 'good' or conditionStr.lower() == 'used':
                    usedFound = 1
                    priceStr = ''.join(recommendedTag.xpath('.//div[@class="bb-l"]//strong//text()'))
                    #print etree.tostring(recommendedTag.xpath('.//div[@class="bb-l"]')[0])
                    # print priceStr
                    if priceStr:
                        recommendedItem['marketUsed'] = float(priceStr.strip().replace('$', '').replace(',',''))
                        # print conditionStr
                        # print recommendedItem['marketUsed']
                elif (not usedFound) and ('refurbished' not in conditionStr.lower()):
                    usedFound = 1
                    priceStr = ''.join(recommendedTag.xpath('.//div[@class="bb-l"]//strong//text()'))
                    # print recommendedTag.xpath('.//div[@class="bb-l"]//strong')
                    #print etree.tostring(recommendedTag)
                    # print priceStr
                    if priceStr:
                        recommendedItem['marketUsed'] = float(priceStr.strip().replace('$', '').replace(',',''))
                        # print conditionStr
                        # print recommendedItem['marketUsed']
            #print recommendedItem
                
            pricesUrl = redirUrl + queryUrl.replace('&', '?', 1)
            # print pricesUrl
            req = opener.open(pricesUrl)
            strHTML = req.read()
            # f = open('ebay.html', 'w')
            # f.write(strHTML)
            # f.close()
            if strHTML:
                searchResultNew = parseProductPageSold(strHTML)
            
            # print searchResult
            
            #Search for old condition
            pricesUrl = pricesUrl.replace(condNewStr, condUsedStr)
            req = opener.open(pricesUrl) 
            strHTML = req.read()
            if strHTML:
                searchResultOld = parseProductPageSold(strHTML)
            
            
            
            #If no result found for 'new' items, used 'used' for search instead.
            # if (not searchResult.get('firstPageItems', [])) and (condition == 'new'):
                # # print 'No condition new sold items found, search for used items.'
                # pricesUrl = pricesUrl.replace('&LH_ItemCondition=3', '&LH_ItemCondition=4')
                # # print pricesUrl
                # req = opener.open(pricesUrl) 
                # strHTML = req.read()
                # if strHTML:
                    # searchResult = parseProductPageSold(strHTML)
                    
                    
            # print searchResult
            resellValue['category'] = category
            resellValue['userCat'] = userCat
            resellValue['recommendedItem'] = recommendedItem
            resellValue['firstPageItemsNew'] = searchResultNew.get('firstPageItems', {})
            resellValue['firstPageItemsOld'] = searchResultOld.get('firstPageItems', {})
            if not resellValue['firstPageItemsNew']:
                resellValue['firstPageItemsNew'] = resellValue['firstPageItemsOld']
            # Always get the new title from the product page function.
            resellValue['title'] = recommendedItem.get('title', '')
            # if itemInfo.get('title'):
                # resellValue['title'] = itemInfo['title']
            # else:
                # resellValue['title'] = recommendedItem.get('title', '')
                
            resellValue['resellNew'] = searchResultNew.get('resellPrice',  0)
            resellValue['resellOld'] = searchResultOld.get('resellPrice',  0)
            if not resellValue['resellNew']:
                resellValue['resellNew'] = resellValue['resellOld'] 
            
            # if searchResult.get('resellPrice', 0):
                # if condition == 'new':
                    # resellValue['resellNew'] = searchResult['resellPrice']

                    # # if recommendedItem.get('marketNew', 0) and recommendedItem.get('marketNew', 0)<resellValue['resellNew']:
                        # # resellValue['resellNew'] = recommendedItem['marketNew']
                # else:
                    # resellValue['resellUsed'] = searchResult['resellPrice']

                    # if recommendedItem.get('marketUsed', 0) and recommendedItem.get('marketUsed', 0)<resellValue['resellUsed']:
                        # resellValue['resellUsed'] = recommendedItem['marketUsed']
            
            # print resellValue
     
    # else:
        # #print 'I am here'
        # # Log in to ebay
        # cookie = cookielib.CookieJar()   
        # opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
        # opener.addheaders = [('User-agent', 'Chrome/21.0.1180.57 Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/537.1 (KHTML, like Gecko) Safari/537.1')]
        # # opener.addheaders = [('User-agent', 'Chrome/21.0.1180.57')]
    
        
        # category = ''
        # if itemInfo.get('title', ''):
            # categories, opener = queryCategory(itemInfo['title'].strip())
        # elif itemInfo.get('barcode', ''):
            # categories, opener = queryCategory(barcode)
        # if categories:
            # category = categories[0][0]
        # # print category
            
        # # ebayCred = operation3.getDBLogin('ebaydealsea')
        # # log = {'MfcISAPICommand': 'SignInWelcome', 'co_partnerId': 502, 'userid': ebayCred['username'], 'pass': ebayCred['password']}
        # # signUrl = 'https://signin.ebay.com/ws/eBayISAPI.dll'
        # # login_data = urllib.urlencode(log)
        # # req = opener.open(signUrl)
        # # req = opener.open(signUrl, login_data)
        # # category = ''
        # # if 'accountsummary' in req.url.lower():
            # # catSearchStr = '&cpg=4&aid=4&keywords='+urllib.quote(itemInfo['title'].strip())
            # # catSearchUrl = 'http://cgi5.ebay.com/ws/eBayISAPI.dll?NewListing'+catSearchStr
            # # req = opener.open(catSearchUrl)
            # # strHTML = req.read()
            # # root = etree.HTML(strHTML)
            # # optionTags = root.xpath('//div[@id="cat1_inp"]//option')
            # # #print optionTags
            # # if optionTags:
                # # category = optionTags[0].get('value', '')
                # # print optionTags[0].text
        # # print 'Category: ' + category
        # searchUrl = searchUrl.replace('sch/', 'sch/'+category+'/')
        # req = opener.open(searchUrl)



        # # print req.url






        # strHTML = req.read()
                
        # # f = open('ebay.html', 'w')
        # # f.write(strHTML)
        # # f.close()
        


        # searchResult = parseCompletedPage(strHTML, req.url)        
        # #If no result found for 'new' items, used 'used' for search instead.
        # if (not searchResult.get('firstPageItems', [])) and (condition == 'new'):
            # # print 'No condition new sold items found, search for used items.'
            # searchUrl = searchUrl.replace('&LH_ItemCondition=3', '&LH_ItemCondition=4')
            # # print searchUrl
            # req = opener.open(searchUrl) 
            # strHTML = req.read()
            # if strHTML:
                # searchResult = parseCompletedPage(strHTML, req.url) 

        # # print 'searchResult:'
        # # print searchResult
        # resellValue['category'] = category
        # resellValue['userCat'] = searchResult.get('userCat', '')
        # resellValue['recommendedItem'] = {}
        # resellValue['firstPageItems'] = searchResult.get('firstPageItems', [])
        # if itemInfo.get('title', ''):
            # resellValue['title'] = itemInfo['title']
        # elif itemInfo.get('barcode', '') and len(resellValue['firstPageItems']):
            # resellValue['title'] = resellValue['firstPageItems'][0]['title']
        # if searchResult.get('resellPrice', 0):
            # if 'new' in itemInfo.get('condition', '').lower():
                # resellValue['resellNew'] = searchResult['resellPrice']
                # # if recommendedItem.get('marketNew', 0) and recommendedItem.get('marketNew', 0)<resellValue['resellNew']:
                    # # resellValue['resellNew'] = recommendedItem['marketNew']
            # else:
                # resellValue['resellUsed'] = searchResult['resellPrice']
                # # if recommendedItem.get('marketUsed', 0) and recommendedItem.get('marketUsed', 0)<resellValue['resellUsed']:
                    # # resellValue['resellUsed'] = recommendedItem['marketUsed']
    
    #Get the range for New:
    newSoldFound = True
    Nitems = len(resellValue.get('firstPageItemsNew', {}))
    # print 'Sold items: %d' % Nitems
    sortedItems = sorted(resellValue['firstPageItemsNew'], key=lambda d: (d.get('marketNew', 0)+d.get('marketUsed',0)))
    if Nitems:
        if Nitems > 1:
            pointLow = min(float(Nitems-1)/4, 1)*0.25
            pointHigh = 0.75
            # pointExp = 0.25+ max(min(float(Nitems-10)/90, 1), 0)*0.125
            pointExp = 0.25
            pricePerLow = operation3.percentile(sortedItems, pointLow, key=lambda d: (d.get('marketNew', 0)+d.get('marketUsed',0)))*0.75
            pricePerExp = operation3.percentile(sortedItems, pointExp, key=lambda d: (d.get('marketNew', 0)+d.get('marketUsed',0)))
            pricePerHigh = operation3.percentile(sortedItems, pointHigh, key=lambda d: (d.get('marketNew', 0)+d.get('marketUsed',0)))
            resellValue['rangeLowNew'] = (pricePerLow-3)*0.8
            resellValue['rangeHighNew'] = (pricePerHigh-3)*0.8
            resellValue['expectationNew'] = (pricePerExp-3)*0.8
            if (resellValue['rangeHighNew']-resellValue['expectationNew'])>(resellValue['expectationNew']-resellValue['rangeLowNew'])*2:
                resellValue['rangeHighNew'] = resellValue['rangeLowNew']+(resellValue['expectationNew']-resellValue['rangeLowNew'])*3
            # print 'pointLow: %.2f, %.2f' % (pointLow, resellValue['rangeLow'])
            # print 'pointHigh: %.2f, %.2f' % (pointHigh, resellValue['rangeHigh'])
            # print 'pointExp: %.2f, %.2f' % (pointExp, resellValue['expectation'])
        else:
            resellValue['rangeHighNew'] = (sortedItems[0].get('marketNew', 0)+sortedItems[0].get('marketUsed', 0)-3)*0.8
            resellValue['rangeLowNew'] = (sortedItems[0].get('marketNew', 0)+sortedItems[0].get('marketUsed', 0)-3)*0.8*0.5
            resellValue['expectationNew'] = (sortedItems[0].get('marketNew', 0)+sortedItems[0].get('marketUsed', 0)-3)*0.8*2/3
            # print 'pointLow: %.2f' % (resellValue['rangeLow'])
            # print 'pointHigh: %.2f' % (resellValue['rangeHigh'])
            # print 'pointExp: %.2f' % (resellValue['expectation'])
        
        # if 'new' in itemInfo.get('condition', '').lower():
            # # print 'listNew: 0.5, %.2f' % resellValue.get('resellNew', 0)
            # pass
        # else:
            # # print 'listUsed: 0.5, %.2f' % resellValue.get('resellUsed', 0)
            # pass
    else: 
        newSoldFound = False

      
    #Get the range for Old:
    Nitems = len(resellValue.get('firstPageItemsOld', {}))
    # print 'Sold items: %d' % Nitems
    sortedItems = sorted(resellValue['firstPageItemsOld'], key=lambda d: (d.get('marketNew', 0)+d.get('marketUsed',0)))
    if Nitems:
        if Nitems > 1:
            pointLow = min(float(Nitems-1)/4, 1)*0.25
            pointHigh = 0.75
            # pointExp = 0.25+ max(min(float(Nitems-10)/90, 1), 0)*0.125
            pointExp = 0.25
            pricePerLow = operation3.percentile(sortedItems, pointLow, key=lambda d: (d.get('marketNew', 0)+d.get('marketUsed',0)))*0.75
            pricePerExp = operation3.percentile(sortedItems, pointExp, key=lambda d: (d.get('marketNew', 0)+d.get('marketUsed',0)))
            pricePerHigh = operation3.percentile(sortedItems, pointHigh, key=lambda d: (d.get('marketNew', 0)+d.get('marketUsed',0)))
            resellValue['rangeLowOld'] = (pricePerLow-3)*0.8
            resellValue['rangeHighOld'] = (pricePerHigh-3)*0.8
            resellValue['expectationOld'] = (pricePerExp-3)*0.8
            if (resellValue['rangeHighOld']-resellValue['expectationOld'])>(resellValue['expectationOld']-resellValue['rangeLowOld'])*2:
                resellValue['rangeHighOld'] = resellValue['rangeLowOld']+(resellValue['expectationOld']-resellValue['rangeLowOld'])*3
            # print 'pointLow: %.2f, %.2f' % (pointLow, resellValue['rangeLow'])
            # print 'pointHigh: %.2f, %.2f' % (pointHigh, resellValue['rangeHigh'])
            # print 'pointExp: %.2f, %.2f' % (pointExp, resellValue['expectation'])
        else:
            resellValue['rangeHighOld'] = (sortedItems[0].get('marketNew', 0)+sortedItems[0].get('marketUsed', 0)-3)*0.8
            resellValue['rangeLowOld'] = (sortedItems[0].get('marketNew', 0)+sortedItems[0].get('marketUsed', 0)-3)*0.8*0.5
            resellValue['expectationOld'] = (sortedItems[0].get('marketNew', 0)+sortedItems[0].get('marketUsed', 0)-3)*0.8*2/3
            # print 'pointLow: %.2f' % (resellValue['rangeLow'])
            # print 'pointHigh: %.2f' % (resellValue['rangeHigh'])
            # print 'pointExp: %.2f' % (resellValue['expectation'])
        
        # if 'new' in itemInfo.get('condition', '').lower():
            # # print 'listNew: 0.5, %.2f' % resellValue.get('resellNew', 0)
            # pass
        # else:
            # # print 'listUsed: 0.5, %.2f' % resellValue.get('resellUsed', 0)
            # pass
                
        
                   
    else:
        #Get category default values if the search cannot find a match.
        if resellValue.get('category', ''):
            #print resellValue
            #Get the url for all items inside the category
            #Here the condition in searchUrl is old. ToDo: make it more explicit and clear.
            searchUrl = (searchUrlOrig.split('_nkw', 1)[0]+searchUrlOrig.split('_nkw', 1)[-1].split('&', 1)[-1]).replace('sch/', 'sch/'+category+'/')
            req = opener.open(searchUrl)
            # print req.url
            strHTML = req.read()
                    
            # f = open('ebay.html', 'w')
            # f.write(strHTML)
            # f.close()
            
            searchResult = parseCompletedPage(strHTML, req.url)  
            resellValue['resellUsed'] = searchResult.get('resellPrice', 0)
            if not newSoldFound:
                resellValue['resellNew']  =  resellValue['resellOld']  
     
            # if searchResult.get('resellPrice', 0):
                # if 'new' in itemInfo.get('condition', '').lower():
                    # resellValue['resellNew'] = searchResult['resellPrice']
                # else:
                    # resellValue['resellUsed'] = searchResult['resellPrice']
                    
            Nitems = len(searchResult.get('firstPageItems', []))
            # print 'Default items in category: %d' % Nitems
            if Nitems:
                resellValue['default'] = 1;
                sortedItems = sorted(searchResult['firstPageItems'], key=lambda d: (d.get('marketNew', 0)+d.get('marketUsed',0)))
                pointExp = 0.25
                pricePerExp = operation3.percentile(sortedItems, pointExp, key=lambda d: (d.get('marketNew', 0)+d.get('marketUsed',0)))
                # print pointExp
                resellValue['rangeHighOld'] = (pricePerExp-3)*0.8*1.5
                resellValue['rangeLowOld'] = (pricePerExp-3)*0.8*0.75
                resellValue['expectationOld'] = (pricePerExp-3)*0.8
                # print 'pointLow: %.2f' % (resellValue['rangeLow'])
                # print 'pointHigh: %.2f' % (resellValue['rangeHigh'])
                # print 'pointExp: %.2f' % (resellValue['expectation'])
                
                # if 'new' in itemInfo.get('condition', '').lower():
                    # print 'listNew: 0.5, %.2f' % resellValue.get('resellNew', 0)
                # else:

                    # print 'listUsed: 0.5, %.2f' % resellValue.get('resellUsed', 0)
            
            # print searchResult
                
    # print newSoldFound
    if not newSoldFound:
        resellValue['rangeHighNew'] = resellValue.get('rangeHighOld', 0)
        resellValue['rangeLowNew'] = resellValue.get('rangeLowOld', 0)
        resellValue['expectationNew'] = resellValue.get('expectationOld', 0)





        # print resellValue
            
            
        # f = open('ebay.html', 'w')
        # f.write(strHTML)
        # f.close()

    
    return resellValue
            
##End of queryPriceAllCond(itemInfo)
         
         
#http://www.ebay.com/sch/i.html?_nkw=the+davinci+code&_sop=12
#&_sop=12 means best match; &LH_BIN=1 means buy it now; &LH_ItemCondition=4 means used, 3 means new; LH_PreFloc=1 means US Only
#on productised item page. ?&tabs=15 for all items. &LH_BIN=1 for buy it now
def queryPrice(itemInfo):
#search for best matched price to sell on ebay
#itemInfo is dict with keys: barcode, title, condition
#Jiong 20140716: Added condition='mixed' and passed-in category number.

    resellValue = {}
    
    # opener = urllib2.build_opener(urllib2.HTTPRedirectHandler)
    
    # itemInfo = {'barcode': '0818406569', 'title': 'Blackjack: Play Like The Pros', 'condition': 'Used-good'}
    # itemInfo = {'barcode': '0321611136', 'title': 'Blackjack: Play Like The Pros', 'condition': 'Used-good'}
    # # # itemInfo = {'barcode': '4043972146181', 'title': 'Blackjack: Play Like The Pros', 'condition': 'Used-good'}
    # # itemInfo = {'barcode': '4043972146181', 'title': 'Blackjack: Play Like The Pros', 'condition': 'New'}
    # itemInfo = {'barcode': '', 'title': 'Tomtom XL 340TM', 'condition': 'Used-good'}
    # # itemInfo = {'barcode': '', 'title': 'iphone 4 black', 'condition': 'Used-good'}
    # itemInfo = {'barcode': '', 'title': 'iphone 4 white', 'condition': 'New'}
    # # itemInfo = {'barcode': '', 'title': 'Blackjack: Play Like The Pros', 'condition': 'New'}
    # # itemInfo = {'barcode': '', 'title': 'Blackjack: Play Like The Pros', 'condition': 'Used-good'}
    
    # print itemInfo
    
    cookie = cookielib.CookieJar()   
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    opener.addheaders = [('User-agent', 'Chrome/21.0.1180.57 Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/537.1 (KHTML, like Gecko) Safari/537.1')]
    # opener.addheaders = [('User-agent', 'Chrome/21.0.1180.57')]
    

    if itemInfo.get('barcode', ''):
        barcode = itemInfo['barcode'].lstrip('0');
        if len(barcode)==9 or len(barcode)==11:
            barcode = '0' + barcode #A simple hack to compensate the mistakenly stripped zero for isbn or upc.
        searchUrl = 'http://www.ebay.com/sch/i.html?_nkw='+barcode
    elif itemInfo.get('title', ''):
        searchUrl = ('http://www.ebay.com/sch/i.html?_nkw='+urllib.quote(itemInfo['title'].strip()))
    else:
        return resellValue
   
    #Simplify condition to 'free' and 'used' two levels for now.
    if 'new' in itemInfo.get('condition', '').lower():
        condition = 'new'
    elif 'mixed' in itemInfo.get('condition', '').lower():
        condition = 'mixed'
    else:
        condition = 'used'
        
    #Get category from itemInfo
    category = itemInfo.get('category', '')
    
    
    binStr = '&LH_BIN=1'
    matchStr = '&_sop=12'
    locStr = '&LH_PrefLoc=1'
    nItemsStr = '&_ipg=200'
    completedStr = '&LH_Complete=1'
    soldStr = '&LH_Sold=1'
    viewStr = '&_dmd=1' #1 for list view, #2 for gallery view
    if condition == 'new':
        condUrlStr = '&LH_ItemCondition=3'    
    elif condition == 'mixed':
        condUrlStr = ''
    else:
        condUrlStr = '&LH_ItemCondition=4'
    if not itemInfo.get('listingStatus', '').lower() == 'active':
        queryUrl = matchStr+condUrlStr+locStr+nItemsStr+viewStr+completedStr+soldStr
    else :
        queryUrl = matchStr+condUrlStr+locStr+nItemsStr+viewStr
    searchUrl += queryUrl
    searchUrlOrig = searchUrl #Saved for calculating category default value.
    searchUrl = searchUrl.replace('sch/', 'sch/'+category+'/')
    
    # print searchUrl
    
    req = opener.open(searchUrl) 
    redirUrl = req.geturl()
    # print redirUrl
    recommendedItem = {}
    if '/ctg/' in redirUrl:
        #Get the recommended item
        strHTML = req.read()
        if strHTML:
            recommendedItem['link'] = redirUrl
            root = etree.HTML(strHTML)
            titleTags = root.xpath('//h3[@class="tpc-titr"]')
            if titleTags:
                recommendedItem['title'] = titleTags[0].text
                    
            imgTags = root.xpath('//div[@id="v4-15"]//img')
            # print imgTags
            if imgTags:
                imgUrl = imgTags[0].get('xrc', '')
                # print imgUrl
                if imgUrl:
                    recommendedItem['imgUrl'] = imgUrl
            
            # Category number
            catTags = root.xpath('//li[@itemprop="offers"]/a')
            if catTags:
                category = catTags[0].get('href', '').split('_pcategid=')[-1].split('&')[0]
                # print category
            
            
            # User Category
            userCat = ''
            topCatTags = root.xpath('//meta[@name = "keywords"]')
            if topCatTags:
                topCatStr = topCatTags[0].get('content')
                topCatStr = topCatStr.split(', ebay, listings')[0].split(',')[-1].strip()
                # print topCatStr
                userCat = categoryMap2.get(topCatStr.lower(), '')
                # print userCat
            
     
            
            #Get the brand new and used prices for the recommended item.
            recommendedTags = root.xpath('//table[@class="bb-btbl"]')
            usedFound = 0
            for recommendedTag in recommendedTags:
                conditionStr = ''.join(recommendedTag.xpath('.//div[@class="bb-cd"]//div[@class="bb-rtd"]//text()')).strip()
                # print conditionStr
                if 'brand new' in conditionStr.lower() or conditionStr.lower()[:3] == 'new':
                    priceStr = ''.join(recommendedTag.xpath('.//div[@class="bb-l"]//strong//text()'))
                    # print etree.tostring(recommendedTag.xpath('.//div[@class="bb-l"]')[0])
                    # print priceStr
                    if priceStr:
                        recommendedItem['marketNew'] = float(priceStr.strip().replace('$', '').replace(',',''))
                        # print conditionStr
                        # print recommendedItem['marketNew']
                elif conditionStr.lower() == 'good' or conditionStr.lower() == 'used':
                    usedFound = 1
                    priceStr = ''.join(recommendedTag.xpath('.//div[@class="bb-l"]//strong//text()'))
                    #print etree.tostring(recommendedTag.xpath('.//div[@class="bb-l"]')[0])
                    # print priceStr
                    if priceStr:
                        recommendedItem['marketUsed'] = float(priceStr.strip().replace('$', '').replace(',',''))
                        # print conditionStr
                        # print recommendedItem['marketUsed']
                elif (not usedFound) and ('refurbished' not in conditionStr.lower()):
                    usedFound = 1
                    priceStr = ''.join(recommendedTag.xpath('.//div[@class="bb-l"]//strong//text()'))
                    # print recommendedTag.xpath('.//div[@class="bb-l"]//strong')
                    #print etree.tostring(recommendedTag)
                    # print priceStr
                    if priceStr:
                        recommendedItem['marketUsed'] = float(priceStr.strip().replace('$', '').replace(',',''))
                        # print conditionStr
                        # print recommendedItem['marketUsed']
            #print recommendedItem
                
            pricesUrl = redirUrl + queryUrl.replace('&', '?', 1)
            # print pricesUrl
            req = opener.open(pricesUrl)
            strHTML = req.read()
            
            searchResult = parseProductPageSold(strHTML)
            #If no result found for 'new' items, used 'used' for search instead.
            if (not searchResult.get('firstPageItems', [])) and (condition == 'new'):
                # print 'No condition new sold items found, search for used items.'
                pricesUrl = pricesUrl.replace('&LH_ItemCondition=3', '&LH_ItemCondition=4')
                # print pricesUrl
                req = opener.open(pricesUrl) 
                strHTML = req.read()
                if strHTML:
                    searchResult = parseProductPageSold(strHTML)
            # print searchResult
            resellValue['category'] = category
            resellValue['userCat'] = userCat
            resellValue['recommendedItem'] = recommendedItem
            resellValue['firstPageItems'] = searchResult.get('firstPageItems', {})
            # Always get the new title from the product page function.
            resellValue['title'] = recommendedItem.get('title', '')
            # if itemInfo.get('title'):
                # resellValue['title'] = itemInfo['title']
            # else:
                # resellValue['title'] = recommendedItem.get('title', '')
            if searchResult.get('resellPrice', 0):
                if condition == 'new':
                    resellValue['resellNew'] = searchResult['resellPrice']
                    # if recommendedItem.get('marketNew', 0) and recommendedItem.get('marketNew', 0)<resellValue['resellNew']:
                        # resellValue['resellNew'] = recommendedItem['marketNew']
                elif condition == 'mixed':
                    resellValue['resellMixed'] = searchResult['resellPrice']
                    # if recommendedItem.get('marketMixed', 0) and recommendedItem.get('marketMixed', 0)<resellValue['resellMixed']:
                        # resellValue['resellMixed'] = recommendedItem['marketMixed']
                else:
                    resellValue['resellUsed'] = searchResult['resellPrice']
                    # if recommendedItem.get('marketUsed', 0) and recommendedItem.get('marketUsed', 0)<resellValue['resellUsed']:
                        # resellValue['resellUsed'] = recommendedItem['marketUsed']
            
            # print resellValue
     
    else:
        # #print 'I am here'
        # # Log in to ebay
        # cookie = cookielib.CookieJar()   
        # opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
        # opener.addheaders = [('User-agent', 'Chrome/21.0.1180.57 Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/537.1 (KHTML, like Gecko) Safari/537.1')]
        # # opener.addheaders = [('User-agent', 'Chrome/21.0.1180.57')]
    
        
        if not category:
            if itemInfo.get('title', ''):
                categories, opener = queryCategory(itemInfo['title'].strip())
            elif itemInfo.get('barcode', ''):
                categories, opener = queryCategory(barcode)
            if categories:
                category = categories[0][0]
            searchUrl = searchUrl.replace('sch/', 'sch/'+category+'/')
            req = opener.open(searchUrl)
        # print category
            
        # ebayCred = operation3.getDBLogin('ebaydealsea')
        # log = {'MfcISAPICommand': 'SignInWelcome', 'co_partnerId': 502, 'userid': ebayCred['username'], 'pass': ebayCred['password']}
        # signUrl = 'https://signin.ebay.com/ws/eBayISAPI.dll'
        # login_data = urllib.urlencode(log)
        # req = opener.open(signUrl)
        # req = opener.open(signUrl, login_data)
        # category = ''
        # if 'accountsummary' in req.url.lower():
            # catSearchStr = '&cpg=4&aid=4&keywords='+urllib.quote(itemInfo['title'].strip())
            # catSearchUrl = 'http://cgi5.ebay.com/ws/eBayISAPI.dll?NewListing'+catSearchStr
            # req = opener.open(catSearchUrl)
            # strHTML = req.read()
            # root = etree.HTML(strHTML)
            # optionTags = root.xpath('//div[@id="cat1_inp"]//option')
            # #print optionTags
            # if optionTags:
                # category = optionTags[0].get('value', '')
                # print optionTags[0].text
        # print 'Category: ' + category



        # print req.url






        strHTML = req.read()
                
        # f = open('ebay.html', 'w')
        # f.write(strHTML)
        # f.close()
        


        searchResult = parseCompletedPage(strHTML, req.url)        
        #If no result found for 'new' items, used 'used' for search instead.
        if (not searchResult.get('firstPageItems', [])) and (condition == 'new'):
            # print 'No condition new sold items found, search for used items.'
            searchUrl = searchUrl.replace('&LH_ItemCondition=3', '&LH_ItemCondition=4')
            # print searchUrl
            req = opener.open(searchUrl) 
            strHTML = req.read()
            if strHTML:
                searchResult = parseCompletedPage(strHTML, req.url) 

        # print 'searchResult:'
        # print searchResult
        resellValue['category'] = category
        resellValue['userCat'] = searchResult.get('userCat', '')
        resellValue['recommendedItem'] = {}
        resellValue['firstPageItems'] = searchResult.get('firstPageItems', [])
        if itemInfo.get('title', ''):
            resellValue['title'] = itemInfo['title']
        elif itemInfo.get('barcode', '') and len(resellValue['firstPageItems']):
            resellValue['title'] = resellValue['firstPageItems'][0]['title']
        if searchResult.get('resellPrice', 0):
            if 'new' in itemInfo.get('condition', '').lower():
                resellValue['resellNew'] = searchResult['resellPrice']
                # if recommendedItem.get('marketNew', 0) and recommendedItem.get('marketNew', 0)<resellValue['resellNew']:
                    # resellValue['resellNew'] = recommendedItem['marketNew']
            if 'mixed' in itemInfo.get('condition', '').lower():
                resellValue['resellMixed'] = searchResult['resellPrice']
                # if recommendedItem.get('marketMixed', 0) and recommendedItem.get('marketMixed', 0)<resellValue['resellMixed']:
                    # resellValue['resellMixed'] = recommendedItem['marketMixed']
            else:
                resellValue['resellUsed'] = searchResult['resellPrice']
                # if recommendedItem.get('marketUsed', 0) and recommendedItem.get('marketUsed', 0)<resellValue['resellUsed']:
                    # resellValue['resellUsed'] = recommendedItem['marketUsed']
    
    #Get the range:
    Nitems = len(resellValue.get('firstPageItems', {}))
    # print 'Sold items: %d' % Nitems
    sortedItems = sorted(resellValue['firstPageItems'], key=lambda d: (d.get('marketNew', 0)+d.get('marketUsed',0)+d.get('market',0)))
    # print sortedItems
    if Nitems:
        if Nitems > 1:
            pointLow = min(float(Nitems-1)/4, 1)*0.25
            pointHigh = 0.75
            # pointExp = 0.25+ max(min(float(Nitems-10)/90, 1), 0)*0.125
            pointExp = 0.25
            pricePerLow = operation3.percentile(sortedItems, pointLow, key=lambda d: (d.get('marketNew', 0)+d.get('marketUsed',0)+d.get('market',0)))*0.75
            pricePerExp = operation3.percentile(sortedItems, pointExp, key=lambda d: (d.get('marketNew', 0)+d.get('marketUsed',0)+d.get('market',0)))
            pricePerHigh = operation3.percentile(sortedItems, pointHigh, key=lambda d: (d.get('marketNew', 0)+d.get('marketUsed',0)+d.get('market',0)))
            # print pricePerHigh
            # print pricePerLow
            # print pricePerExp
            resellValue['rangeLow'] = (pricePerLow-3)*0.8
            resellValue['rangeHigh'] = (pricePerHigh-3)*0.8
            resellValue['expectation'] = (pricePerExp-3)*0.8
            if (resellValue['rangeHigh']-resellValue['expectation'])>(resellValue['expectation']-resellValue['rangeLow'])*2:
                resellValue['rangeHigh'] = resellValue['rangeLow']+(resellValue['expectation']-resellValue['rangeLow'])*3
            # print 'pointLow: %.2f, %.2f' % (pointLow, resellValue['rangeLow'])
            # print 'pointHigh: %.2f, %.2f' % (pointHigh, resellValue['rangeHigh'])
            # print 'pointExp: %.2f, %.2f' % (pointExp, resellValue['expectation'])
        else:
            resellValue['rangeHigh'] = (sortedItems[0].get('marketNew', 0)+sortedItems[0].get('marketUsed', 0)+sortedItems[0].get('market', 0)-3)*0.8
            resellValue['rangeLow'] = (sortedItems[0].get('marketNew', 0)+sortedItems[0].get('marketUsed', 0)+sortedItems[0].get('market', 0)-3)*0.8*0.5
            resellValue['expectation'] = (sortedItems[0].get('marketNew', 0)+sortedItems[0].get('marketUsed', 0)+sortedItems[0].get('market', 0)-3)*0.8*2/3
            # print 'pointLow: %.2f' % (resellValue['rangeLow'])
            # print 'pointHigh: %.2f' % (resellValue['rangeHigh'])
            # print 'pointExp: %.2f' % (resellValue['expectation'])
        
        # if 'new' in itemInfo.get('condition', '').lower():
            # # print 'listNew: 0.5, %.2f' % resellValue.get('resellNew', 0)
            # pass
        # else:
            # # print 'listUsed: 0.5, %.2f' % resellValue.get('resellUsed', 0)
            # pass
                
        
                   
    else:
        #Get category default values if the search cannot find a match.
        if resellValue.get('category', ''):
            #print resellValue
            #Get the url for all items inside the category
            searchUrl = (searchUrlOrig.split('_nkw', 1)[0]+searchUrlOrig.split('_nkw', 1)[-1].split('&', 1)[-1]).replace('sch/', 'sch/'+category+'/')
            req = opener.open(searchUrl)
            # print req.url
            strHTML = req.read()
                    
            # f = open('ebay.html', 'w')
            # f.write(strHTML)
            # f.close()
            
            searchResult = parseCompletedPage(strHTML, req.url)  
            if searchResult.get('resellPrice', 0):
                if 'new' in itemInfo.get('condition', '').lower():
                    resellValue['resellNew'] = searchResult['resellPrice']
                else:
                    resellValue['resellUsed'] = searchResult['resellPrice']
                    
            Nitems = len(searchResult.get('firstPageItems', []))
            # print 'Default items in category: %d' % Nitems
            if Nitems:
                resellValue['default'] = 1;
                sortedItems = sorted(searchResult['firstPageItems'], key=lambda d: (d.get('marketNew', 0)+d.get('marketUsed',0)+d.get('market',0)))
                pointExp = 0.25
                pricePerExp = operation3.percentile(sortedItems, pointExp, key=lambda d: (d.get('marketNew', 0)+d.get('marketUsed',0)+d.get('market',0)))
                # print pointExp
                resellValue['rangeHigh'] = (pricePerExp-3)*0.8*1.5
                resellValue['rangeLow'] = (pricePerExp-3)*0.8*0.75
                resellValue['expectation'] = (pricePerExp-3)*0.8
                # print 'pointLow: %.2f' % (resellValue['rangeLow'])
                # print 'pointHigh: %.2f' % (resellValue['rangeHigh'])
                # print 'pointExp: %.2f' % (resellValue['expectation'])
                
                # if 'new' in itemInfo.get('condition', '').lower():
                    # print 'listNew: 0.5, %.2f' % resellValue.get('resellNew', 0)
                # else:

                    # print 'listUsed: 0.5, %.2f' % resellValue.get('resellUsed', 0)
            
            # print searchResult
                





        # print resellValue
            
            
        # f = open('ebay.html', 'w')
        # f.write(strHTML)
        # f.close()

    
    return resellValue
            
##End of queryPrice(itemInfo)


#http://www.ebay.com/sch/i.html?_nkw=the+davinci+code&_sop=12
#&_sop=12 means best match; &LH_BIN=1 means buy it now; &LH_ItemCondition=4 means used, 3 means new; LH_PreFloc=1 means US Only
#on productised item page. ?&tabs=15 for all items. &LH_BIN=1 for buy it now
def queryPriceActive(itemInfo):
#search for best matched price to sell on ebay
#itemInfo is dict with keys: barcode, title, condition
#

    resellValue = {}
    
    # opener = urllib2.build_opener(urllib2.HTTPRedirectHandler)
    
    # itemInfo = {'barcode': '0818406569', 'title': 'Blackjack: Play Like The Pros', 'condition': 'Used-good'}
    # itemInfo = {'barcode': '0321611136', 'title': 'Blackjack: Play Like The Pros', 'condition': 'Used-good'}
    # # # itemInfo = {'barcode': '4043972146181', 'title': 'Blackjack: Play Like The Pros', 'condition': 'Used-good'}
    # # itemInfo = {'barcode': '4043972146181', 'title': 'Blackjack: Play Like The Pros', 'condition': 'New'}
    # itemInfo = {'barcode': '', 'title': 'Tomtom XL 340TM', 'condition': 'Used-good'}
    # # itemInfo = {'barcode': '', 'title': 'iphone 4 black', 'condition': 'Used-good'}
    # itemInfo = {'barcode': '', 'title': 'iphone 4 white', 'condition': 'New'}
    # # itemInfo = {'barcode': '', 'title': 'Blackjack: Play Like The Pros', 'condition': 'New'}
    # # itemInfo = {'barcode': '', 'title': 'Blackjack: Play Like The Pros', 'condition': 'Used-good'}
    
    # print itemInfo
    
    cookie = cookielib.CookieJar()   
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    opener.addheaders = [('User-agent', 'Chrome/21.0.1180.57 Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/537.1 (KHTML, like Gecko) Safari/537.1')]
    # opener.addheaders = [('User-agent', 'Chrome/21.0.1180.57')]
    

    if itemInfo.get('barcode', ''):
        barcode = itemInfo['barcode'].lstrip('0');
        if len(barcode)==9 or len(barcode)==11:
            barcode = '0' + barcode #A simple hack to compensate the mistakenly stripped zero for isbn or upc.
        searchUrl = 'http://www.ebay.com/sch/i.html?_nkw='+barcode
    elif itemInfo.get('title', ''):
        searchUrl = ('http://www.ebay.com/sch/i.html?_nkw='+urllib.quote(itemInfo['title'].strip()))
    else:
        return resellValue
   
    
    binStr = '&LH_BIN=1'
    matchStr = '&_sop=12'
    locStr = '&LH_PrefLoc=1'
    nItemsStr = '&_ipg=200'
    viewStr = '&_dmd=1' #1 for list view, #2 for gallery view
    if 'new' in itemInfo.get('condition', '').lower():
        condUrlStr = '&LH_ItemCondition=3'          
    else:
        condUrlStr = '&LH_ItemCondition=4'
    queryUrl = matchStr+binStr+condUrlStr+locStr+nItemsStr+viewStr
    searchUrl += queryUrl
    # print searchUrl
    
    req = opener.open(searchUrl) 
    redirUrl = req.geturl()
    #print redirUrl
    recommendedItem = {}
    if '/ctg/' in redirUrl:
        #Get the recommended item
        strHTML = req.read()
        if strHTML:
            recommendedItem['link'] = redirUrl
            root = etree.HTML(strHTML)
            titleTags = root.xpath('//h3[@class="tpc-titr"]')
            if titleTags:
                recommendedItem['title'] = titleTags[0].text
                    
            imgTags = root.xpath('//div[@id="v4-15"]//img')
            # print imgTags
            if imgTags:
                imgUrl = imgTags[0].get('xrc', '')
                # print imgUrl
                if imgUrl:
                    recommendedItem['imgUrl'] = imgUrl
            
            # Category number
            category = ''
            catTags = root.xpath('//li[@itemprop="offers"]/a')
            if catTags:
                category = catTags[0].get('href', '').split('_pcategid=')[-1].split('&')[0]
                # print category
            
            
            
            #Get the brand new and used prices for the recommended item.
            recommendedTags = root.xpath('//table[@class="bb-btbl"]')
            usedFound = 0
            for recommendedTag in recommendedTags:
                conditionStr = ''.join(recommendedTag.xpath('.//div[@class="bb-cd"]//div[@class="bb-rtd"]//text()')).strip()
                # print conditionStr
                if 'brand new' in conditionStr.lower() or conditionStr.lower()[:3] == 'new':
                    priceStr = ''.join(recommendedTag.xpath('.//div[@class="bb-l"]//strong//text()'))
                    # print etree.tostring(recommendedTag.xpath('.//div[@class="bb-l"]')[0])
                    # print priceStr
                    if priceStr:
                        recommendedItem['marketNew'] = float(priceStr.strip().replace('$', '').replace(',',''))
                        # print conditionStr
                        # print recommendedItem['marketNew']
                elif conditionStr.lower() == 'good' or conditionStr.lower() == 'used':
                    usedFound = 1
                    priceStr = ''.join(recommendedTag.xpath('.//div[@class="bb-l"]//strong//text()'))
                    #print etree.tostring(recommendedTag.xpath('.//div[@class="bb-l"]')[0])
                    # print priceStr
                    if priceStr:
                        recommendedItem['marketUsed'] = float(priceStr.strip().replace('$', '').replace(',',''))
                        # print conditionStr
                        # print recommendedItem['marketUsed']
                elif (not usedFound) and ('refurbished' not in conditionStr.lower()):
                    usedFound = 1
                    priceStr = ''.join(recommendedTag.xpath('.//div[@class="bb-l"]//strong//text()'))
                    # print recommendedTag.xpath('.//div[@class="bb-l"]//strong')
                    #print etree.tostring(recommendedTag)
                    # print priceStr
                    if priceStr:
                        recommendedItem['marketUsed'] = float(priceStr.strip().replace('$', '').replace(',',''))
                        # print conditionStr
                        # print recommendedItem['marketUsed']
            #print recommendedItem
                
            pricesUrl = redirUrl + queryUrl.replace('&', '?', 1)
            # print pricesUrl
            req = opener.open(pricesUrl)
            strHTML = req.read()
            
            searchResult = parseProductPage(strHTML)
            # print searchResult
            resellValue['category'] = category
            resellValue['recommendedItem'] = recommendedItem
            resellValue['firstPageItems'] = searchResult.get('firstPageItems', {})
            if itemInfo.get('title'):
                resellValue['title'] = itemInfo['title']
            else:
                resellValue['title'] = recommendedItem.get('title', '')
            if searchResult.get('resellPrice', 0):
                if 'new' in itemInfo.get('condition', '').lower():
                    resellValue['resellNew'] = searchResult['resellPrice']
                    # if recommendedItem.get('marketNew', 0) and recommendedItem.get('marketNew', 0)<resellValue['resellNew']:
                        # resellValue['resellNew'] = recommendedItem['marketNew']
                else:
                    resellValue['resellUsed'] = searchResult['resellPrice']
                    # if recommendedItem.get('marketUsed', 0) and recommendedItem.get('marketUsed', 0)<resellValue['resellUsed']:
                        # resellValue['resellUsed'] = recommendedItem['marketUsed']
            
            # print resellValue
     
    else:
        #print 'I am here'
        # Log in to ebay
        cookie = cookielib.CookieJar()   
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
        opener.addheaders = [('User-agent', 'Chrome/21.0.1180.57 Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/537.1 (KHTML, like Gecko) Safari/537.1')]
        # opener.addheaders = [('User-agent', 'Chrome/21.0.1180.57')]
    
        category = ''
        categories, opener = queryCategory(itemInfo['title'].strip(), opener)
        if categories:
            category = categories[0][0]
        # print category
            
        # ebayCred = operation3.getDBLogin('ebaydealsea')
        # log = {'MfcISAPICommand': 'SignInWelcome', 'co_partnerId': 502, 'userid': ebayCred['username'], 'pass': ebayCred['password']}
        # signUrl = 'https://signin.ebay.com/ws/eBayISAPI.dll'
        # login_data = urllib.urlencode(log)
        # req = opener.open(signUrl)
        # req = opener.open(signUrl, login_data)
        # category = ''
        # if 'accountsummary' in req.url.lower():
            # catSearchStr = '&cpg=4&aid=4&keywords='+urllib.quote(itemInfo['title'].strip())
            # catSearchUrl = 'http://cgi5.ebay.com/ws/eBayISAPI.dll?NewListing'+catSearchStr
            # req = opener.open(catSearchUrl)
            # strHTML = req.read()
            # root = etree.HTML(strHTML)
            # optionTags = root.xpath('//div[@id="cat1_inp"]//option')
            # #print optionTags
            # if optionTags:
                # category = optionTags[0].get('value', '')
                # print optionTags[0].text
        searchUrl = searchUrl.replace('sch/', 'sch/'+category+'/')
        req = opener.open(searchUrl)
        # print req.url
        strHTML = req.read()
        
        searchResult = parseCompletedPage(strHTML, req.url)
        # print searchResult
        resellValue['category'] = category
        resellValue['recommendedItem'] = {}
        resellValue['firstPageItems'] = searchResult.get('firstPageItems', {})
        resellValue['title'] = itemInfo['title']
        if searchResult.get('resellPrice', 0):
            if 'new' in itemInfo.get('condition', '').lower():
                resellValue['resellNew'] = searchResult['resellPrice']
                # if recommendedItem.get('marketNew', 0) and recommendedItem.get('marketNew', 0)<resellValue['resellNew']:
                    # resellValue['resellNew'] = recommendedItem['marketNew']
            else:
                resellValue['resellUsed'] = searchResult['resellPrice']
                # if recommendedItem.get('marketUsed', 0) and recommendedItem.get('marketUsed', 0)<resellValue['resellUsed']:
                    # resellValue['resellUsed'] = recommendedItem['marketUsed']
        
        # print resellValue
            
            
        # f = open('ebay.html', 'w')
        # f.write(strHTML)
        # f.close()

    
    return resellValue
            
##End of queryPriceActive(itemInfo)


def queryCategory(strQuery, opener = None):
    
    if not opener:
        cookie = cookielib.CookieJar()   
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
        opener.addheaders = [('User-agent', 'Chrome/21.0.1180.57 Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/537.1 (KHTML, like Gecko) Safari/537.1')]
        # opener.addheaders = [('User-agent', 'Chrome/21.0.1180.57')]
    
    
    # Log in to ebay
    # ebayCred = operation3.getDBLogin('ebaydealsea')
    ebayCred = {'username': 'alpswang1@gmail.com', 'password': 'password12#$'}

    log = {'MfcISAPICommand': 'SignInWelcome', 'co_partnerId': 502, 'userid': ebayCred['username'], 'pass': ebayCred['password']}
    signUrl = 'https://signin.ebay.com/ws/eBayISAPI.dll'
    login_data = urllib.urlencode(log)

    req = opener.open(signUrl)




    req = opener.open(signUrl, login_data)
    categories = []
    
    #For some reason the open function above cannot longer redirect.
    # if 'half.ebay.com' in req.url.lower():
    if True:
        catSearchStr = '&cpg=4&aid=4&keywords='+urllib.quote(strQuery.strip())
        catSearchUrl = 'http://cgi5.ebay.com/ws/eBayISAPI.dll?NewListing'+catSearchStr

        req = opener.open(catSearchUrl)
        strHTML = req.read()
        
        # f = open('ebay.html', 'w')
        # f.write(strHTML)
        # f.close()

        root = etree.HTML(strHTML)
        optionTags = root.xpath('//div[@id="cat1_inp"]//option')
        #print optionTags
        for optionTag in optionTags:
            category = optionTag.get('value', '')
            categoryDesc = optionTag.text
            percentage = int(categoryDesc.split('%)')[0].split('(')[-1])
            categories += [(category, categoryDesc, percentage)]
    # print category
    
    # print categories


    return categories, opener

##End of queryCategory(itemInfo)



def searchCompleted(itemInfo):
    '''Search matched  listings'''
    searchResult ={}
        
    # itemInfo = {'barcode': '0818406569', 'title': 'Blackjack: Play Like The Pros', 'condition': 'Used-good'}
    # itemInfo = {'barcode': '0321611136', 'title': 'Blackjack: Play Like The Pros', 'condition': 'Used-good'}
    # # # itemInfo = {'barcode': '4043972146181', 'title': 'Blackjack: Play Like The Pros', 'condition': 'Used-good'}
    # # itemInfo = {'barcode': '4043972146181', 'title': 'Blackjack: Play Like The Pros', 'condition': 'New'}
    # itemInfo = {'barcode': '', 'title': 'Tomtom XL 340TM', 'condition': 'Used-good'}
    # # itemInfo = {'barcode': '', 'title': 'iphone 4 black', 'condition': 'Used-good'}
    # itemInfo = {'barcode': '', 'title': 'iphone 4 white', 'condition': 'New', 'category': '9355'}
    # # itemInfo = {'barcode': '', 'title': 'Blackj`ck: Play Like The Pros', 'condition': 'New'}
    # # itemInfo = {'barcode': '', 'title': 'Blackjack: Play Like The Pros', 'condition': 'Used-good', 'category': '378'}
    
    # print itemInfo
    
    
    cookie = cookielib.CookieJar()   
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    # opener.addheaders = [('User-agent', 'Chrome/21.0.1180.57 Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/537.1 (KHTML, like Gecko) Safari/537.1')]
    opener.addheaders = [('User-agent', 'Chrome/21.0.1180.57')]
    
    #Sign in dealsea to get the shipping info in the listing.
    # ebayCred = operation3.getDBLogin('ebaydealsea')
    # Temp solution. Talk with Larry to fix this.
    ebayCred = {'username': 'alpswang1@gmail.com', 'password': 'password12#$'}
    log = {'MfcISAPICommand': 'SignInWelcome', 'co_partnerId': 502, 'userid': ebayCred['username'], 'pass': ebayCred['password']}
    signUrl = 'https://signin.ebay.com/ws/eBayISAPI.dll'
    login_data = urllib.urlencode(log)
    req = opener.open(signUrl)
    req = opener.open(signUrl, login_data)
    # print req.url
    
    # if itemInfo.get('barcode', ''):
        # barcode = itemInfo['barcode'].lstrip('0');
        # if len(barcode)==9 or len(barcode)==11:
            # barcode = '0' + barcode #A simple hack to compensate the mistakenly stripped zero for isbn or upc.
        # searchUrl = 'http://www.ebay.com/sch/i.html?_nkw='+barcode
    # elif itemInfo.get('title', ''):
        # searchUrl = ('http://www.ebay.com/sch/i.html?_nkw='+urllib.quote(itemInfo['title'].strip()))
    # else:
        # return researchResult
        
    if itemInfo.get('title', ''):
        searchUrl = ('http://www.ebay.com/sch/i.html?_nkw='+urllib.quote(itemInfo['title'].strip()))
    else:
        return searchResult
   
    
    binStr = '&LH_BIN=1'
    matchStr = '&_sop=13' #Recent first
    locStr = '&LH_PrefLoc=1'
    nItemsStr = '&_ipg=200'
    completedStr = '&LH_Complete=1'
    viewStr = '&_dmd=1' #1 for list view, #2 for gallery view
    if 'new' in itemInfo.get('condition', '').lower():
        condUrlStr = '&LH_ItemCondition=3'          
    else:
        condUrlStr = '&LH_ItemCondition=4'
    # queryUrl = matchStr+binStr+condUrlStr+locStr+nItemsStr+completedStr
    queryUrl = matchStr+condUrlStr+locStr+nItemsStr+completedStr+viewStr #Include all BIN and auction items.
    searchUrl += queryUrl
    searchUrl = searchUrl.replace('sch/', 'sch/'+itemInfo.get('category', '')+'/')
    # print searchUrl
    
    req = opener.open(searchUrl)
    # print req.url
    strHTML = req.read()
    
    searchResult = parseCompletedPage(strHTML, req.url)
    # print searchResult
    
    # f = open('ebay.html', 'w')
    # f.write(strHTML)
    # f.close()
    
    return searchResult
    
#End of searchCompleted(itemInfo)



def parseCompletedPage(strHTML, url):
    result = {}
    if not strHTML:
        return result
        
    try:
        if 'itemcondition=3' in url.lower():
            condition = 'new'
        elif 'itemcondition=4' in url.lower():
            condition = 'used'
        elif 'itemcondition' not in url.lower():
            condition = 'unknown'
        else:
            condition = 'used'
            
        root = etree.HTML(strHTML)
        
        #Get the user category
        userCat = ''
        topCatTags = root.xpath('//div[@id="gh-cat-box"]//option[@value="0"]/preceding-sibling::option[1]')
        if topCatTags:
           topCatStr = topCatTags[-1].text.encode('windows-1252', 'ignore').strip()
           userCat = categoryMap1.get(topCatStr.lower(), '')
           # print topCatStr
           # print userCat
        result['userCat'] = userCat
        
        
        #The following parsing code is written to cover two different page formats used by ebay.
        listItems = []
        soldItems = []
        # listTags = root.xpath('//div[@class="rs rsw t225"]//tbody[@itemprop="itemOffered"]')
        # listTags = root.xpath('//div[@class="rs rsw t225"][a[@id="mainContent"]]//tbody[@itemprop="itemOffered"]')
        listTags = root.xpath('//div[contains(@class, "rs rsw")][a[@id="mainContent"]]//*[@listingid]')
        # print listTags
        # print 'here'
        for listTag in listTags:
            # print listTag.get('class')
            listItem = {}
            
            #img and link
            #print etree.tostring(listTag, pretty_print=True)
            # imgTags = listTag.xpath('.//div[@class="picW"]//a')
            imgTags = listTag.xpath('.//div[contains(@class, "picW")]//a')
            #print imgTags
            if imgTags:
                listItem['link'] = imgTags[0].get('href', '')
                imgsrcTags = imgTags[0].xpath('.//img')
                if imgsrcTags:
                    listItem['imgurl'] = imgsrcTags[0].get('src')
            
            #title
            titleStr = ''.join(listTag.xpath('.//div[@class="ittl"]//a//text()'))
            if not titleStr:
                # f = open('ebay.html', 'w')
                # f.write(strHTML)
                # f.close()
                # print 'Format 2'
                titleStr = ''.join(listTag.xpath('.//h3[@class="lvtitle"]//a//text()'))
            if titleStr:
                listItem['title'] = titleStr.strip()
                
            #price + shipping
            priceStr = ''
            priceTags = listTag.xpath('.//*[@class="g-b bidsold" or @class="g-bbidsold"]')
            if priceTags:
                listItem['sold'] = 1
                priceStr = ''.join(priceTags[0].xpath('.//text()')).strip()
            else:
                priceTags = listTag.xpath('.//*[@class="g-b binsold" or @class="g-bbinsold"]')
                if priceTags:
                    listItem['sold'] = 0
                    priceStr = ''.join(priceTags[0].xpath('.//text()')).strip()
             #processing the priceStr
            dotPos = priceStr.find('.')
            if dotPos>0:
                priceStr = priceStr[:dotPos+3]
            shippingStr = ''.join(listTag.xpath('.//span[@class="ship"]//text()')).strip()
            # print shippingStr
            # print priceStr
            if priceStr:
                if condition == 'new':
                    listItem['marketNew'] = float(priceStr.replace('$', '').replace(',', ''))
                    if shippingStr and ('free' not in shippingStr.lower()):
                        try:
                            listItem['marketNew'] += float(shippingStr.split('$')[-1].split()[0].replace(',', ''))
                        except Exception, e:
                            pass
                elif condition == 'used':
                    listItem['marketUsed'] = float(priceStr.replace('$', '').replace(',', ''))
                    if shippingStr and ('free' not in shippingStr.lower()):
                        try:
                            listItem['marketUsed'] += float(shippingStr.split('$')[-1].split()[0].replace(',', ''))
                        except Exception, e:
                            pass
                else:
                    listItem['market'] = float(priceStr.replace('$', '').replace(',', ''))
                    if shippingStr and ('free' not in shippingStr.lower()):
                        try:
                            listItem['market'] += float(shippingStr.split('$')[-1].split()[0].replace(',', ''))
                        except Exception, e:
                            pass
            
            #listing style
            binStr = ''.join(listTag.xpath('.//div[@class="bin"]//text()')).strip()
            if not binStr:
                binStr = ''.join(listTag.xpath('.//li[@class="lvaucbin bin"]//text()')).strip()
            if 'now' in binStr.lower():
                listItem['style'] = "Buy It Now"
            else:
                listItem['style'] = 'Auction'
            
            # print shippingStr
            # print listItem
            listItems += [listItem]
            if listItem.get('sold', ''):
                soldItems += [listItem]
            
        listItems = sorted(listItems, key=lambda d: -(d.get('sold', 0)+d.get('sold',0)))
        
        # print listItems
        # print len(listItems)
                
        result['firstPageItems'] = listItems
        
        #Sort and then get the recommended resell price
        sortedItems = sorted(soldItems, key=lambda d: (d.get('marketNew', 0)+d.get('marketUsed',0)+d.get('market',0)))
        Nitems = len(sortedItems)
        # print 'Sold iems: %d' % Nitems
        if Nitems:
            recommendedPrice = ((sortedItems[Nitems/2].get('marketNew', 0)+sortedItems[Nitems/2].get('marketUsed', 0)+sortedItems[Nitems/2].get('market', 0))
                + (sortedItems[(Nitems-1)/2].get('marketNew', 0)+sortedItems[(Nitems-1)/2].get('marketUsed', 0)+sortedItems[(Nitems-1)/2].get('market', 0)))/2
            result['resellPrice'] = recommendedPrice
        
            pricePer25 = operation3.percentile(sortedItems, 0.25, key=lambda d: (d.get('marketNew', 0)+d.get('marketUsed',0)+d.get('market',0)))
            pricePer75 = operation3.percentile(sortedItems, 0.75, key=lambda d: (d.get('marketNew', 0)+d.get('marketUsed',0)+d.get('market',0)))
            result['range25'] = pricePer25
            result['range75'] = pricePer75
            
            
            
            
        
        # print recommendedPrice
        return result
        
    except Exception, e:
        print ("Error: Cannot parse ebay search page: ")
        print e
        return result

##End of parseCompletedPage(strHTML)




def parseSearchPage(strHTML, url):
    result = {}
    if not strHTML:
        return result
        
    try:
        if 'itemcondition=3' in url.lower():
            condition = 'new'
        elif 'itemcondition=4' in url.lower():
            condition = 'used'
        else:
            condition = 'used'
            
        root = etree.HTML(strHTML)
        
        #The following parsing code is written to cover two different page formats used by ebay.
        listItems = []
        # listTags = root.xpath('//div[@class="rs rsw t225"]//tbody[@itemprop="itemOffered"]')
        # listTags = root.xpath('//div[@class="rs rsw t225"][a[@id="mainContent"]]//tbody[@itemprop="itemOffered"]')
        listTags = root.xpath('//div[contains(@class, "rs rsw")][a[@id="mainContent"]]//*[@listingid]')
        # print listTags
        for listTag in listTags:
            # print listTag.get('class')
            listItem = {}
            
            #img and link
            #print etree.tostring(listTag, pretty_print=True)
            # imgTags = listTag.xpath('.//div[@class="picW"]//a')
            imgTags = listTag.xpath('.//div[contains(@class, "picW")]//a')
            #print imgTags
            if imgTags:
                listItem['link'] = imgTags[0].get('href', '')
                imgsrcTags = imgTags[0].xpath('.//img')
                if imgsrcTags:
                    listItem['imgurl'] = imgsrcTags[0].get('src')
            
            #title
            titleStr = ''.join(listTag.xpath('.//div[@class="ittl"]//a//text()'))
            if not titleStr:
                # print 'Format 2'
                titleStr = ''.join(listTag.xpath('.//h3[@class="lvtitle"]//a//text()'))
            if titleStr:
                listItem['title'] = titleStr.strip()
            
                
            #price + shipping
            priceStr = ''.join(listTag.xpath('.//*[@class="g-b"]//text()')).strip()
             #processing the priceStr
            dotPos = priceStr.find('.')
            if dotPos>0:
                priceStr = priceStr[:dotPos+3]
            shippingStr = ''.join(listTag.xpath('.//span[@class="ship"]//text()')).strip()
            # print shippingStr
            # print priceStr
            if priceStr:
                if condition == 'new':
                    listItem['marketNew'] = float(priceStr.replace('$', '').replace(',', ''))
                    if shippingStr and ('free' not in shippingStr.lower()):
                        listItem['marketNew'] += float(shippingStr.split('$')[-1].split()[0].replace(',', ''))
                if condition == 'used':
                    listItem['marketUsed'] = float(priceStr.replace('$', '').replace(',', ''))
                    if shippingStr and ('free' not in shippingStr.lower()):
                        listItem['marketUsed'] += float(shippingStr.split('$')[-1].split()[0].replace(',', ''))
            # print shippingStr
            # print listItem
            listItems += [listItem]
            
        # print listItems
                
        result['firstPageItems'] = listItems
        
        #Sort and then get the recommended resell price
        sortedItems = sorted(listItems, key=lambda d: (d.get('marketNew', 0)+d.get('marketUsed',0)))
        Nitems = len(sortedItems)
        if Nitems:
            recommendedPrice = ((sortedItems[Nitems/2].get('marketNew', 0)+sortedItems[Nitems/2].get('marketUsed', 0))
                + (sortedItems[(Nitems-1)/2].get('marketNew', 0)+sortedItems[(Nitems-1)/2].get('marketUsed', 0)))/2
            
            result['resellPrice'] = recommendedPrice
            
        # print recommendedPrice
        return result
        
    except Exception, e:
        print ("Error: Cannot parse ebay search page: ")
        print e
        return result

##End of parseSearchPage(strHTML)





def parseProductPage(strHTML):
    result = {}
    if not strHTML:
        return result
    
    try:
        root = etree.HTML(strHTML)
        
        listItems = []
        listTags = root.xpath('//li[@class="biv"]')
        for listTag in listTags:
            listItem = {}
            
            #img, title and link
            imgTags = listTag.xpath('.//a[@class="ls-ic"]')
            if imgTags:
                listItem['link'] = imgTags[0].get('href', '')
                listItem['title'] = imgTags[0].get('title', '')
                imgsrcTags = imgTags[0].xpath('.//img')
                if imgsrcTags:
                    listItem['imgurl'] = imgsrcTags[0].get('src')
            
            #marketNew or marketUsed
            priceStr = ''.join(listTag.xpath('.//strong[contains(@class, "price")]/text()')).strip()
            # print priceStr
             #processing the priceStr
            dotPos = priceStr.find('.')
            if dotPos>0:
                priceStr = priceStr[:dotPos+3]
            #print priceStr
            if priceStr:
                price = float(priceStr.replace('$', '').replace(',', ''))
                conditionStr = ''.join(listTag.xpath('.//div[@class="ls-c"]//span[@class="slr"]/b//text()')).strip().lower()
                # print conditionStr
                if 'brand new' in conditionStr or conditionStr[:3] == 'new':
                    listItem['marketNew'] = price
                elif ('not working' not in conditionStr.lower()) and ('refurbished' not in conditionStr.lower()):
                    listItem['marketUsed'] = price
                else:
                    continue
            
            listItems += [listItem]
            
        result['firstPageItems'] = listItems
        
        #Sort and then get the recommended resell price
        sortedItems = sorted(listItems, key=lambda d: (d.get('marketNew', 0)+d.get('marketUsed',0)))
        Nitems = len(sortedItems)
        if Nitems:
            recommendedPrice = ((sortedItems[Nitems/2].get('marketNew', 0)+sortedItems[Nitems/2].get('marketUsed', 0))
                + (sortedItems[(Nitems-1)/2].get('marketNew', 0)+sortedItems[(Nitems-1)/2].get('marketUsed', 0)))/2
            
            result['resellPrice'] = recommendedPrice
            
        # print recommendedPrice
        return result
        
        
    except Exception, e:
        print ("Error: Cannot parse ebay category product page: ")
        print e
        return result

#end of parseProductPage(strHTML)
            
        

def parseProductPageSold(strHTML):
    result = {}
    if not strHTML:
        return result
    
    try:
        root = etree.HTML(strHTML)
        
        listItems = []
        listTags = root.xpath('//li[@class="biv"]')
        for listTag in listTags:
            listItem = {}
            
            #img, title and link
            imgTags = listTag.xpath('.//a[@class="ls-ic"]')
            if imgTags:
                listItem['link'] = imgTags[0].get('href', '')
                listItem['title'] = imgTags[0].get('title', '')
                imgsrcTags = imgTags[0].xpath('.//img')
                if imgsrcTags:
                    listItem['imgurl'] = imgsrcTags[0].get('src')
            
            #marketNew or marketUsed, only for sold items
            priceStr = ''.join(listTag.xpath('.//strong[contains(@class, "pricespan ls-so")]/text()')).strip()
            if not priceStr:
                continue
            shippingStr = ''.join(listTag.xpath('.//span[@class="ship"]//text()')).strip()
            if 'free' in shippingStr.lower():
                shippingFee = 0
            else:
                shippingFee = 3
            
            # print priceStr
             #processing the priceStr
            dotPos = priceStr.find('.')
            if dotPos>0:
                priceStr = priceStr[:dotPos+3]
            #print priceStr
            if priceStr:
                price = float(priceStr.replace('$', '').replace(',', ''))
                conditionStr = ''.join(listTag.xpath('.//div[@class="ls-c"]//span[@class="slr"]/b//text()')).strip().lower()
                # print conditionStr
                if 'brand new' in conditionStr or conditionStr[:3] == 'new':
                    listItem['marketNew'] = price + shippingFee
                elif ('not working' not in conditionStr.lower()) and ('refurbished' not in conditionStr.lower()):
                    listItem['marketUsed'] = price + shippingFee
                else:
                    continue
            
            listItems += [listItem]
            
        result['firstPageItems'] = listItems
        
        #Sort and then get the recommended resell price
        sortedItems = sorted(listItems, key=lambda d: (d.get('marketNew', 0)+d.get('marketUsed',0)))
        Nitems = len(sortedItems)
        if Nitems:
            recommendedPrice = ((sortedItems[Nitems/2].get('marketNew', 0)+sortedItems[Nitems/2].get('marketUsed', 0))
                + (sortedItems[(Nitems-1)/2].get('marketNew', 0)+sortedItems[(Nitems-1)/2].get('marketUsed', 0)))/2
            
            result['resellPrice'] = recommendedPrice
            
        # print recommendedPrice
        return result
        
        
    except Exception, e:
        print ("Error: Cannot parse ebay category product page: ")
        print e
        return result

#end of parseProductPageSold(strHTML)

        
        
    
#http://www.ebay.com/sch/i.html?_nkw=the+davinci+code&_sop=12
#&_sop=12 means best match; &LH_BIN=1 means buy it now; &LH_ItemCondition=4 means used, 3 means new; LH_PreFloc=1 means US Only
#on productised item page. ?&tabs=15 for all items. &LH_BIN=1 for buy it now
#Two possible returns - one is product page for items with productized listing. Second is regular search result
#Tell by looking for <meta property="og:type" content="ebay-objects:item>
#Can also use <meta proerty="og:url" content="http://www.ebay.com/ctg/..../43435374">
#No matter what type of results, take top 5 and analyze them to get the desired information
#get up to 5 ebay item id from the keyword search
# def eBaySearch(keywords):
    # #keywords is a dictionary; two members keywords['barcode'],keywords['title']; return a list of eBay item url
    # barcode = ''
    # title = ''
    # urlList = []
    # if 'barcode' in keywords:
        # barcode = keywords['barcode']
    # if 'title' in keywords:
        # title = keywords['title'].strip().replace(' ','+')
    # if barcode <> '':
        # url = 'http://www.ebay.com/sch/i.html?_nkw='+barcode+'&_sop=12&LH_BIN=1'
    # elif title <> '':
        # url = 'http://www.ebay.com/sch/i.html?_nkw='+title+'&_sop=12&LH_BIN=1'
    # else:
        # #print "No barcode nor title in keywords. Abort"
        # return []
    # root = url2HTML(url)
    # #Detect whether page is productized page or normal search results
    # #Productized page has this <meta proerty="og:url" content="http://www.ebay.com/ctg/..../43435374">
    # typeTags = root.xpath('.//meta[@property="og:url"]')
    # if typeTags:
        # url2 = typeTags[0].xpath('@content')[0]
        # epid = url2.split('/')[-1]
        # #Append url2 so the return page is buy-it-now items with all conditions
        # url2 = url2 + '?&tabs=15&LH_BIN=1'
        # #refresh page with url2
        # root2 = url2HTML(url2)

        # #get ebay items on page
        # itemTags = root2.xpath('.//a[@class="ls-ic"]')
        # if itemTags:
            # for itemTag in itemTags:
                # urlList+=itemTag.xpath('@href')
    # #when the result page is regular search result page
    # else:
        # itemTags = root.xpath('.//table[@itemprop="offers"]')
        # if itemTags:
            # for itemTag in itemTags:
                # itemid = itemTag.xpath('@listingid')
                # if itemid:
                    # urlList+=['http://www.ebay.com/itm/?item='+itemid[0]]
    # #print "%d results found" %len(urlList)
    # return urlList
# #end of eBaySearch() 