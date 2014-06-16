"""
Get item recommended information.
The input is the command argument one. The output result is console ouput stirng. 
The input and output foramtion is JSON.
If can't find recommended information, nothing will be printed to consle.

Input Parameters: barcode,title,category,market,condition
Output Parameters: barcode, title, category, market, condition, price

"""

import sys, json

try:
    data = json.loads(sys.argv[1])
except:
    sys.exit(1)

#TODO add search algorithm
#input: data['barcode']...

result = {
    'barcode': '123',
    'title': 'SanGuoYanYi',
    'category': 'Book', 
    'market': 'Amazon trade in',
    'condition': 'Used-good',
    'price': 888.00
    }

print json.dumps(result)
