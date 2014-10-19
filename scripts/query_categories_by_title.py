'''
Query the categories by title.
The input is the command argument one. The output result is console ouput stirng.
The input and output foramtion is JSON.
If can't find the information, nothing will be printed to console.

Input Parameters: title
Output: 

'''

    
import sys, json
import InvAlgo

try:
    print sys.argv[1];
    data = json.loads(sys.argv[1])
except:
    sys.exit(1)

#TODO add query algorithm
#input: title => data[0]


if not data[0]:
    print 'No title found from the input.'  

    result = []    
    
    # result = [
      # {
        # 'catNum': '12345',
        # 'catNameLong': 'Household Suppliers & Cleaning>Vacuum Parts & Accessories',
      # },
      # {
        # 'catNum': '12346',
        # 'catNameLong': 'Wholesale Lots > Tools > Power Tools',
      # },
      # {
        # 'catNum': '12347',
        # 'catNameLong': 'Home Improvement > Electrical & Solar > Other',
      # },
      # {
        # 'catNum': '12348',
        # 'catNameLong': 'Camera & Photo Accessories > Batteries',
      # }
    # ]
    
else:
    
    result = InvAlgo.queryCategoryMT(data[0])
    if result:
        result = result[:5] + [{'catNum': '000', 'catNameLong': 'None of the above.'}]
    else:
        result = [{'catNum': '000', 'catNameLong': 'no category found'}]
    # a = [
      # {
        # 'catNum': '12348',
        # 'catNameLong': 'Camera & Photo Accessories > Batteries',
      # }
    # ]
    # result += result1[1:2]
    # result += a
    
    # print a
    # print result
    

print '***|||RESULT|||***'
print json.dumps(result)
