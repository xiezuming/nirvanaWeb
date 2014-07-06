import operation3
import ebay
# import amazon

def queryBarcode(barcode):
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
        productInfoEbay = ebay.queryPriceAllCond(itemInfo)
        # print productInfoEbay
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
