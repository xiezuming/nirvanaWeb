"""
Query matched items on the eBay by title..
The input is the command argument one. The output result is console ouput stirng. 
The input and output foramtion is JSON.
If can't find itmes, nothing will be printed to consle.

Input Parameters: title, catNum
Output: Item list.

"""

import sys, json

try:
    print sys.argv[1];
    data = json.loads(sys.argv[1])
except:
    sys.exit(1)

#TODO add query algorithm
#input: title => data[0], catNum => data[1]

result = {
	1	:	{
				'title'		:	data[0] + '| Garmin forerunner 620 gps fitness computer black / blue train wristwatch watch',
				'url'		:	'http://www.ebay.com/itm/Garmin-forerunner-620-gps-fitness-computer-black-blue-train-wristwatch-watch-/151210376553?pt=LH_DefaultDomain_0&hash=item2334d73d69',
				'price'		:	399.99,
				'image'		:	'http://i.ebayimg.com/00/s/NjQwWDQ2Ng==/z/haMAAOxyXDhSojfU/$_3.JPG'
			},
	2	:	{
				'title'		:	data[1] + '| Xiaomi RED RICE Hongmi Android 4.2 Quad Core 1.5G 1G RAM Dual Sim 3G Smartphone',
				'url'		:	'http://www.ebay.com/itm/Xiaomi-RED-RICE-Hongmi-Android-4-2-Quad-Core-1-5G-1G-RAM-Dual-Sim-3G-Smartphone-/151239857913?pt=Cell_Phones&hash=item23369916f9',
				'price'		:	218.28,
				'image'		:	'http://i.ebayimg.com/00/s/ODAwWDgwMA==/z/afYAAOxy-WxTCwL6/$_3.JPG'
			},
};
print 'test'
print '***|||RESULT|||***'
print json.dumps(result)
