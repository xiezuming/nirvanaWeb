#!/usr/bin/python


import urllib2
import time
import operation3
from lxml import etree
import re

def searchAmazon(dict):
    #input {'barcode':'abc','title':'abc','condition':'New'}

    result = {}
    result['recommended'] = {}
    result['itemList'] = []
    result['title'] = ''
    result['pricenew'] = 0
    result['priceused'] = 0
    result['pricetradein'] = 0
    result['category'] = ''
    searchResult={'match':[],'looseMatch':[]}

    if 'barcode' in dict.keys():
        searchResult = searchItemUrl({'barcode':dict['barcode']},returnNo=20,looseMatch=True)
    if 'title' in dict.keys() and searchResult['match']==[]:
        searchResult = searchItemUrl({'keyword':dict['title']},returnNo=20,looseMatch=True)
    # print searchResult
    if searchResult['match'] != []:
        recommendedAsin = searchResult['match'][0]['asin']
        itemInfo = operation3.getAmznInfo(recommendedAsin)
        #print itemInfo
        if 'asin' in itemInfo.keys(): 
            result['recommended']['asin'] = itemInfo['asin']
            result['asin'] = itemInfo['asin']
        if 'title' in itemInfo.keys(): 
            result['recommended']['title'] = itemInfo['title']
            result['title'] = itemInfo['title']
        if itemInfo['price']+itemInfo['shipping']<1000: 
            result['recommended']['pricenew'] = itemInfo['price']+itemInfo['shipping']
            result['pricenew'] = itemInfo['price']+itemInfo['shipping']
        else:
            result['recommended']['pricenew'] = 0
        if 'priceused' in itemInfo.keys(): 
            result['recommended']['priceused'] = itemInfo['priceused']
            result['priceused'] = itemInfo['priceused']
        else:
            result['recommended']['priceused'] = 0
        if 'pricetradein' in itemInfo.keys(): 
            result['recommended']['pricetradein'] = itemInfo['pricetradein']
            result['pricetradein'] = itemInfo['pricetradein']
        else:
            result['recommended']['pricetradein'] = 0
        if 'weight' in itemInfo.keys(): 
            result['recommended']['weight'] = itemInfo['weight']
            result['weight'] = itemInfo['weight']
        #is default weight needed here? maybe not
        #else:
        #    result['recommended']['weight'] = 5
        if 'dimensions' in itemInfo.keys(): 
            result['recommended']['dimensions'] = itemInfo['dimensions']
        if 'category' in itemInfo.keys(): 
            result['recommended']['category'] = itemInfo['category']
            result['category'] = itemInfo['category']

    result['itemList'] = searchResult['match']+searchResult['looseMatch']
    return result


