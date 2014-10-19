'''
Query item default informations by barcode.
The input is the command argument one. The output result is console ouput stirng.
The input and output foramtion is JSON.
If can't find the information, nothing will be printed to console.

Input Parameters: barcode
Output: The dict of information: title, category, salesChannel, imageUrl

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
    #input: barcode => data[0]
    
    
if not data[0]:
    print 'No barcode info found from the input.'    
    
    result = {
      'title': 'Apple MacBook Air A1465 11.6\' Laptop - MD711LL/A (June, 2013)',
      'category': 'ELE',
      'salesChannel': 'eBay',
      'imageUrl': 'http://thumbs2.ebaystatic.com/d/l225/m/maNLzwO1dp6Z9F2-fkPhKBQ.jpg'
    }

    print 'test'
    print '***|||RESULT|||***'
    #print json.dumps(result)
    
else:
        
        
    result = {}
    queryResult = InvAlgo.queryEPIDMT(data[0])
    # print queryResult

    if queryResult.get('title', ''):
        result['title'] = queryResult['title']
        # result['expectedPrice'] = queryResult.get('expectation', 0.5)
        # result['marketPriceMin'] = queryResult.get('marketPriceMin', 0.5)
        # result['marketPriceMax'] = queryResult.get('marketPriceMax', 0.5)
        result['category'] = categoryMap.get(queryResult.get('userCat', '').lower(), '')
        result['salesChannel'] = 'EB'
        result['imageUrl'] = queryResult.get('imageUrl', '')
        
        

    #print '***|||RESULT|||***'
    # print json.dumps(result)


    #TODO add query algorithm
    #input: barcode => data[0]

    # result = {
      # 'title': 'Apple MacBook Air A1465 11.6\' Laptop - MD711LL/A (June, 2013)',
      # 'category': 'ELE',
      # 'salesChannel': 'EB',
      # 'imageUrl': 'http://thumbs2.ebaystatic.com/d/l225/m/maNLzwO1dp6Z9F2-fkPhKBQ.jpg'
    # }

    print 'test'
    print '***|||RESULT|||***'
    print json.dumps(result)
