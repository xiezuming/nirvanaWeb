'''
Query the similar items by title and category number.
The input is the command argument one. The output result is console ouput stirng.
The input and output foramtion is JSON.
If can't find the information, nothing will be printed to console.

Input Parameters: title, catNum
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
#input: catNum => data[1]

itemInfo = {'title': data[0], 'category': data[1]}

try:
    result = InvAlgo.querySimilarItems(itemInfo)
    if result:
        result += [{'title': 'None of the above is similar to mine.', 'url': 'na', 'image': 'http://pics.ebaystatic.com/aw/pics/community/myWorld/imgBuddyBig24.gif'}]
    else:
        result = [{'title': 'no matched item', 'url': 'na', 'image': ''}]
    

    
except Exception, e:
    print 'Error in function query_similar_items()'
    print e
    result = []
    
    
# result = [
  # {
    # "title": "Apple iPhone 5s (Latest Model) 16GB Factory Unlocked NEW",
    # "url": "http://www.ebay.com/itm/1",
    # "image": "http://thumbs3.ebaystatic.com/d/l225/pict/191204953246_1.jpg"
  # },
  # {
    # "title": "3D sex goddess Marilyn Monroe Hard Matte Case Cover for iPhone 5 5S",
    # "url": "http://www.ebay.com/itm/2",
    # "image": "http://thumbs4.ebaystatic.com/d/l225/m/mXauv2MnBVlkIJkHA2wRqWA.jpg"
  # }
# ]

print '***|||RESULT|||***'
print json.dumps(result)