def searchItemUrl(itemID, verify='', returnNo=1, looseMatch=False):
    #3-12-2014: enhanced by Larry to return list of asin and loosematch
    #when looseMatch = True, return a dictionary {'match':[],'looseMatch':[]}
    #when looseMatch = False, return a url when returnNo=1 and return a list of asin when returnNo>1
    itemUrl = ''
    keyword = ''
    asinResult = []
    looseResult = []
    if itemID.get('asin', ''):
        itemUrl = 'http://www.amazon.com/dp/'+itemID['asin']
        asinResult.append(itemID['asin'])
    elif itemID.get('isbn10', ''):
        itemUrl = 'http://www.amazon.com/dp/'+itemID['isbn10'].zfill(10)
        asinResult.append(itemID['isbn10'])
    else:
        if itemID.get('upc', ''):
            keyword = itemID['upc'].zfill(12)
        elif itemID.get('isbn13', ''):
            keyword = itemID['isbn13'].zfill(13)
        elif itemID.get('barcode', ''):
            barcode = str(itemID['barcode']).lstrip('0')
            if len(barcode)<=10: keyword=barcode.zfill(10)
            elif len(barcode)<=12: keyword=barcode.zfill(12)
            else: keyword=barcode.zfill(13)
        # keyword = 'finance'
    if keyword:
        url = 'http://www.amazon.com/s/&field-keywords='+keyword.replace(',',' ').replace(':',' ').replace("'"," ").replace(' ', '%20')
        urlString = operation3.url2str(url)
        # f = open('amazon.html', 'w')
        # f.write(urlString)
        # f.close()
        if urlString:
            root = etree.HTML(urlString)
            asinList1 = root.xpath('//div[@id="atfResults"]/div')
            asinList2 = root.xpath('//div[@id="btfResults"]/div')
            asinList = asinList1+asinList2
            if asinList: #Format 1.
                print 'Format 1'

                for item in asinList:
                    asin = item.xpath('./@name')
                    if asin!=[]:
                        searchItem = {}
                        searchItem['asin'] = asin[0]
                        title = item.xpath('.//span[@class="lrg bold"]/text()')
                        if title != []:
                            searchItem['title'] = title[0]
                        img = item.xpath('.//img')
                        if img != []:
                            imgurl = img[0].get('src','')
                            imgurlSplit = imgurl.split('/I/', 1)
                            if len(imgurlSplit)>1:
                                imgurl = imgurlSplit[0]+'/I/'+imgurlSplit[1].split('.', 1)[0]+'.'+imgurlSplit[1].split('.')[-1]
                            searchItem['imgurl'] = imgurl
                        pricelist = item.xpath('.//li[@class="newp"]//del/text()')
                        if pricelist != []:
                            searchItem['pricelist'] = pricelist[0].split('$')[1].strip().replace(',','')
                        rentcheck = item.xpath('.//li[@class="newp"]//text()')
                        if 'to rent' in rentcheck:
                            pricenew = item.xpath('.//ul[@class="rsltL"]//span[@class="red"]/text()')
                        else:    
                            pricenew = item.xpath('.//li[@class="newp"]//span[@class="bld lrg red"]/text()')
                        #print pricenew
                        if pricenew != []:
                            if pricenew[0].find('$')>0:
                                searchItem['pricenew'] = pricenew[0].split('$')[1].strip().replace(',','')
                        itemstring = etree.tostring(item)
                        if itemstring.find("More Buying Choices")>0:
                            morestring = itemstring.split("More Buying Choices")[1]
                            if morestring.find("used")>0:
                                priceused = morestring.split(' used ')[0].split('$')[-1].split('<')[0]
                                searchItem['priceused'] = priceused
                        elif itemstring.find("condition=used")>0:
                            morestring = itemstring.split("condition=used")[1]
                            if morestring.find(" used ")>0:
                                priceused = morestring.split(' used ')[0].split('$')[-1].split('<')[0]
                                searchItem['priceused'] = priceused
                        asinResult.append(searchItem)
                #asin = asinList[0]
                itemUrl = 'http://www.amazon.com/dp/'+asinResult[0]['asin']
        
            if not asinList: #Format 2 new from Oct 2014.
                asinList1 = root.xpath('//div[@id="atfResults"]//li[contains(@id, "result_")]')
                asinList2 = root.xpath('//div[@id="btfResults"]//li[contains(@id, "result_")]')
                asinList = asinList1+asinList2
                # print asinList
                if asinList:
                    print 'Format 2'
                for item in asinList:
                    asin = item.xpath('./@data-asin')
                    # print asin
                    if asin:
                        searchItem = {}
                        searchItem['asin'] = asin[0]
                        title = item.xpath('.//h2[contains(@class, "s-inline s-access-title")]/text()')
                        if title != []:
                            searchItem['title'] = title[0]
                            # print searchItem['title']
                        img = item.xpath('.//img')
                        if img != []:
                            imgurl = img[0].get('src','')
                            imgurlSplit = imgurl.split('/I/', 1)
                            if len(imgurlSplit)>1:
                                imgurl = imgurlSplit[0]+'/I/'+imgurlSplit[1].split('.', 1)[0]+'._AA300_.'+imgurlSplit[1].split('.')[-1]
                            searchItem['imgurl'] = imgurl
                            # print searchItem['imgurl']
                        # print asin[0]
                        priceList = ''
                        priceTags = item.xpath(('.//a[contains(@class, "a-link-normal a-text-normal") and contains(@href, "%s")]//span[contains(@class, "a-color-price")]' % asin[0]))
                        for priceTag in priceTags:
                            priceText = '`'.join(priceTag.getparent().xpath('.//text()'))
                            # print priceText
                            if '$' in priceText:
                                priceStr =  priceText.split('$')[-1].split('`')[0].replace(',','')
                                # print priceStr
                                priceList += (',' + priceStr)
                                if 'rent' in priceText:
                                    continue
                                elif 'used' in priceText:
                                    searchItem['priceused'] = priceStr
                                else:
                                    searchItem['pricenew'] = priceStr
                        searchItem['priceList'] = priceList.strip(',')
                        # print searchItem
                        asinResult.append(searchItem)
                
                itemUrl = 'http://www.amazon.com/dp/'+asinResult[0]['asin']            
                            
                         
    #If still cannot get itemUrl, use keyword and verification
    if not itemUrl:
        if itemID.get('keyword', ''):
            keyword = itemID['keyword'].lower()
                        
            #Special process when verify is required.
            if verify.lower() == 'keyword':
                keyword0 = keyword #Original keywords for constructing url
                keyword = re.sub('[^\x00-\x7F]', '', keyword) #Strip off all non-ascii keywords 
                #Construct the verification key list
                
                #Get all words with both numbers and letters
                verKeys = re.findall('(?:[a-z]+[0-9]|[0-9]+[a-z])[a-z0-9]*', keyword)
                
                #Get all numbers with equal or more than 4 digits
                verKeys += re.findall('(?:^|(?<= ))[0-9]{4,}(?:$|(?= ))', keyword)
                
                #Get the first word
                keywordList = keyword.split()
                for word in keywordList:
                    if word not in verKeys:
                        verKeys.append(word)
                        break
                
                #Get the longest word
                keywordListSorted = sorted(keywordList, key=len, reverse=True)
                for word in keywordListSorted:
                    if len(word)<5:
                        break
                    elif '-' in word:
                        continue
                    elif word in verKeys:
                        continue
                    else:
                        verKeys.append(word)
                        break
                
                #Get the center word
                L = len(keywordList)
                keywordListSorted = [keywordList[(i+1)/2*((-1)**i)+(L/2)] for i in range(0, L)]
                for word in keywordListSorted:
                    if len(word)<3 and (not re.findall('[0-9]', word)):
                        continue
                    if word not in verKeys:
                        verKeys.append(word)
                        break                
                print 'Verification keys: '+' '.join(verKeys)
                
                #Get items
                url = ('http://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Daps&field-keywords='+keyword0.replace('%', '%25').replace('&', '%26').replace(' ', '+'))
                #print url
                urlString = operation3.url2str(url)
                if urlString:
                    root = etree.HTML(urlString)
                    resultList = root.xpath('//div[contains(@id, "tfResults")]/div[contains(@id, "result_")]')
                    count = 0
                    #print len(resultList)
                    for result in resultList:
                        description = ' '.join(result.xpath('./h3[@class="newaps"][1]//*/text()'))
                        formatStr = ' '.join(result.xpath('./ul[@class="rsltL"][1]//span[@class="lrg"][1]/text()'))
                        #print formatStr
                        if 'instant' in formatStr:
                            continue
                        else:
                            description += (' '+formatStr)
                        description = description.lower()
                        descriptionWords = description.split()
                        #print description
                        #Keyword verification
                        #If it is the first search result and more than 3 verification keywords, We loose the 
                        #match threshold to the number of verification keywords minus one.
                        if (not (count)) and len(verKeys)>3:
                            matchThr = len(verKeys)-1
                        else:
                            matchThr = len(verKeys)
                        #matchRes = [1 for key in verKeys if key in descriptionWords]
                        #print description
                        matchRes = [1 for key in verKeys if key in description]
                        if sum(matchRes)>=matchThr:
                            asin = result.get('name')
                            print 'Amazon item: '+description.encode('windows-1252', 'ignore')
                            if asin:
                                itemUrl = 'http://www.amazon.com/dp/'+asin
                            #print count
                            break
                        count += 1
                
            #Generic search process.
            else:
                url = 'http://www.amazon.com/s/&field-keywords='+keyword.replace(',',' ').replace(':',' ').replace("'"," ").replace(' ', '%20')
                urlString = operation3.url2str(url)
                if urlString:
                    root = etree.HTML(urlString)
                    asinList1 = root.xpath('//div[@id="atfResults"]/div')
                    asinList2 = root.xpath('//div[@id="btfResults"]/div')
                    asinList = asinList1+asinList2
                    #asinList = root.xpath('//div[@id="atfResults"]/div[@id="result_0"]/@name')
                    if asinList:
                        for item in asinList:
                            asin = item.xpath('./@name')
                            if asin != []:
                                searchItem = {}
                                searchItem['asin'] = asin[0]
                                title = item.xpath('.//span[@class="lrg bold"]/text()')
                                if title != []:
                                    searchItem['title'] = title[0]
                                img = item.xpath('.//img')
                                if img != []:
                                    imgurl = img[0].get('src','')
                                    imgurlSplit = imgurl.split('/I/', 1)
                                    if len(imgurlSplit)>1:
                                        imgurl = imgurlSplit[0]+'/I/'+imgurlSplit[1].split('.', 1)[0]+'.'+imgurlSplit[1].split('.')[-1]
                                    searchItem['imgurl'] = imgurl
                                pricelist = item.xpath('.//li[@class="newp"]//del/text()')
                                if pricelist != []:
                                    searchItem['pricelist'] = pricelist[0].split('$')[1].strip().replace(',','')
                                rentcheck = item.xpath('.//li[@class="newp"]//text()')
                                if 'to rent' in rentcheck:
                                    pricenew = item.xpath('.//ul[@class="rsltL"]//span[@class="red"]/text()')
                                else:    
                                    pricenew = item.xpath('.//li[@class="newp"]//span[@class="bld lrg red"]/text()')
                                if pricenew != []:
                                    if pricenew[0].find('$')>0:
                                        searchItem['pricenew'] = pricenew[0].split('$')[1].strip().replace(',','')
                                itemstring = etree.tostring(item)
                                if itemstring.find("More Buying Choices")>0:
                                    morestring = itemstring.split("More Buying Choices")[1]
                                    if morestring.find(" used ")>0:
                                        priceused = morestring.split(' used ')[0].split('$')[-1].split('<')[0]
                                        searchItem['priceused'] = priceused
                                elif itemstring.find("condition=used")>0:
                                    morestring = itemstring.split("condition=used")[1]
                                    if morestring.find(" used ")>0:
                                        priceused = morestring.split(' used ')[0].split('$')[-1].split('<')[0]
                                        searchItem['priceused'] = priceused
                                #print searchItem
                                asinResult.append(searchItem)
                        #asin = asinList[0]
                        itemUrl = 'http://www.amazon.com/dp/'+asinResult[0]['asin']
    
    if looseMatch == True and asinResult == []:
        looseList = root.xpath('//div[@id="fkmr-results0"]/div')
        if looseList:
            for item in looseList:
                #print etree.tostring(item)
                asin = item.xpath('./@name')
                if asin != []:
                    searchItem = {}
                    searchItem['asin'] = asin[0]
                    title = item.xpath('.//span[@class="lrg bold"]/text()')
                    if title != []:
                        searchItem['title'] = title[0]
                    pricelist = item.xpath('.//li[@class="newp"]//del/text()')
                    if pricelist != []:
                        searchItem['pricelist'] = pricelist[0].split('$')[1].strip().replace(',','')
                    rentcheck = item.xpath('.//li[@class="newp"]//text()')
                    if 'to rent' in rentcheck:
                        pricenew = item.xpath('.//ul[@class="rsltL"]//span[@class="red"]/text()')
                    else:    
                        pricenew = item.xpath('.//li[@class="newp"]//span[@class="bld lrg red"]/text()')
                    if pricenew != []:
                        if pricenew[0].find('$')>0:
                            searchItem['pricenew'] = pricenew[0].split('$')[1].strip().replace(',','')
                    itemstring = etree.tostring(item)
                    if itemstring.find("More Buying Choices")>0:
                        morestring = itemstring.split("More Buying Choices")[1]
                        if morestring.find(" used ")>0:
                            priceused = morestring.split(' used ')[0].split('$')[-1].split('<')[0]
                            searchItem['priceused'] = priceused
                    elif itemstring.find("condition=used")>0:
                        morestring = itemstring.split("condition=used")[1]
                        if morestring.find(" used ")>0:
                            priceused = morestring.split(' used ')[0].split('$')[-1].split('<')[0]
                            searchItem['priceused'] = priceused
                    #print searchItem
                    looseResult.append(searchItem)
    #print 'keyword: '+keyword
    # print asinResult
    if looseMatch == True:
        return {'match':asinResult[:min(len(asinResult),returnNo)],'looseMatch':looseResult}
    else:
        if returnNo==1:
            return itemUrl
        elif returnNo>1:
            return asinResult[:min(len(asinResult),returnNo)]
   
