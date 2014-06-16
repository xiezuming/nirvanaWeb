"""
Query recommended categories on the eBay by title.
The input is the command argument one. The output result is console ouput stirng.
The input and output foramtion is JSON.
If can't find itmes, nothing will be printed to consle.

Input Parameters: title
Output: Categoris

"""

import sys, json

try:
    print sys.argv[1];
    data = json.loads(sys.argv[1])
except:
    sys.exit(1)

#TODO add query algorithm
#input: title => data[0]

result = {
	1	:	{
				'catNum'		:	'12345',
				'catNameLong'	:	'Household Suppliers & Cleaning>Vacuum Parts & Accessories',
			},
	2	:	{
				'catNum'		:	'12346',
				'catNameLong'	:	'Wholesale Lots > Tools > Power Tools',
			},
	3	:	{
				'catNum'		:	'12347',
				'catNameLong'	:	'Home Improvement > Electrical & Solar > Other',
			},
	4	:	{
				'catNum'		:	'12348',
				'catNameLong'	:	'Camera & Photo Accessories > Batteries',
			},
};
print 'test'
print '***|||RESULT|||***'
print json.dumps(result)
