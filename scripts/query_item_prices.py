'''
Query item market price and expected price.
The input is the command argument one. The output result is console ouput stirng.
The input and output foramtion is JSON.
If can't find the information, nothing will be printed to console.

Input Parameters: barcode, title
Output: The price information group by conditon key.
E.g.: 
{
'NW' : {'marketPriceMin':100, 'marketPriceMax':200, 'expectedPrice':120},
'GD' : {'marketPriceMin':100, 'marketPriceMax':200, 'expectedPrice':120},
......
}

'''

import sys, json

try:
    print sys.argv[1];
    data = json.loads(sys.argv[1])
except:
    sys.exit(1)

#TODO add query algorithm
#input: barcode => data[0]
#input: title => data[1]

result = {
'NW' : {'marketPriceMin':100, 'marketPriceMax':200, 'expectedPrice':120},
'GD' : {'marketPriceMin':90, 'marketPriceMax':190, 'expectedPrice':110},
'FR' : {'marketPriceMin':80, 'marketPriceMax':180, 'expectedPrice':100},
'PR' : {'marketPriceMin':70, 'marketPriceMax':170, 'expectedPrice':90},
}

print 'test'
print '***|||RESULT|||***'
print json.dumps(result)
