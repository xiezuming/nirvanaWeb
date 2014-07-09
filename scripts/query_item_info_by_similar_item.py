'''
Query item defaults and prices information by similar item.
The input is the command argument one. The output result is console ouput stirng.
The input and output foramtion is JSON.
If can't find the information, nothing will be printed to console.

Input Parameters: title, catNum, itemUrl
Output: The dict of information: title, category, salesChannel, priceGroup

'''

import sys, json

try:
    print sys.argv[1];
    data = json.loads(sys.argv[1])
except:
    sys.exit(1)

#TODO add query algorithm
#input: title => data[0]
#input: catNum => data[1]
#input: itemUrl => data[2]

result = {
  'title': 'Apple MacBook Air A1465 11.6\' Laptop - MD711LL/A (June, 2013)',
  'category': 'ELE',
  'salesChannel': 'EB',
  'priceGroup' : {
    'NW' : {'marketPriceMin':100.1, 'marketPriceMax':200.1, 'expectedPrice':120},
    'GD' : {'marketPriceMin':90.1, 'marketPriceMax':190.1, 'expectedPrice':110},
    'FR' : {'marketPriceMin':80.1, 'marketPriceMax':180.1, 'expectedPrice':100},
    'PR' : {'marketPriceMin':70.1, 'marketPriceMax':170.1, 'expectedPrice':90},
  }
}

print 'test'
print '***|||RESULT|||***'
print json.dumps(result)
