'''
Query item defaults and prices information by similar item.
The input is the command argument one. The output result is console ouput stirng.
The input and output foramtion is JSON.
If can't find the information, nothing will be printed to console.

Input Parameters: title, catNum, itemUrl
Output: The dict of information: title, category, salesChannel, priceGroup

'''


categoryMap = {
    'appliances':               'APP',
    'automotive, industry':     'AUT',
    'beauty, health, grocery':  'BEA',
    'books':                    'BOK',
    'clothing, shoes, jewelry': 'CLO',
    'collectibles':             'COL',
    'electronics, computers':   'ELE',
    'everything else':          'ELS',
    'furniture':                'FUR',
    'gift cards':               'GIF',
    'home, garden, tools':      'HOM',
    'movies, music, games':     'MOV',
    'sports, outdoors':         'SPR',
    'toys, kids, baby':         'TOY'
    }
    
    
import sys, json
import InvAlgo

try:
    print sys.argv[1];
    data = json.loads(sys.argv[1])
except:
    sys.exit(1)

#TODO add query algorithm
#input: title => data[0]
#input: catNum => data[1]
#input: itemUrl => data[2]

try:
    result = {'title': data[0], 'salesChannel': 'EB'}
    
    # ebayItemId = data[2].split('?')[0].split('/')[-1]
    # print ebayItemId
    
    itemInfo = {}
    itemInfo['title'] = data[0]
    itemInfo['category'] = data[1]
    
    queryResult = InvAlgo.queryPriceAllCond(itemInfo)
    # print itemDetails
    result['category'] = categoryMap.get(queryResult.get('userCat', 'everything else').lower(), 'ELS')
    
    priceGroup = {'NW':{}, 'GD':{}, 'FR':{}, 'PR':{}}
    priceGroup['NW'] = queryResult['new']
    priceGroup['GD'] = queryResult['used']
    priceGroup['FR'] = queryResult['used']
    priceGroup['PR'] = queryResult['used']
    result['priceGroup'] = priceGroup

    print 
    
     
except Exception, e:
    print 'Error in function query_similar_items()'
    print e
    result = {}
    
# result = {
  # 'title': 'Apple MacBook Air A1465 11.6\' Laptop - MD711LL/A (June, 2013)',
  # 'category': 'ELE',
  # 'salesChannel': 'EB',
  # 'priceGroup' : {
    # 'NW' : {'marketPriceMin':100.1, 'marketPriceMax':200.1, 'expectedPrice':120},
    # 'GD' : {'marketPriceMin':90.1, 'marketPriceMax':190.1, 'expectedPrice':110},
    # 'FR' : {'marketPriceMin':80.1, 'marketPriceMax':180.1, 'expectedPrice':100},
    # 'PR' : {'marketPriceMin':70.1, 'marketPriceMax':170.1, 'expectedPrice':90},
  # }
# }

print 'test'
print '***|||RESULT|||***'
print json.dumps(result)
