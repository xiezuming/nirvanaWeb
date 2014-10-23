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

ebayCatMap = {
    'antiques': 'Collectibles',
    'art': 'Home, Garden, Tools',
    'baby': 'Toys, Kids, Baby',
    'books': 'Books',
    'business & industrial': 'Automotive, Industry',
    'cameras & photo': 'Electronics, Computers',
    'cell phones & accessories': 'Electronics, Computers',
    'clothing, shoes & accessories': 'Clothing, Shoes, Jewelry',
    'coins & paper money': 'Collectibles',
    'collectibles': 'Collectibles',
    'computers/tablets & networking': 'Electronics, Computers',
    'consumer electronics': 'Electronics, Computers',
    'crafts': 'Home, Garden, Tools',
    'dolls & bears': 'Toys, Kids, Baby',
    'dvds & movies': 'Movies, Music, Games',
    'ebay motors': 'Automotive, Industry',
    'entertainment memorabilia': 'Collectibles',
    'gift cards & coupons': 'Gift Cards',
    'health & beauty': 'Beauty, Health, Grocery',
    'home & garden': 'Home, Garden, Tools',
    'jewelry & watches': 'Clothing, Shoes, Jewelry',
    'music': 'Movies, Music, Games',
    'musical instruments & gear': 'Movies, Music, Games',
    'pet supplies': 'Home, Garden, Tools',
    'pottery & glass': 'Home, Garden, Tools',
    'real estate': 'Everything Else',
    'specialty services': 'Everything Else',
    'sporting goods': 'Sports, Outdoors',
    'sports mem, cards & fan shop': 'Collectibles',
    'stamps': 'Collectibles',
    'tickets & experiences': 'Everything Else',
    'toys & hobbies': 'Toys, Kids, Baby',
    'travel': 'Everything Else',
    'video games & consoles': 'Movies, Music, Games',
    'everything else': 'Everything Else'
    }
    
    
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
    
    result = InvAlgo.queryCategoryMT(data[0], format= 'long')
    if result:
        result = result[:5] + [{'catNum': '000', 'catNameLong': 'None of the above.', 'algoType': 2}]
    else:
        result = [{'catNum': '000', 'catNameLong': 'no category found', 'algoType': 2}]
        
    
    for cat in result:
        #Get app category code.
        ebayCatName = cat.get('catNameLong', '').split('>')[0].strip()
        cat['catCode'] = categoryMap.get(ebayCatMap.get(ebayCatName.lower(), 'Everything Else').lower(), 'ELS')
        #strip the top category name.
        if ('Other' in cat.get('catNameLong') and cat.get('catNameLong').count('>') == 1) or cat.get('catNameLong').count('>') == 0:
            # cat['catNameLong'] = cat.get('catNameLong')
            continue
        else:
            cat['catNameLong'] = ' > '.join(cat.get('catNameLong').split(' > ')[1:])
        
        
    
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
