'''
Query item default informations by similar item.
The input is the command argument one. The output result is console ouput stirng.
The input and output foramtion is JSON.
If can't find the information, nothing will be printed to console.

Input Parameters: itemUrl
Output: The dict of information: title, category, salesChannel

'''

import sys, json

try:
    print sys.argv[1];
    data = json.loads(sys.argv[1])
except:
    sys.exit(1)

#TODO add query algorithm
#input: itemUrl => data[0]

result = {
  'title': 'Apple MacBook Air A1465 11.6\' Laptop - MD711LL/A (June, 2013)',
  'category': 'ELE',
  'salesChannel': 'EB'
}

print 'test'
print '***|||RESULT|||***'
print json.dumps(result)
