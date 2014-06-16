"""
Link the inventory item with eBay URL.
The input is the command argument one. The output result is console ouput stirng. 
The input foramtion is JSON.
If can't find recommended information, nothing will be printed to consle.

Input Parameters: userId,itemId,linkUrl
Output: error_message. return null if no error.

"""

import sys, json

try:
    data = json.loads(sys.argv[1])
except:
    print 'JSON load exception.'
    sys.exit(1)

#TODO add link algorithm
#input: userId => data[0], itemId => data[1], linkUrl => data[2]

result = {"message" : "Can't connect to DB"};
print 'test';
print '***|||RESULT|||***';
print json.dumps(result);