#End of searchItemUrl			




def getItemDetails(itemID):
    itemDetails = {'source': 'amazon.com', 'availability': 0, 'price': 0, 'shipping': 0}
    url = searchItemUrl(itemID)
    parseItmPg = operation3.parseAmznInfo
    #print url
    if url: 
        strHtml = operation3.url2str(url)
        if strHtml: 
            itemDetails.update(parseItmPg(strHtml))
    return itemDetails


# def parseItmPg(string):
    
    # def liststrip(list): #Local function
        # for i in range(len(list)):
            # list[i] = list[i].strip()
    # # End of def liststrip(list)
    
    # #priceinfo = {'sku' : asin}
    # #priceinfo['produrl'] = 'http://www.amazon.com/dp/'+asin
    # priceinfo = {}
    # priceinfo['title'] = ''
    # priceinfo['shipping'] = 999
    # priceinfo['prime'] = 0
    # priceinfo['availability' ] = 0
    # priceinfo['maxqty'] = 1
    # priceinfo['thirdparty'] = 1
    # priceinfo['source'] = 'amazon'
   
    # try:
# #         url = 'http://www.amazon.com/dp/'+asin
# #         root = url2HTML(url)
        
        # root = etree.HTML(string)
        # asin = ''
        # asinList = root.xpath('(//input[@id="ASIN" and @name="ASIN"])[1]')
        # if asinList:
            # asin = asinList[0].get('value', '')
        # if not asin: return priceinfo
        # priceinfo['sku'] = asin
        # priceinfo['url'] = 'http://www.amazon.com/dp/'+asin


        
        
    
        # buyBlkTags = root.xpath('.//form[@id="handleBuy"]')
        # if buyBlkTags:
            # buyblk = buyBlkTags[0]
    
            # #Get title.
            # title = ''.join(buyblk.xpath('.//span[@id="btAsinTitle"]//text()'))
            # priceinfo['title']=title
    
            # #Get price and prime info.
            # pricetag = buyblk.xpath('.//td[@id="actualPriceContent"]/span[@id="actualPriceValue"]/b[@class="priceLarge"]')
            # #Larry added on 3-14-13 to catch some books with both new and rental
            # if not pricetag: pricetag = buyblk.xpath('.//td[@class="rightBorder buyNewOffers"]/span[@class="rentPrice"]')
            # if (pricetag): #if price is displayed
                # priceinfo['price'] = float(pricetag[0].text.strip().strip('$').replace(',',''))
                # priceinfo['prime'] = 0
                # priceinfo['shipping'] = 999
                # priceinfo['availability'] = 0
                # #if free shipping available, it's prime eligible
                # if 'free' in etree.tostring(pricetag[0].getparent().getparent(), method='text', encoding='utf-8').lower():
                    # priceinfo['prime'] = 1
                    # priceinfo['shipping'] = 0

            # else: #If price is "too low to display"
                # if buyblk.xpath('.//td[@id="actualPriceContent"]/span[@id="actualPriceValue"]//a[@target="WhyNoPrice"]'):
                    # extrainfo = operation3.getAmznPriceHF(asin)
                    # if 'price' in extrainfo:
                        # priceinfo['price'] = extrainfo['price']
                        # priceinfo['prime'] = 0
                        # priceinfo['shipping'] = 999
                        # priceinfo['availability'] = 0
                        # #if free shipping available, it's prime eligible
                        # shptag = buyblk.xpath('.//td[@id="shippingMessageStandAlone"]')
                        # if shptag:
                            # if 'free' in etree.tostring(shptag[0], method='text', encoding='utf-8').lower():
                                # priceinfo['prime'] = 1
                                # priceinfo['shipping'] = 0
            
            # if not ('price' in priceinfo):
                # priceinfo['price'] = 4999
                # priceinfo['maxqty'] = 0
                # priceinfo['availability'] = 0
            # else:
            # #Get the shipping info if not prime.
                # if not priceinfo.get('prime', 0):
                    # shptag = buyblk.xpath('.//span[@class="plusShippingText"]')
                    # if shptag:
                        # if 'free' in shptag[0].text.lower():
                            # priceinfo['shipping'] = 0
                        # else:
                            # if len(shptag[0].text.split('$'))>1:
                                # priceinfo['shipping'] = float(shptag[0].text.split('$')[1].split(u'\xa0')[0])
                
                # #Get availability info.
                # priceinfo['availability']=0
                # availtag = buyblk.xpath('.//span[@class="availGreen"]')
                # if availtag:
                    # availtext = availtag[0].text
                    # if 'Only' in availtext:
                        # availqty = int(availtext.split(' ')[1])
                        # if availqty >= 2: 
                            # priceinfo['availability'] = 1
                    # else:
                        # priceinfo['availability'] = 1
                # else:
                    # availtag = buyblk.xpath('.//span[@class="availOrange"]')
                    # if availtag:
                        # availtext = availtag[0].text
                        # if 'released' in availtext.lower():
                            # priceinfo['availability'] = 1
                        # elif 'day' in availtext.lower():
                            # priceinfo['availability'] = availtext.lower().split('day')[0].split()[-1]
                # if availtag:
                    # sellertext = ''.join(availtag[0].xpath('../descendant-or-self::text()'))
                    # if 'sold by amazon.com' in sellertext.lower():
                        # priceinfo['thirdparty'] = 0
                    # else:
                        # priceinfo['thirdparty'] = 1
    
            # #Get maximum order quantity info.
            # maxqty = 0
            # if buyblk.xpath('.//select[@id="quantity"]/option'):
                # maxqty = int(buyblk.xpath('.//select[@id="quantity"]/option')[-1].text)
                # priceinfo['maxqty'] = maxqty

        # #Get product features
        # features = ''
        # featureblk = root.xpath('.//div[@id="feature-bullets_feature_div"]')
        # if not featureblk:
            # featureblk = root.xpath('.//h2[text()="Product Features"]/..')
        # if featureblk:
            # for bullet in featureblk[0].xpath('.//li'):
                # if bullet.text:
                    # features = features + bullet.text + '<br>'
            # priceinfo['features'] = features
        # #Features may be loacated right after price.
        # features = ''
        # featureblk = root.xpath('.//div[@id="feature-bullets-atf"]')
        # if featureblk:
            # for bullet in featureblk[0].xpath('.//li'):
                # features = features + ' '.join(bullet.xpath('.//text()')) + '<br>'
            # priceinfo['features'] = features+'<br>'+priceinfo['features'] if 'features' in priceinfo else features


        # #Get technical details
        # techdetails = ''
        # techblk = root.xpath('.//div[@id="technical-data_feature_div"]')
        # if not techblk:
            # techblk = root.xpath('.//h2[text()="Technical Details"]/..')
        # if techblk:
            # for bullet in techblk[0].xpath('.//li'):
                # if bullet.text:
                    # techdetails = techdetails + bullet.text + '<br>'
            # if techdetails == '':
                # for bullet in techblk[0].xpath('.//li'):
                    # techdetail = bullet.xpath('.//text()')
                    # liststrip(techdetail)
                    # techdetails = techdetails+''.join(techdetail)+'<br>'
        # priceinfo['techdetails'] = techdetails

        # #Get product details
        # details = ''
        # detailblk = root.xpath('.//div[@id="detail-bullets_feature_div"]')
        # if not detailblk:
            # detailblk = root.xpath('.//h2[text()="Product Details"]/..')
        # if detailblk:
            # for bullet in detailblk[0].xpath('.//li'):
                # detail = bullet.xpath('.//text()')
                # liststrip(detail)
                # detailtext = ' '.join(detail)
                # detailtextlower = detailtext.lower()
                # #see if it's customer review. If yes, stop
                # if 'average customer' in detailtextlower:
                    # break
                # elif 'amazon' in detailtextlower:
                    # break
                # elif 'asin' in detailtextlower:
                    # continue
                # elif 'shipping:' in detailtextlower:
                    # continue
                    
                # #Dimension
                # elif 'dimensions:' in detailtextlower:
                    # dims = detailtextlower.split('dimensions:')[-1].split('inches')[0].split('x')
                    # priceinfo['dimensions'] = [float(dim) for dim in dims]
                    
                # #Weight
                # elif 'weight:' in detailtextlower:
                    # if 'pounds' in detailtextlower:
                         # priceinfo['weight'] = float(detailtextlower.split('weight:')[-1].split('pounds')[0])
                    # elif 'ounces' in detailtextlower:
                         # priceinfo['weight'] = float(detailtextlower.split('weight:')[-1].split('ounces')[0])/16
                    # detailtext = detailtext.split('(')[0]
                    
                # #Isbn10
                # elif 'isbn-10:' in detailtextlower:
                    # priceinfo['isbn10'] = detailtextlower.split('isbn-10:')[-1].strip().upper()
                    
                # #Isbn13
                # elif 'isbn-13:' in detailtextlower:
                    # priceinfo['isbn13'] = detailtextlower.split('isbn-13:')[-1].strip().replace('-', '').upper()
                    
                # #Grab release date in various cases.
                # elif 'publisher:' in detailtextlower: 
                    # strRelDate = detailtextlower.split('(')[-1].split(')')[0].strip()
                    # try: 
                        # timeRelDate = time.strptime(strRelDate, '%B %d, %Y')
                        # priceinfo['releaseDate'] = time.strftime("%Y-%m-%d", timeRelDate)
                    # except Exception, e:
                        # try: 
                            # timeRelDate = time.strptime(strRelDate, '%B %Y')
                            # priceinfo['releaseDate'] = time.strftime("%Y-%m-%d", timeRelDate)
                        # except Exception, e:
                            # try:
                                # timeRelDate = time.strptime(strRelDate, '%Y')
                                # priceinfo['releaseDate'] = time.strftime("%Y-%m-%d", timeRelDate)
                            # except Exception, e:
                                # print ("Warning: Cannot get release date from item url: "+url)
                                # print e
                                # print detailtext

                        
                # details = details+detailtext+'<br>'
        # priceinfo['details'] = details
        
        
        # #Get large image url
        # imgblk = root.xpath('.//table[@class="productImageGrid"][1]')
        # if imgblk:
            # imgtag = imgblk[0].xpath('.//img[1]')
            # imgurl = imgtag[0].get('src', '') if imgtag else ''
            # imgurlSplit = imgurl.split('/I/', 1)
            # if len(imgurlSplit)>1:
                # imgurl = imgurlSplit[0]+'/I/'+imgurlSplit[1].split('.', 1)[0]+'.jpg' 
            
            # priceinfo['imgurl'] = imgurl
       

    # except Exception, e:
        # #print asin
        # print e
        # return priceinfo

    # return priceinfo

	

