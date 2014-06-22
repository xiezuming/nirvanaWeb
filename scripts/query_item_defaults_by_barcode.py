'''
Query item default informations by barcode.
The input is the command argument one. The output result is console ouput stirng.
The input and output foramtion is JSON.
If can't find the information, nothing will be printed to consle.

Input Parameters: barcode
Output: The dict of information: title, category, marketPriceMin, marketPriceMax, expectedPrice, salesChannel, imageUrl

'''

import sys, json

try:
    print sys.argv[1];
    data = json.loads(sys.argv[1])
except:
    sys.exit(1)

#TODO add query algorithm
#input: barcode => data[0]

result = {
  'title': 'Apple MacBook Air A1465 11.6\' Laptop - MD711LL/A (June, 2013)',
  'category': 'ELE',
  'marketPriceMin': 100.0,
  'marketPriceMax': 200.0,
  'expectedPrice': 120.0,
  'salesChannel': 'EB',
  'imageUrl': 'http://thumbs2.ebaystatic.com/d/l225/m/maNLzwO1dp6Z9F2-fkPhKBQ.jpg'
}

print 'test'
print '***|||RESULT|||***'
print json.dumps(result)
