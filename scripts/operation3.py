#!/usr/bin/python

import io
import sys
import csv
import urllib2
import time
from lxml import etree
import os
import yaml
import MySQLdb
import smtplib
import subprocess
#import signal
from BeautifulSoup import BeautifulSoup
import re
import mechanize
import cookielib
import urllib
try:
    import Image
except ImportError:
    from PIL import Image
import ftplib
import math
from datetime import datetime

def removenewline(str):
    newstr = str.replace('\n','<br>').replace('\r','<br>')
    return newstr

def liststrip(list):
    for i in range(len(list)):
        list[i] = list[i].strip()

def getFeeRates(feecat,dbname='webdb2'):
    feetuple=()
    query = "SELECT tier1,tier2,tier3 from ebayCat where catNum='NotInList'"
    if type(feecat) is tuple or type(feecat) is list:
        for item in feecat:
            query = query+" OR catNum="+"'"+item+"'"
        #print query
    elif type(feecat) is str:
        query = query+" OR catNum="+"'"+feecat+"'"
        #print query
    else:
        print "feecat is %s. Please use tuple, string or list" %type(feecat)
        return(feetuple)        
    dblogin=getDBLogin(dbname)
    try:
        db=MySQLdb.connect(host=dblogin['host'],user=dblogin['username'],passwd=dblogin['password'],db=dblogin['database'])
        cur = db.cursor()
        cur.execute(query)
        feetuple=cur.fetchone()
    except Exception, e:
        print e
    if db: db.close()
    return(feetuple)
#end of getFeeRates(feecat)

def priceCalc(amazondict={},othersource=[],feecat='unknown',ebaypricemin=0,gsflag=0,margin=0.08,primelimit=35):
    #Notes:
    #format of amazondict = (price,availability,prime), e.g. {'price':29.99,'availability':1,'prime':1}
    #format of othersource = [{site:'overstock','price':29.99,'availability':1,'prime':1},{},...]
    #feecat can be string, tuple or list of category numbers. feecat can also be a fee tuple like (0.13,0.06,0.02) to improve speed
    #default values 
    newprice = 2999
    paypalfee = 0.029
    gsmarkup = 0.05
    primemarkup = 0.05
    feetuple=()

    #Local function
    def bestDict(sourcelist):
        #to be developed
        if len(sourcelist) == 1:
            return(sourcelist[0])
    #end of local function bestDict(sourcelist)
    
    def calculator(d,t,gs=0,lowcost=0):
        targetprice = 2999
        #11-27-2013 change lowcostadder = 5
        lowcostadder = 3
        #for amazon items, add $8 shipping to item less than $35
        if lowcost==1: lowcostadder = 8 
        feetieradder = 5 
        #price and availability are required in d.
        if 'price' not in d or 'availability' not in d:
            pass
        else:
            if int(d['availability'])==0:
                return(targetprice)
            if float(d['price'])<45:
                feerate = float(t[0])
                feetieradder = 0
            else:
              try:
                feerate = float(t[1])
              except:
                print "DEBUG",d,t
              feetieradder = 50 * (float(t[0])-float(t[1]))
            targetprice = float(d['price'])*(1+feerate)/(1-float(margin)-float(paypalfee))+feetieradder
	    if float(d['price']) < primelimit:
                targetprice += lowcostadder
            if int(d['availability'])>5:
                targetprice += 5
            if not d.get('prime') or d.get('prime')=='0':
                targetprice *= (1+primemarkup)
            if gs==1 or gs=='1':
                targetprice *= (1+gsmarkup)
        return(targetprice)
        #end of local function calculator(d,t,gs=0)

    #get ebay fee rates (<50,50-100,>100)
    if feecat <> 'unknown':
        if type(feecat) == tuple and len(feecat) == 3:
            feetuple = feecat
        else:
            feetuple = getFeeRates(feecat)
    if not feetuple:
        feetuple= (0.09,0.09,0.09)
    #added 7/18/2013 to resolve freshprice hang due to new catnum issue
    elif not feetuple[0]:
        feetuple= (0.09,0.09,0.09)

    #Get best option from all other sources
    if not othersource:
        otherdict = {}
    else:
        otherdict = bestDict(othersource)
    newprice2 = calculator(otherdict,feetuple,gsflag)
    if not amazondict:
        newprice = newprice2
    else:
        newprice1=calculator(amazondict,feetuple,gs=gsflag,lowcost=1)
        newprice = min(newprice1,newprice2)
    if newprice < ebaypricemin:
        if newprice*1.2 < ebaypricemin:
            newprice = newprice*1.2
	else:
            newprice = float(ebaypricemin) - 1

    return(newprice)
#end of priceCalc()

def getDBLogin(dbname):

    dirs = [ '.', os.environ.get('HOME'), '/etc' ]
    # print dirs
    config_file = 'dbconfig_file.yaml'
    for mydir in dirs:
        myfile = "%s/%s" % (mydir, config_file)
        if os.path.exists( myfile ):
            try:
                f = open( myfile, "r" )
            except IOError, e:
                print "unable to open file %s" % e

            #print "using file %s" % myfile

            yData  = yaml.load( f.read() )

            dblogin = yData.get(dbname, {})

            return dblogin

# def url2HTML(url,parser='etree'): 
    # urllib2Header = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.57 Safari/537.1'}
    # tryCount = 0
    # root = {}
    # while True: #Retry 20 times to avoid temporary connection issue.
        # tryCount += 1
        # try:
            # req = urllib2.Request(url, headers=urllib2Header)
            # t1 = time.time()
            # if parser=='etree':
                # root = etree.HTML(urllib2.urlopen(req, timeout = 15).read())
            # elif parser=='soup':
                # root = BeautifulSoup(urllib2.urlopen(req, timeout = 15).read())
            # if time.time()-t1 > 14.5: 
                # print 'urllib2.urlopen() timed out: %s' % url
                # print 'Retry #%d' % tryCount
                # if tryCount>=20:
                    # break
                # else: continue
        # except Exception, e:
            # print ('Cannot open url: %s, retry #%d' % (url, tryCount))
            # if tryCount>=20:   
                # print e
                # break
            # else: continue
        # break
    # return root

# #End of url2HTML()


def url2HTML(url,parser='etree'):
    '''
    root = url2HTML(url,parser='etree')
    Get the etree or BeautifulSoup root from url.
    This function calls url2str and then uses etree.HTML or BeautifulSoup to get the root node.
    
    --Input
    url: Url address, must begin with 'http://'
    parser = 'etree': The parser to the html string. Must be either 'etree' or 'soup'.
    
    --Output
    root: etree or BeautifulSoup root node for the retrieved html. Return {} if no html can be retrived from the url.
    '''
    
    try:
        if parser=='etree':
            htmlStr = url2str(url)
        elif parser == 'soup':
            htmlStr = url2str(url,parser='soup') 
        # f = open('url.html', 'w')
        # f.write(htmlStr)
        # f.close()
        
        if not htmlStr: 
            return {}
        elif parser=='etree':
            root = etree.HTML(htmlStr)
        elif parser=='soup':
            root = BeautifulSoup(htmlStr)
        else:
            print ('Error: Parser can only be "etree" or "soup". Return blank dictionary.')
            return {}
        
        return root
        
    except Exception, e:
        print ('Error when using url2HTML. Return blank dictionary.')
        print e
        return {}

#End of url2HTML()


def url2str(url,parser='etree'):
    '''
    retStr = url2str(url)
    Get the string from a url using urllib2.
    Try 20 times with timeout for each try 15 seconds. 
    If failed, return a blank string.
    
    --Input
    url: Url address, must begin with 'http://'
    
    --Output
    retStr: Retrieved string. Blank string if failed.
    3-13-2014: when parser='soup', return urlopen object
    '''
    
    urllib2Header = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.57 Safari/537.1'}
    tryCount = 0
    retStr = ''
    retObj = None
    while True: #Retry 20 times to avoid temporary connection issue.
        tryCount += 1
        try:
            req = urllib2.Request(url, headers=urllib2Header)
            t1 = time.time()
            if parser == 'soup':
                retObj = urllib2.urlopen(req, timeout = 15)
            elif parser == 'etree':
                retObj = urllib2.urlopen(req, timeout = 15)
                retStr = retObj.read()
                retUrl = retObj.geturl()
            if time.time()-t1 > 14.5: 
                print 'urllib2.urlopen() timed out: %s' % url
                print 'Retry #%d' % tryCount
                if tryCount>=20:
                    break
                else: continue
            #added 10-15-2013, if string is empty, retry
            if (retStr=='' or retStr==None) and retObj == None: 
                print 'urllib2.urlopen() empty string: %s' % url
                print 'Retry #%d' % tryCount
                if tryCount>=20:
                    break
                else: continue
        except Exception, e:
            print ('Cannot open url: %s, retry #%d' % (url, tryCount))
            if tryCount>=20:   
                print e
                break
            else: continue
        break
    if parser == 'etree':
        return retStr
    if parser == 'soup':
        return retObj

#End of url2str()


def url2strmore(url,parser='etree'):
    '''
    retStr = url2str(url)
    Get the string from a url using urllib2.
    Try 20 times with timeout for each try 15 seconds. 
    If failed, return a blank string.
    
    --Input
    url: Url address, must begin with 'http://'
    
    --Output
    retStr: Retrieved string. Blank string if failed.
    3-13-2014: when parser='soup', return urlopen object
    '''
    
    urllib2Header = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.57 Safari/537.1'}
    tryCount = 0
    retStr = ''
    retUrl = ''
    retObj = None
    while True: #Retry 20 times to avoid temporary connection issue.
        tryCount += 1
        try:
            req = urllib2.Request(url, headers=urllib2Header)
            t1 = time.time()
            if parser == 'soup':
                retObj = urllib2.urlopen(req, timeout = 15)
            elif parser == 'etree':
                retObj = urllib2.urlopen(req, timeout = 15)
                retStr = retObj.read()
                retUrl = retObj.geturl()
            if time.time()-t1 > 14.5: 
                print 'urllib2.urlopen() timed out: %s' % url
                print 'Retry #%d' % tryCount
                if tryCount>=20:
                    break
                else: continue
            #added 10-15-2013, if string is empty, retry
            if (retStr=='' or retStr==None) and retObj == None: 
                print 'urllib2.urlopen() empty string: %s' % url
                print 'Retry #%d' % tryCount
                if tryCount>=20:
                    break
                else: continue
        except Exception, e:
            print ('Cannot open url: %s, retry #%d' % (url, tryCount))
            if tryCount>=20:   
                print e
                break
            else: continue
        break
    if parser == 'etree':
        return retStr, retUrl
    if parser == 'soup':
        return retObj

#End of url2strmore()



def emailalert(subject, msg, toaddr=['jwang6@gmail.com', 'yuc134@gmail.com', 'happitail.auto@gmail.com']):
    #Connect to gmail server.     
    usr = 'happitailing@gmail.com'
    psw = getDBLogin('emails')[usr.split('@')[0]]
    fromaddr = 'happitailing@gmail.com'
    server=smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(usr,psw)

    gmtime = time.gmtime()
    timeAbsNow = int(time.mktime(gmtime))
    date = time.strftime("%Y-%m-%d", gmtime)
    #clocktime = time.strftime("%H:%M:%S", gmtime)

    m="Date: %s\r\nFrom: %s\r\nTo: %s\r\nSubject: %s\r\nX-Mailer: My-Mail\r\n\r\n" % (date, fromaddr, toaddr, subject)
    server.sendmail(fromaddr,toaddr,m+msg)
    
    server.quit()
#End of emailalert


def emailalertHTML(subject, msg, toaddr):
    '''
    emailalertHTML(subject, msg, toaddr)
    Send email with html format. happitailing@gmail.com is used as sender address.
    
    --Input
    subject: Email subject, string. 
    msg: Email body in html, string.
    toaddr: Recipient address, list of strings. E.g. ['jwang6@gmail.com', 'yuc134@gmail.com', 'happitail.auto@gmail.com']
    
    --Output
    No output.
    '''
    
    
    ##Connect to gmail server.     
    usr = 'happitailing@gmail.com'
    psw = getDBLogin('emails')[usr.split('@')[0]]
    fromaddr = usr
    #toaddr = ['jwang6@gmail.com', 'yuc134@gmail.com', 'happitail.auto@gmail.com']
    # toaddr = 'jwang6@gmail.com'
    server=smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(usr,psw)

    ##Construct email headers.
    gmtime = time.gmtime()
    timeAbsNow = int(time.mktime(gmtime))
    date = time.strftime("%Y-%m-%d", gmtime)
    #clocktime = time.strftime("%H:%M:%S", gmtime)
    
    m=("Date: %s\r\nFrom: %s\r\nTo: %s\r\nSubject: %s\r\nX-Mailer: My-Mail\r\nContent-Type: text/html;charset=UTF-8\r\nContent-Transfer-Encoding: quoted-printable\r\n\r\n" 
        % (date, fromaddr, toaddr, subject))
    
    
    ##Email protocol formatting: Convert '=' to '=3D'.
    msg = re.sub('=(?!3D)', '=3D', msg)
    #print m+msg
    

    server.sendmail(fromaddr,toaddr,m+msg)
    server.quit()
#End of emailalertHTML(subject, msg, toaddr)

def emailForwardHTML(subject, comment, msg, toaddr):
    #Connect to gmail server.
    usr = 'happitailing@gmail.com'
    psw = getDBLogin('emails')[usr.split('@')[0]]
    fromaddr = usr
    #toaddr = 'jwang6@gmail.com; yuc134@gmail.com'
    server=smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(usr,psw)

    forwardNote = '---------- Forwarded message ----------<br>'
    forwardNote += ('From: '+msg['From'].replace('<', '').replace('>', '')+'<br>')
    forwardNote += ('Date: '+msg['Date']+'<br>')
    forwardNote += ('Subject: '+msg['Subject']+'<br>')
    forwardNote += ('To: '+msg['To'].replace('<', '').replace('>', '')+'<br><br>')
    
    msg.replace_header('From', fromaddr)
    msg.replace_header('To', toaddr)
    msg.replace_header('Subject', subject)
    
    bodyStr = re.findall('<body[\s\S]*?>', msg.as_string())
    if bodyStr:
        #print bodyStr[0]
        msgString = msg.as_string().replace(bodyStr[0], (bodyStr[0]+comment+'<br>'*3+forwardNote), 1)
    #print msgString
    else:
        print 'This is not an html email'
    
    
    
    msgString = msgString.encode('ascii', 'ignore')
    
    
    f = open('email1.txt', 'w')
    f.write(msgString)
    f.close()
    
    server.sendmail(fromaddr, toaddr.split('; '), msgString)
    
    server.quit()
    
#End of emailForwardHTML(subject, comment, msg)


def runscript(current,previous,check_output=0,cmd='python',db='localdb1'):
    def dboperation(database,command):
        dblogin = getDBLogin(database)
        conn = None
        try:
            conn=MySQLdb.connect(host=dblogin['host'], user=dblogin['username'], passwd=dblogin['password'], db=dblogin['database'])
            cursor = conn.cursor()
            cursor.execute(command)
            conn.commit()
            conn.close()
        except MySQLdb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])
            sys.exit(1)
    
    def dbfetchone(database,command):
        dblogin = getDBLogin(database)
        conn = None
        data = ()
        try:
            conn=MySQLdb.connect(host=dblogin['host'], user=dblogin['username'], passwd=dblogin['password'], db=dblogin['database'])
            cursor = conn.cursor()
            cursor.execute(command)
            data = cursor.fetchone()
            conn.commit()
            conn.close()
        except MySQLdb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])
            sys.exit(1)
        return data


    message = ''
    commlist=[] 
    starttime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())

    commlist = [cmd] + current.strip().split(' ')
    if previous == 'NA':
        command = "insert into processstatus (script,start_time) values('%s','%s')" %(current,starttime)
        dboperation(db,command)
        if check_output ==1:
            try:
                message = subprocess.check_output(commlist)
                flag = 0
            except Exception,e:
                flag = 1
                message = e
        else:
            flag=subprocess.call(commlist)
        #flag =0 when pass and flag >0 when fail
        command = """update processstatus set flag='%s',message = '%s',end_time=current_timestamp
                          where script = '%s' and
                          start_time = '%s'""" %(flag,message,current,starttime)
        dboperation(db,command)
        if flag > 0:
            emailalert('Script Failed!',current)

    else:
        command = """select flag from processstatus where script = '%s'
                          order by start_time desc limit 1""" %previous
        data = dbfetchone(db,command)[0]
        if data >0 or data == None:
            #previous script failed
            command="insert into processstatus values ('%s',current_timestamp,current_timestamp,999,'Previous script failed')" %current
            dboperation(db,command)
            emailalert('Previous Script Failed!',current)
        else:
            command="insert into processstatus (script,start_time) values('%s','%s')" %(current,starttime)
            dboperation(db,command)
            if check_output ==1:
                try:
                    message = subprocess.check_output(commlist)
                    flag = 0
                except Exception,e:
                    flag = 1
                    message = e
            else:
                flag=subprocess.call(commlist)
            #flag =0 when pass and flag =1 when fail
            command="""update processstatus set flag='%s',message='%s',end_time=current_timestamp
                          where script = '%s' and 
                          start_time = '%s'""" %(flag,message,current,starttime)
            dboperation(db,command)
            if flag > 0:
                emailalert('Script Failed!',current)
#End of runscript

def ebayreport(account,type):
    br = mechanize.Browser()
    cj = cookielib.LWPCookieJar()
    br.set_cookiejar(cj)
    br.set_handle_equiv(True)
    br.set_handle_gzip(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)
    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

    login=getDBLogin(account)
    ebay_userid = login['username']
    ebay_pwd = login['password']

    if type=='active':
       listing_filter = ['3']
       date_range_type = ['1']

    if type=='ship':
       listing_filter = ['6']
       date_range_type = ['1']
    br.open('http://my.ebay.com/ws/eBayISAPI.dll?MyeBay')

    br.select_form(name="SignInForm")
    br.form['userid'] = ebay_userid
    br.form['pass'] = ebay_pwd
    br.submit()

    req = br.click_link(text="Continue")
    resp = br.open(req)

    links = list(br.links(text="File Exchange"))

    req = br.click_link(links[0])
    resp = br.open(req)

    req = br.click_link(text="Create a Download Request")
    resp = br.open(req)

    br.select_form(name="formDownload")
    br.form['ListingFilter'] = listing_filter
    br.submit()

    br.select_form(name="formDownload")
    br.form['DateRangeType'] = date_range_type
    resp = br.submit()

    html = resp.get_data()

    id = str(html).find('Your ref # is')
    temp = str(html)[id:]
    id1 = temp.find('.')
    ref_number = temp[:id1].split(" ")[4]
    #print temp[:id1]
    return(ref_number)
#end of ebayreport


# def getAmznInfo(asin):
    
    # priceinfo = {'sku' : asin}
    # priceinfo['produrl'] = 'http://www.amazon.com/dp/'+asin
    # priceinfo['title'] = ''
    # priceinfo['shipping'] = 999
    # priceinfo['prime'] = 0
    # priceinfo['availability' ] = 0
    # priceinfo['maxqty'] = 1
    # priceinfo['thirdparty'] = 1
    # priceinfo['qtyInStock'] = 20
    # priceinfo['add-on'] = 0
   
    # try:
        # url = 'http://www.amazon.com/dp/'+asin
        # root = url2HTML(url)
        
    
        # buyBlkTags = root.xpath('.//form[@id="handleBuy"]')
        # if buyBlkTags:
            # print 'Format 1'
            # buyblk = buyBlkTags[0]
    
            # #Get title.
            # title = ''.join(buyblk.xpath('.//span[@id="btAsinTitle"]//text()'))
            # priceinfo['title']=title
    
            # #Get price and prime info.
            # pricetag = buyblk.xpath('.//td[@id="actualPriceContent"]/span[@id="actualPriceValue"]/b[@class="priceLarge"]')
            # #Larry added on 3-14-13 to catch some books with both new and rental
            # if not pricetag: pricetag = buyblk.xpath('.//td[@class="rightBorder buyNewOffers"]/span[@class="rentPrice"]')
            # #Larry added on 9-6-13 to catch some books with both new and rental
            # #if not pricetag: pricetag = buyblk.xpath('.//td[@class=re.compile("buyNewOffers")]/span[@class="rentPrice"]')
            # if not pricetag: pricetag = buyblk.xpath('.//td[@class=" buyNewOffers"]/span[@class="rentPrice"]')
            # if (pricetag): #if price is displayed
                # priceinfo['price'] = float(pricetag[0].text.strip().strip('$').replace(',',''))
                # priceinfo['prime'] = 0
                # priceinfo['shipping'] = 999
                # priceinfo['availability'] = 0
                # #if free shipping available, it's prime eligible
                # if 'free' in etree.tostring(pricetag[0].getparent().getparent(), method='text', encoding='utf-8').lower():
                    # priceinfo['prime'] = 1
                    # priceinfo['shipping'] = 0

            # else: #If price is "too low to display"
                # if buyblk.xpath('.//td[@id="actualPriceContent"]/span[@id="actualPriceValue"]//a[@target="WhyNoPrice"]'):
                    # extrainfo = getAmznPriceHF(asin)
                    # if 'price' in extrainfo:
                        # priceinfo['price'] = extrainfo['price']
                        # priceinfo['prime'] = 0
                        # priceinfo['shipping'] = 999
                        # priceinfo['availability'] = 0
                        # #if free shipping available, it's prime eligible
                        # shptag = buyblk.xpath('.//td[@id="shippingMessageStandAlone"]')
                        # if shptag:
                            # if 'free' in etree.tostring(shptag[0], method='text', encoding='utf-8').lower():
                                # priceinfo['prime'] = 1
                                # priceinfo['shipping'] = 0
            
            # if not ('price' in priceinfo):
                # priceinfo['price'] = 4999
                # priceinfo['maxqty'] = 0
                # priceinfo['availability'] = 0
            # else:
            # #Get the shipping info if not prime.
                # if not priceinfo.get('prime', 0):
                    # shptag = buyblk.xpath('.//span[@class="plusShippingText"]')
                    # if shptag:
                        # if 'free' in shptag[0].text.lower():
                            # priceinfo['shipping'] = 0
                        # else:
                            # if len(shptag[0].text.split('$'))>1:
                                # priceinfo['shipping'] = float(shptag[0].text.split('$')[1].split(u'\xa0')[0])
                
                # #Get availability info.
                # priceinfo['availability']=0
                # availtag = buyblk.xpath('.//span[@class="availGreen"]')
                # if availtag:
                    # priceinfo['availability'] = 1
                    # #Get the qtyInStock information. This field is only meaningful when availability = 1.
                    # availtext = availtag[0].text
                    # if 'Only' in availtext:
                        # priceinfo['qtyInStock'] = int(availtext.split(' ')[1])
                # else:
                    # availtag = buyblk.xpath('.//span[@class="availOrange"]')
                    # if availtag:
                        # availtext = availtag[0].text
                        # if 'released' in availtext.lower():
                            # priceinfo['availability'] = 1
                        # elif 'day' in availtext.lower():
                            # priceinfo['availability'] = availtext.lower().split('day')[0].split()[-1]
                # if availtag:
                    # sellertext = ''.join(availtag[0].xpath('../descendant-or-self::text()'))
                    # if 'sold by amazon.com' in sellertext.lower():
                        # priceinfo['thirdparty'] = 0
                    # else:
                        # priceinfo['thirdparty'] = 1
    
            # #Get maximum order quantity info.
            # maxqty = 0
            # if buyblk.xpath('.//select[@id="quantity"]/option'):
                # #print etree.tostring(buyblk.xpath('.//select[@id="quantity"]/option')[0])
                # maxqty = int(buyblk.xpath('.//select[@id="quantity"]/option')[-1].text)
                # priceinfo['maxqty'] = maxqty
        # else:
            # #Get title when "handleBuy" does not exist.This is usually for books
            # print 'No buy block found'
            # #print priceinfo
            # title = ''.join(root.xpath('.//h1[@id="title"]//text()'))
            # priceinfo['title']=title.split('\n')[0]

            # #Get price, availability, prime information for books
            # buyboxes = root.xpath('.//div[@id="buybox"]')
            # if buyboxes:
                # buybox = buyboxes[0]
                # #Only get price related information for new items
                # newprice = ''.join(buybox.xpath('.//div[@id="buyNewSection"]//text()'))
                # #print str(newprice)
                # if newprice.find('$')>0:
                    # priceinfo['price'] = float(newprice.split('$')[1].replace(',',''))
                # else:
                    # priceinfo['price'] = 4999
                # #Get prime info: option1
                # if buybox.xpath('.//div[@id="buyNewSection"]//span[@class="primeBadge inlineBlock-display prime-padding"]'):
                    # priceinfo['prime'] = 1
                    # priceinfo['shipping']=0
                # else:
                    # priceinfo['prime'] = 0
                    # #hardcode shipping to $4
                    # priceinfo['shipping']= 4
                # #get availability, maxquantity and third party flag
                # buyNewInner = buybox.xpath('.//div[@id="buyNewInner"]')
                # if buyNewInner:
                    # #print "inside buyNewInner"
                    # buyNewInner0 = buyNewInner[0]
                    # #Get maximum order quantity info.
                    # maxqty = 0
                    # if buyNewInner0.xpath('.//select[@id="quantity"]/option'):
                        # maxqty = int(buyNewInner0.xpath('.//select[@id="quantity"]/option')[-1].text.strip('+'))
                        # priceinfo['maxqty'] = maxqty
                    # #Get availability
                    # priceinfo['availability']=0
                    # availText = ''.join(buyNewInner0.xpath('.//div[@id="availability"]//text()'))
                    # #print availText
                    # if availText.lower().find('in stock')>0:
                        # priceinfo['availability']=1
                    # #Get thirdparty information
                    # priceinfo['thirdparty']=1
                    # merchantText = ''.join(buyNewInner0.xpath('.//div[@id="merchant-info"]//text()'))
                    # if merchantText.find('Amazon.com')>0:
                        # priceinfo['thirdparty']=1
                    # #Get prime info: option2
                    # if ''.join(buyNewInner0.xpath('.//text()')).find('on orders over $25')>0:
                        # priceinfo['prime'] = 1
                        # priceinfo['shipping']=0
                    # else:
                        # priceinfo['prime'] = 0
                        # #hardcode shipping to $4
                        # priceinfo['shipping']= 4

                # else:
                    # priceinfo['availability']=0
                    # priceinfo['maxqty']=0
                    # priceinfo['thirdparty']=1

            # #print priceinfo
            # #Added 10-15-2013. New Amazon format
            # price_feature = root.xpath('.//div[@id="price_feature_div"]')
            # #print etree.tostring(price_feature[0])
            # if price_feature:
                # print 'format 2'
                # #print "price_feature"
                # price_feature_text=''.join(price_feature[0].xpath('.//text()')).lower()
                # #print price_feature_text
                # #if price_feature_text.find('free'):
                # if 'free' in price_feature_text:
                    # priceinfo['shipping'] = 0
                # if price_feature_text.find('list price')>=0:
                    # newprice= price_feature_text.split('$')[2].split('\n')[0]
                # else:
                    # newprice= price_feature_text.split('$')[1].split('\n')[0]
                # priceinfo['price'] = float(newprice.replace(',',''))
                # #print priceinfo['price'] 
                
                # #newprice = ''.join(price_feature[0].xpath('.//span[@id="priceblock_ourprice"]//text()'))
                # #if newprice.find('$')>0:
                # #    priceinfo['price'] = float(newprice.split('$')[1].replace(',',''))
                # #else:
                # #    priceinfo['price'] = 4999
                
            # if not ('price' in priceinfo):
                # priceinfo['price'] = 4999
                # priceinfo['maxqty'] = 0
                # priceinfo['availability'] = 0
            # else:
                # # #Get the shipping info if not prime.
                # # if not priceinfo.get('prime', 0):
                    # # shptag = buyblk.xpath('.//span[@class="plusShippingText"]')
                    # # if shptag:
                        # # if 'free' in shptag[0].text.lower():
                            # # priceinfo['shipping'] = 0
                        # # else:
                            # # if len(shptag[0].text.split('$'))>1:
                                # # priceinfo['shipping'] = float(shptag[0].text.split('$')[1].split(u'\xa0')[0])
                # #Get availability
                # availability_feature = root.xpath('//div[@id="availability_feature_div"]')
                # if availability_feature:
                    # #print "availability_feature"
                    # availability_feature_text = ''.join(availability_feature[0].xpath('.//text()')).lower()
                    # if availability_feature_text.find('in stock')>0:
                        # priceinfo['availability']=1
        
        # #print priceinfo
        # ##Extract fields without dependence on "handleBuy" block.
        # #Add-on
        # addonTags = root.xpath('//div[@id="addonBuyboxID"]/child::*')
        # if addonTags: priceinfo['add-on'] = 1
        
        
        # #Get product features
        # features = ''
        # featureblk = root.xpath('.//div[@id="featurebullets_feature_div"]')
        # if not featureblk:
            # featureblk = root.xpath('.//h2[text()="Product Features"]/..')
        # if featureblk:
            # for bullet in featureblk[0].xpath('.//li'):
                # features = features + ' '.join(bullet.xpath('.//text()')) + '<br>'
            # priceinfo['features'] = features+'<br>'+priceinfo['features'] if 'features' in priceinfo else features
                # # if bullet.text:
                    # # features = features + bullet.text + '<br>'
            # # priceinfo['features'] = features
            
        # #Features may be loacated right after price.
        # if not features:
            # featureblk = root.xpath('.//div[@id="feature-bullets-atf"]')
            # if featureblk:
                # for bullet in featureblk[0].xpath('.//li'):
                    # features = features + ' '.join(bullet.xpath('.//text()')) + '<br>'
                # priceinfo['features'] = features+'<br>'+priceinfo['features'] if 'features' in priceinfo else features


        # #Get technical details
        # techdetails = ''
        # techblk = root.xpath('.//div[@id="technical-data_feature_div"]')
        # if not techblk:
            # techblk = root.xpath('.//h2[text()="Technical Details"]/..')
        # if techblk:
            # for bullet in techblk[0].xpath('.//li'):
                # if bullet.text:
                    # techdetails = techdetails + bullet.text + '<br>'
            # if techdetails == '':
                # for bullet in techblk[0].xpath('.//li'):
                    # techdetail = bullet.xpath('.//text()')
                    # liststrip(techdetail)
                    # techdetails = techdetails+''.join(techdetail)+'<br>'
        # priceinfo['techdetails'] = techdetails

        # #Get product details
        # details = ''
        # detailblk = root.xpath('.//div[@id="detail-bullets_feature_div"]')
        # if not detailblk:
            # detailblk = root.xpath('.//h2[text()="Product Details"]/..')
        # if detailblk:
            # for bullet in detailblk[0].xpath('.//li'):
                # detail = bullet.xpath('.//text()')
                # liststrip(detail)
                # detailtext = ' '.join(detail)
                # detailtextlower = detailtext.lower()
                # #see if it's customer review. If yes, stop
                # if 'average customer' in detailtextlower:
                    # break
                # elif 'amazon' in detailtextlower:
                    # break
                # elif 'asin' in detailtextlower:
                    # continue
                # elif 'shipping:' in detailtextlower:
                    # continue
                    
                # #Dimension
                # elif 'dimensions:' in detailtextlower:
                    # dims = detailtextlower.split('dimensions:')[-1].split('inches')[0].split('x')
                    # priceinfo['dimensions'] = sorted([float(dim) for dim in dims], reverse = True)
                    
                # #Weight
                # elif 'weight:' in detailtextlower:
                    # if 'pounds' in detailtextlower:
                         # priceinfo['weight'] = float(detailtextlower.split('weight:')[-1].split('pounds')[0])
                    # elif 'ounces' in detailtextlower:
                         # priceinfo['weight'] = float(detailtextlower.split('weight:')[-1].split('ounces')[0])/16
                    # detailtext = detailtext.split('(')[0]
                    
                # #Isbn10
                # elif 'isbn-10:' in detailtextlower:
                    # priceinfo['isbn10'] = detailtextlower.split('isbn-10:')[-1].strip().upper()
                    
                # #Isbn13
                # elif 'isbn-13:' in detailtextlower:
                    # priceinfo['isbn13'] = detailtextlower.split('isbn-13:')[-1].strip().replace('-', '').upper()
                    
                # #Grab release date in various cases.
                # elif 'publisher:' in detailtextlower: 
                    # strRelDate = detailtextlower.split('(')[-1].split(')')[0].strip()
                    # try: 
                        # timeRelDate = time.strptime(strRelDate, '%B %d, %Y')
                        # priceinfo['releaseDate'] = time.strftime("%Y-%m-%d", timeRelDate)
                    # except Exception, e:
                        # try: 
                            # timeRelDate = time.strptime(strRelDate, '%B %Y')
                            # priceinfo['releaseDate'] = time.strftime("%Y-%m-%d", timeRelDate)
                        # except Exception, e:
                            # try:
                                # timeRelDate = time.strptime(strRelDate, '%Y')
                                # priceinfo['releaseDate'] = time.strftime("%Y-%m-%d", timeRelDate)
                            # except Exception, e:
                                # print ("Warning: Cannot get release date from item url: "+url)
                                # print e
                                # print detailtext

                        
                # details = details+detailtext+'<br>'
        # priceinfo['details'] = details
        
        
        # #Get large image url
        # imgblk = root.xpath('.//table[@class="productImageGrid"][1]')
        # if imgblk:
            # imgtag = imgblk[0].xpath('.//img[1]')
            # imgurl = imgtag[0].get('src', '') if imgtag else ''
            # imgurlSplit = imgurl.split('/I/', 1)
            # if len(imgurlSplit)>1:
                # imgurl = imgurlSplit[0]+'/I/'+imgurlSplit[1].split('.', 1)[0]+'.'+imgurlSplit[1].split('.')[-1]
            
            # priceinfo['imgurl'] = imgurl
       

    # except Exception, e:
        # print asin
        # print e
        # return priceinfo
    # #if 'price' not in priceinfo:
    # #    f = open(asin+'.html','w')
    # #    f.write(etree.tostring(root))
    # #    f.close
    # #elif priceinfo['price']>2998:
    # #    f = open(asin+'.html','w')
    # #    f.write(etree.tostring(root))
    # #    f.close

    # return priceinfo

# #End of getAmznInfo(asin)


def getAmznInfo(asin):
    
    priceinfo = {'sku' : asin}
    priceinfo['produrl'] = 'http://www.amazon.com/dp/'+asin
    priceinfo['title'] = ''
    priceinfo['shipping'] = 999
    priceinfo['prime'] = 0
    priceinfo['availability' ] = 0
    priceinfo['maxqty'] = 1
    priceinfo['thirdparty'] = 1
    priceinfo['qtyInStock'] = 20
    priceinfo['add-on'] = 0
   
    try:
        url = 'http://www.amazon.com/dp/'+asin
        htmlStr = url2str(url)
        
        priceinfo.update(parseAmznInfo(htmlStr))
        
        if asin.strip() != priceinfo['sku'].strip():
            priceinfo['availability' ] = 0
    
        #f = open(asin+'.html','w')
        #f.write(htmlStr)
        #f.close
       

    except Exception, e:
        print asin
        print e
        return priceinfo
    #if 'price' not in priceinfo:
    #    f = open(asin+'.html','w')
    #    f.write(etree.tostring(root))
    #    f.close
    #elif priceinfo['price']>2998:
    #    f = open(asin+'.html','w')
    #    f.write(etree.tostring(root))
    #    f.close

    return priceinfo

#End of getAmznInfo(asin)


#Amazon product page parser.
#To be added: 1, InStockQty and availability in days for book format
#2, The new format in which Technical Details and Additional information are in a box.
#12-28-2013: added code to read related products
def parseAmznInfo(strHTML):
       
    priceinfo = {}
            
    #Initial values. Note: 'price' is not intialized.
    priceinfo['title'] = ''
    priceinfo['shipping'] = 999
    priceinfo['prime'] = 0
    priceinfo['availability' ] = 0
    priceinfo['maxqty'] = 1
    priceinfo['thirdparty'] = 1
    priceinfo['qtyInStock'] = 20
    priceinfo['add-on'] = 0
    priceinfo['variation'] = {}
    
    getInfoHFCalled = 0
   
    try:
        root = etree.HTML(strHTML)
        
        #produrl and sku from meta header
        linkTags= root.xpath('//link[@rel="canonical"]')
        if linkTags:
            priceinfo['produrl'] = linkTags[0].get('href', '')
            
            if 'dp/' in priceinfo['produrl']:
                sku = priceinfo['produrl'].split('dp/')[-1]
            else:
                sku = priceinfo['produrl'].split('/')[-1]
            if len(sku) == 10:
                priceinfo['sku'] = sku
            # else:
                # print 'error: cannot find amazon asin.'
        else:
            pass
            # print 'Error: Cannot find product url tag in meta tags.'
            
        # #title
        # titleTags = root.xpath('//meta[@name="title"]')
        # if titleTags:
            # title = titleTags[0].get('content')
            # title = title.split('Amazon.com')[-1].split(':', 1)[-1].split(':')[0]
            # if len(title) and (not ('amazon' in title.lower())):
                # priceinfo['title'] = title
            # else:
                # print 'Error: Cannot find title or "amazon" appears in title.'
        # else:
            # print 'Error: Cannot find title tag in meta tags.'
        
        
        #Get product details and correct sku
        details = ''
        asin = ''
        isbn10 = ''
        detailblk = root.xpath('.//div[@id="detail-bullets_feature_div"]')
        if not detailblk:
            detailblk = root.xpath('.//h2[text()="Product Details"]/..')
        if detailblk:
            for bullet in detailblk[0].xpath('.//li'):
                detail = bullet.xpath('.//text()')
                liststrip(detail)
                detailtext = ' '.join(detail)
                detailtextlower = detailtext.lower()
                #see if it's customer review. If yes, stop
                if 'average customer' in detailtextlower:
                    break
                elif 'amazon' in detailtextlower:
                    break
                elif 'asin' in detailtextlower:
                    asin = detailtextlower.split('asin:')[-1].strip().upper()
                    continue
                elif 'shipping:' in detailtextlower:
                    continue
                    
                #Dimension
                elif 'dimensions:' in detailtextlower:
                    dims = detailtextlower.split('dimensions:')[-1].split('inches')[0].split('x')
                    priceinfo['dimensions'] = sorted([float(dim) for dim in dims], reverse = True)
                    
                #Weight
                elif 'weight:' in detailtextlower:
                    if 'pounds' in detailtextlower:
                         priceinfo['weight'] = float(detailtextlower.split('weight:')[-1].split('pounds')[0])
                    elif 'ounces' in detailtextlower:
                         priceinfo['weight'] = float(detailtextlower.split('weight:')[-1].split('ounces')[0])/16
                    detailtext = detailtext.split('(')[0]
                    
                #Isbn10
                elif 'isbn-10:' in detailtextlower:
                    isbn10 = detailtextlower.split('isbn-10:')[-1].strip().upper()
                    if len(isbn10) == 10:
                        priceinfo['isbn10'] = isbn10
                    
                #Isbn13
                elif 'isbn-13:' in detailtextlower:
                    priceinfo['isbn13'] = detailtextlower.split('isbn-13:')[-1].strip().replace('-', '').upper()
                    
                #Grab release date in various cases.
                elif 'publisher:' in detailtextlower: 
                    strRelDate = detailtextlower.split('(')[-1].split(')')[0].strip()
                    try: 
                        timeRelDate = time.strptime(strRelDate, '%B %d, %Y')
                        priceinfo['releaseDate'] = time.strftime("%Y-%m-%d", timeRelDate)
                    except Exception, e:
                        try: 
                            timeRelDate = time.strptime(strRelDate, '%B %Y')
                            priceinfo['releaseDate'] = time.strftime("%Y-%m-%d", timeRelDate)
                        except Exception, e:
                            try:
                                timeRelDate = time.strptime(strRelDate, '%Y')
                                priceinfo['releaseDate'] = time.strftime("%Y-%m-%d", timeRelDate)
                            except Exception, e:
                                print ("Warning: Cannot get release date from item url: ")
                                print e
                                print detailtext

                        
                details = details+detailtext+'<br>'
        priceinfo['details'] = details
        if len(asin) == 10:
            priceinfo['sku'] = asin
        elif len(isbn10) == 10:
            priceinfo['sku'] = isbn10
        if not (len(priceinfo.get('sku', '')) == 10): 
            # print 'error: cannot find amazon asin.'
            return priceinfo
        
        sku = priceinfo['sku']
       
        
        #Amazon product page are formatted based on several different templates.
        #Format 1: The old format. Based on <form id="handleBuy">
        buyBlkTags = root.xpath('.//form[@id="handleBuy"]')
        if buyBlkTags:
#             #Debug purpose
#             f = open(sku+'_Format1.html', 'w')
#             f.write(strHTML)
#             f.close()
#             raw_input()
        
            #Format 1. The conventional format.
            # print 'Format 1'
            buyblk = buyBlkTags[0]
    
            #Get title.
            title = ''.join(buyblk.xpath('.//span[@id="btAsinTitle"]//text()'))
            priceinfo['title']=title
    
            #Get price and prime info.
            pricetag = buyblk.xpath('.//td[@id="actualPriceContent"]/span[@id="actualPriceValue"]/b[@class="priceLarge"]')
            #Larry added on 3-14-13 to catch some books with both new and rental
            if not pricetag: pricetag = buyblk.xpath('.//td[@class="rightBorder buyNewOffers"]/span[@class="rentPrice"]')
            #Larry added on 9-6-13 to catch some books with both new and rental
            #if not pricetag: pricetag = buyblk.xpath('.//td[@class=re.compile("buyNewOffers")]/span[@class="rentPrice"]')
            if not pricetag: pricetag = buyblk.xpath('.//td[@class=" buyNewOffers"]/span[@class="rentPrice"]')
            if (pricetag): #if price is displayed
                priceinfo['price'] = float(pricetag[0].text.strip().strip('$').replace(',',''))
                priceinfo['prime'] = 0
                priceinfo['shipping'] = 999
                priceinfo['availability'] = 0
                #if free shipping available, it's prime eligible
                if 'free' in etree.tostring(pricetag[0].getparent().getparent(), method='text', encoding='utf-8').lower():
                    priceinfo['prime'] = 1
                    priceinfo['shipping'] = 0

            else: #If price is "too low to display"
                if buyblk.xpath('.//td[@id="actualPriceContent"]/span[@id="actualPriceValue"]//a[@target="WhyNoPrice"]'):
                    extrainfo = getAmznPriceHF(sku)
                    getInfoHFCalled += 1
                    if 'price' in extrainfo:
                        priceinfo['price'] = extrainfo['price']
                        priceinfo['prime'] = 0
                        priceinfo['shipping'] = 999
                        priceinfo['availability'] = 0
                        #if free shipping available, it's prime eligible
                        shptag = buyblk.xpath('.//td[@id="shippingMessageStandAlone"]')
                        if shptag:
                            if 'free' in etree.tostring(shptag[0], method='text', encoding='utf-8').lower():
                                priceinfo['prime'] = 1
                                priceinfo['shipping'] = 0
            
            if not ('price' in priceinfo):
                priceinfo['price'] = 4999
                priceinfo['maxqty'] = 0
                priceinfo['availability'] = 0
            else:
            #Get the shipping info if not prime.
                if not priceinfo.get('prime', 0):
                    shptag = buyblk.xpath('.//span[@class="plusShippingText"]')
                    if shptag:
                        if 'free' in shptag[0].text.lower():
                            priceinfo['shipping'] = 0
                        else:
                            if len(shptag[0].text.split('$'))>1:
                                priceinfo['shipping'] = float(shptag[0].text.split('$')[1].split(u'\xa0')[0])
                
                #Get availability info.
                priceinfo['availability']=0
                availtag = buyblk.xpath('.//span[@class="availGreen"]')
                if availtag:
                    priceinfo['availability'] = 1
                    #Get the qtyInStock information. This field is only meaningful when availability = 1.
                    availtext = availtag[0].text
                    if 'Only' in availtext:
                        priceinfo['qtyInStock'] = int(availtext.split(' ')[1])
                else:
                    availtag = buyblk.xpath('.//span[@class="availOrange"]')
                    if availtag:
                        availtext = availtag[0].text
                        if 'released' in availtext.lower():
                            priceinfo['availability'] = 1
                        elif 'day' in availtext.lower():
                            priceinfo['availability'] = availtext.lower().split('day')[0].split()[-1]
                if availtag:
                    sellertext = ''.join(availtag[0].xpath('../descendant-or-self::text()'))
                    if 'sold by amazon.com' in sellertext.lower():
                        priceinfo['thirdparty'] = 0
                    else:
                        priceinfo['thirdparty'] = 1
    
            #Get maximum order quantity info.
            maxqty = 0
            if buyblk.xpath('.//select[@id="quantity"]/option'):
                #print etree.tostring(buyblk.xpath('.//select[@id="quantity"]/option')[0])
                maxqty = int(buyblk.xpath('.//select[@id="quantity"]/option')[-1].text)
                priceinfo['maxqty'] = maxqty
                
            # if buyblk.xpath('.//label[@for="asinRedirect"]') or buyblk.xpath('.//table[@class="variations"]'):
                # priceinfo['variationAvailable'] = 1    
            
            #3-8-2014: Larry added used and trade-in code
            usedtag = None
            usedtags = buyblk.xpath('.//a[@class="buyAction olpBlueLink"]')
            #print usedtags
            for tag in usedtags:
                if "condition=used" in tag.get('href',''):
                    usedtag = tag
                    #print tag.get('href','')
                    #print usedtag
                    break
            if usedtag != None:
                usedprice = usedtag.xpath('../span[@class="price"]')[0].text
                priceinfo['priceused'] = float(usedprice.strip('$').replace(',',''))
                #print priceinfo['priceused']

            tradeinblk = []
            tradeinblk = buyblk.xpath('.//div[@id="tradeInBuyboxFeatureDiv"]')
            if tradeinblk != []:
                tradeintext = etree.tostring(tradeinblk[0])
                pricetradein = tradeintext.split('$')[1].split('<')[0].strip()
                priceinfo['pricetradein'] = float(pricetradein)
            # print '    Asin: %s' % priceinfo['sku']
            # print '    Prime: %d' % priceinfo['prime']  
            # print '    Price: %.2f' % priceinfo['price']
            # if 'priceused' in priceinfo.keys():
                # print '    Price Used: %.2f' % priceinfo['priceused']
            # if 'pricetradein' in priceinfo.keys():
                # print '    Price Tradein: %.2f' % priceinfo['pricetradein']
            # print '    Shipping: %.2f' % priceinfo['shipping']
        
        else:
            price_feature = root.xpath('.//div[@id="price_feature_div"]')
            #print "price_feature"
            #print etree.tostring(price_feature[0])
            if price_feature:
#                 #Debug purpose
#                 f = open(sku+'_Format2.html', 'w')
#                 f.write(strHTML)
#                 f.close()
            
                #Format 2: The new format. Added 10-15-2013. 
                # print 'Format 2'
                
                #Get title
                title = ''.join(root.xpath('.//h1[@id="title"]//text()'))
                priceinfo['title']=title.strip()

                #Price
                priceText = ''.join(price_feature[0].xpath('.//span[@id="priceblock_ourprice"]//text()'))
                if '$' in priceText:
                    priceinfo['price'] = float(priceText.split('$')[-1])
                #Prime
                primeText = ''.join(price_feature[0].xpath('.//span[@id="ourprice_shippingmessage"]//text()'))
                if 'free' in primeText.lower():
                    priceinfo['prime'] = 1
                    priceinfo['shipping'] = 0
                else: #New format of amazon: does not show ourprice_shippingmessage when you are not logged in.
                    # print '    New format of amazon: does not show ourprice_shippingmessage when you are not logged in.'
                    fastTrackText = ''.join(root.xpath('.//div[@id="fast-track-message"]//div//text()')).encode('windows-1252', 'ignore')
                    #print fastTrackText
                    if 'one-day' in fastTrackText.lower():
                        priceinfo['prime'] = 1
                        priceinfo['shipping'] = 0
                        
                #If cannot get price info, use the getAmznPriceHF() function.
                if not ('price' in priceinfo):
                    extrainfo = getAmznPriceHF(sku)
                    getInfoHFCalled += 1
                    if 'price' in extrainfo:
                        priceinfo['price'] = extrainfo['price']
                        priceinfo['prime'] = extrainfo['prime']
                        priceinfo['shipping'] = extrainfo['shippingfee']
                        priceinfo['availability'] = extrainfo['availability']
                
                if not ('price' in priceinfo):
                    priceinfo['price'] = 4999
                    priceinfo['maxqty'] = 0
                    priceinfo['availability'] = 0
                else:
                    #Get shipping fee
                    if not priceinfo.get('prime', 0):
                        shpText = ''.join(root.xpath('//span[contains(@class, "shipping3P")]//text()'))
                        if 'free' in shpText.lower():
                            priceinfo['shipping'] = 0
                        elif '$' in shpText:
                            priceinfo['shipping'] = float(shpText.split('$')[1].split()[0].replace(',', ''))
                            
                    #Get availability, instock qty, and third party info.
                    availabilityTags = root.xpath('//div[@id="availability_feature_div"]')
                    if availabilityTags:
                        #print "availabilityTags"
                        #Availability
                        availabilityText = ''.join(availabilityTags[0].xpath('./div[@id="availability"]//text()'))
                        if 'in stock' in availabilityText.lower():
                            priceinfo['availability'] = 1
                        if 'week' in availabilityText.lower():
                            priceinfo['availability'] = 0
                        elif 'day' in availabilityText.lower():
                            availStr = availabilityText.lower().split('day')[0].split()[-1]
                            if '-' in availStr:
                                availStr = availStr.split('-')[-1].strip()
                            priceinfo['availability'] = int(availStr)
                        #Instock qty
                        if 'only' in availabilityText.lower():
                            priceinfo['qtyInStock'] = int(availabilityText.lower().split('only')[1].split()[0])
                        #Third party flag
                        merchantText = ''.join(availabilityTags[0].xpath('./div[@id="merchant-info"]//text()'))
                        if 'sold by amazon.com' in merchantText.lower():
                            priceinfo['thirdparty'] = 0
                        else:
                            priceinfo['thirdparty'] = 1
                            
                #Get maximum order quantity info.
                maxqtyTags = root.xpath('.//select[@id="quantity"]/option')
                if maxqtyTags:
                    #print etree.tostring(maxqtyTags[0])
                    maxqty = int(maxqtyTags[-1].text)
                    priceinfo['maxqty'] = maxqty
                       
                # if root.xpath('.//div[@id="twister_feature_div"]/form[@id="twister"]/div'):
                    # priceinfo['variationAvailable'] = 1  
            
                #3-13-2014: Larry added used code
                usedtag = None
                usedtags = root.xpath('.//div[@id="olp_feature_div"]//span')
                #print usedtags
                for tag in usedtags:
                    if "condition=used" in etree.tostring(tag):
                        usedtag = tag
                        #print etree.tostring(tag)
                        #print usedtag
                        break
                if usedtag != None:
                    usedprice = usedtag.xpath('.//span[@class="a-color-price"]')[0].text
                    priceinfo['priceused'] = float(usedprice.strip('$').replace(',',''))
                    #print priceinfo['priceused']
                
                # print '    Asin: %s' % priceinfo['sku']
                # print '    Prime: %d' % priceinfo['prime']
                # print '    Price: %.2f' % priceinfo['price']
                # if 'priceused' in priceinfo.keys():
                    # print '    Priceused: %.2f' % priceinfo['priceused']
                # print '    Shipping: %.2f' % priceinfo['shipping']
                    
            else:
                'Format 3'
                # print 'Format 3: book format'
                #print priceinfo['availability']
                #print 'No buy block found'
                #print priceinfo
                
                #Get title when "handleBuy" does not exist.This is usually for books
                title = ''.join(root.xpath('.//h1[@id="title"]//text()'))
                priceinfo['title']=title.strip().split('\n')[0]

                #Get price, availability, prime information for books
                buyboxes = root.xpath('.//div[@id="buybox"]')
                #print 'Number of buyboxes: %d' % len(buyboxes)
                if buyboxes:
                    buybox = buyboxes[0]
                    #Only get price related information for new items
                    newprice = ''.join(buybox.xpath('.//div[@id="buyNewSection"]//text()'))
                    #print str(newprice)
                    if newprice.find('$')>0:
                        priceinfo['price'] = float(newprice.split('$')[1].replace(',',''))
                    # else:
                        # priceinfo['price'] = 4999                
                        
                    #Get prime info: option1
                    if buybox.xpath('.//div[@id="buyNewSection"]//span[@class="primeBadge inlineBlock-display prime-padding"]'):
                        priceinfo['prime'] = 1
                        priceinfo['shipping']=0
                    else:
                        priceinfo['prime'] = 0
                        #hardcode shipping to $4
                        priceinfo['shipping']= 4
                        
                    #get availability, maxquantity and third party flag
                    #Still missing availability and qtyInStock -Jiong
                    buyNewInner = buybox.xpath('.//div[@id="buyNewInner"]')
                    if buyNewInner:
                        #print "inside buyNewInner"
                        buyNewInner0 = buyNewInner[0]
                        #Get maximum order quantity info.
                        maxqty = 0
                        if buyNewInner0.xpath('.//select[@id="quantity"]/option'):
                            maxqty = int(buyNewInner0.xpath('.//select[@id="quantity"]/option')[-1].text.strip('+'))
                            priceinfo['maxqty'] = maxqty
                        #Get availability
                        priceinfo['availability']=0
                        availText = ''.join(buyNewInner0.xpath('.//div[@id="availability"]//text()'))
                        #print availText
                        if availText.lower().find('in stock')>0:
                            priceinfo['availability']=1
                        #Get thirdparty information
                        priceinfo['thirdparty']=1
                        merchantText = ''.join(buyNewInner0.xpath('.//div[@id="merchant-info"]//text()'))
                        if 'amazon.com' in merchantText.lower():
                            priceinfo['thirdparty']=0
                        #Get prime info: option2
                        if ''.join(buyNewInner0.xpath('.//text()')).find('on orders over $35')>0:
                            priceinfo['prime'] = 1
                            priceinfo['shipping']=0
                        else:
                            priceinfo['prime'] = 0
                            #hardcode shipping to $4
                            priceinfo['shipping']= 4

                    else:
                        priceinfo['availability']=0
                        priceinfo['maxqty']=0
                        priceinfo['thirdparty']=1

                #3-12-2014 Larry:get used price
                mediamatrix = None
                mediamatrix = root.xpath('.//div[@id="MediaMatrix"]')
                if mediamatrix != None:
                    selected = mediamatrix[0].xpath('.//li[@class="swatchElement selected"]')
                    if selected:
                        usedstring = etree.tostring(selected[0])
                        if usedstring.find("Used")>0:
                            priceused = usedstring.split('Used')[1].split('$')[1].split()[0].replace(',','')
                            priceinfo['priceused']=float(priceused)
                       

    
                    #If cannot get price info, use the getAmznPriceHF() function.
                    if not ('price' in priceinfo):
                        # print 'Cannot get price info from the item page, use getAmznPriceHF() to extract info.'
                        # print sku
                        extrainfo = getAmznPriceHF(sku)
                        getInfoHFCalled += 1
                        if 'price' in extrainfo:
                            priceinfo['price'] = extrainfo['price']
                            priceinfo['prime'] = extrainfo['prime']
                            priceinfo['shipping'] = extrainfo['shippingfee']
                            priceinfo['availability'] = extrainfo['availability']
                            
                    if not ('price' in priceinfo):
                        priceinfo['price'] = 4999
                        priceinfo['maxqty'] = 0
                        priceinfo['availability'] = 0
                        
        #3-12-2014 Larry:get tradein price, same for format 2 and format 3
        tradeinblk = root.xpath('.//div[@id="tradeInButton_feature_div"]')
        if tradeinblk != []:
            tradeintext = etree.tostring(tradeinblk[0])
            if tradeintext.find('$')>0:
                pricetradein = tradeintext.split('$')[1].split('<')[0].strip()
                priceinfo['pricetradein'] = float(pricetradein)
       
        #print priceinfo
        ##Extract fields without dependence on "handleBuy" block.
        #Add-on
        addonTags = root.xpath('//div[@id="addonBuyboxID"]/child::*')
        centercol = root.xpath('//div[@id="centerCol"]')
        if addonTags: priceinfo['add-on'] = 1
        #added 11-24-2013 by Larry
        elif centercol:
            if etree.tostring(centercol[0]).find('This item is available because of the Add-on program')>0:
                priceinfo['add-on'] = 1 
        
        
        #Get product features
        #Format 2
        features = ''
        featureblk = root.xpath('.//div[@id="featurebullets_feature_div"]')
        if not featureblk:
            featureblk = root.xpath('.//h2[text()="Product Features"]/..')
        if featureblk:
            for bullet in featureblk[0].xpath('.//li'):
                features = features + ' '.join(bullet.xpath('.//text()')) + '<br>'
            priceinfo['features'] = features+'<br>'+priceinfo['features'] if 'features' in priceinfo else features
                # if bullet.text:
                    # features = features + bullet.text + '<br>'
            # priceinfo['features'] = features
            
        #Format 1
        #Features may be loacated right after price.
        if not features:
            featureblk = root.xpath('.//div[@id="feature-bullets-atf"]')
            if featureblk:
                for bullet in featureblk[0].xpath('.//li'):
                    features = features + ' '.join(bullet.xpath('.//text()')) + '<br>'
                priceinfo['features'] = features+'<br>'+priceinfo['features'] if 'features' in priceinfo else features
                
        #Format 3
        if not features:
            featureblk = root.xpath('//div[@id="bookDescription_feature_div"]/noscript[1]')
            if featureblk:
                features = features + etree.tostring(featureblk[0]).split('<noscript>')[-1].split('</noscript>')[0].strip() 
                priceinfo['features'] = features+'<br><br>'+priceinfo['features'] if 'features' in priceinfo else features


        #Get technical details
        techdetails = ''
        techblk = root.xpath('.//div[@id="technical-data_feature_div"]')
        if not techblk:
            techblk = root.xpath('.//h2[text()="Technical Details"]/..')
        if techblk:
            for bullet in techblk[0].xpath('.//li'):
                if bullet.text:
                    techdetails = techdetails + bullet.text + '<br>'
            if techdetails == '':
                for bullet in techblk[0].xpath('.//li'):
                    techdetail = bullet.xpath('.//text()')
                    liststrip(techdetail)
                    techdetails = techdetails+''.join(techdetail)+'<br>'
        priceinfo['techdetails'] = techdetails
                
                
        #Get large image url
        imgurl = ''
        if not imgurl:
            imgblk = root.xpath('.//table[@class="productImageGrid"][1]')
            if imgblk:
                imgtag = imgblk[0].xpath('.//img[@id="main-image"][1]')
                if imgtag:
                    #print etree.tostring(imgtag[0])
                    imgurl = imgtag[0].get('rel', '')
                    if not imgurl:
                        imgurl = imgtag[0].get('src', '')
        if not imgurl:
            imgblk = root.xpath('.//div[@id="main-image-container"]')
            #print etree.tostring(imgblk[0])
            if imgblk:
                imgtag = imgblk[0].xpath('.//img[1]')
                if imgtag:
                    imgurl = imgtag[0].get('data-old-hires', '')
                    if not imgurl:
                        imgurl = imgtag[0].get('src', '')
                        #print "inside"
                        #print etree.tostring(imgtag[0])
                    #print "i am here", imgurl
        if not imgurl:
            imgblk = root.xpath('.//tr[@id="prodImageContainer"]')
            if imgblk:
                imgtag = imgblk[0].xpath('//img[@class="prod_image_selector"]')
                if imgtag:
                    imgurl = imgtag[0].get('src', '')
            
        imgurlSplit = imgurl.split('/I/', 1)
        if len(imgurlSplit)>1:
            imgurl = imgurlSplit[0]+'/I/'+imgurlSplit[1].split('.', 1)[0]+'.'+imgurlSplit[1].split('.')[-1]    
        priceinfo['imgurl'] = imgurl
        
       
        #Get variations Format 2 only
        twister_feature = root.xpath('.//div[@id="twister_feature_div"]')
        if twister_feature:
            variations = twister_feature[0].xpath('.//li[@class="swatchSelect"]')
            for item in variations:
                variation = item.get('title', '').split('select')[1].strip()
                priceinfo['title']=variation+' '+priceinfo['title']
                variationNameTags = item.xpath('../preceding-sibling::div[@class="a-row"][1]//label')
                #print variationNameTags
                if variationNameTags:
                    if variationNameTags[0].text.strip():
                        priceinfo['variation'][variationNameTags[0].text.strip().strip(':')] = variation
                        
            if not variations:
                variations = twister_feature[0].xpath('.//option[@class="dropdownSelect"]')
                for item in variations:
                    variation = item.text.strip()
                    priceinfo['title']=variation+' '+priceinfo['title']
                    variationNameTags = item.xpath('../../preceding-sibling::div[@class="a-row a-spacing-micro"][1]//label')
                    #print variationNameTags
                    if variationNameTags:
                        if variationNameTags[0].text.strip():
                            priceinfo['variation'][variationNameTags[0].text.strip().strip(':')] = variation
                    
        #get variations Format 1 only
        else:
            table_variations = root.xpath('.//table[@class="variations"]')
            if table_variations:
                variations = table_variations[0].xpath('.//b[@class="variationLabel"]')
                for variation in variations:
                    priceinfo['title']= variation.text.strip() + ' ' + priceinfo['title']
                    variationNameTags = variation.xpath('./preceding-sibling::b[@class="variationDefault"]')
                    #print variationNameTags
                    if variationNameTags:
                        if variationNameTags[0].text.strip():
                            priceinfo['variation'][variationNameTags[0].text.strip().strip(':')] = variation.text.strip()
                    
            else:
                table_variations = root.xpath('.//div[@class="buying" and select[@name="asin-redirect"]]')
                if table_variations:
                    variations = table_variations[0].xpath('.//option[@selected="selected"]')
                    for variation in variations:
                        priceinfo['title'] = variation.text.strip() + ' ' + priceinfo['title']
                        variationNameTags = variation.xpath('../preceding-sibling::strong[1]//label[@for="asinRedirect"]')
                        #print variationNameTags
                        if variationNameTags:
                            if variationNameTags[0].text.strip():
                                priceinfo['variation'][variationNameTags[0].text.strip().strip(':')] = variation.text.strip()
                        

        #get similar products Format 2 only. Added 12-29-2013
        sims = []
        sims_feature = root.xpath('.//div[@id="purchase-sims-feature"]')
        if sims_feature:
            simslist = sims_feature[0].xpath('.//a[@class="sim-img-title"]/@href')
            for sim in simslist:
                sims.append(sim.split('dp/')[-1].split('/')[0])
        if sims:
            priceinfo['sims'] = sims
            
        #3-12-2014 Larry: get top category
        rankTag = root.xpath('.//li[@id="SalesRank"]')
        if rankTag !=[]:
            rankText = etree.tostring(rankTag[0])
            if rankText.find(' in ')>0:
                topcategory = rankText.split(' in ')[1].split('(')[0].strip().replace('amp;','')
            elif rankText.find('pd_zg_hrsr_e_1_1')>0:
                topcategory = rankText.split('pd_zg_hrsr_e_1_1')[1].split('>')[1].split('<')[0].replace('amp;','')
            elif rankText.find('pd_zg_hrsr_hg_1_1')>0:
                topcategory = rankText.split('pd_zg_hrsr_hg_1_1')[1].split('>')[1].split('<')[0].replace('amp;','')
            priceinfo['category'] = topcategory
 
            
        #Try getAmznPriceHF as the last resort if price or shipping is not correct.
        if (priceinfo.get('price', 0)>=4999 or priceinfo.get('shipping', 0)>=999) and (not getInfoHFCalled):
            # print 'Try getAmznPriceHF as the last resort because price or shipping is not correct.'
            extrainfo = getAmznPriceHF(sku)
            getInfoHFCalled += 1
            if 'price' in extrainfo:
                priceinfo['price'] = extrainfo['price']
                priceinfo['prime'] = extrainfo['prime']
                priceinfo['shipping'] = extrainfo['shippingfee']
                priceinfo['availability'] = extrainfo['availability']
                
            # print '    Asin: %s' % priceinfo['sku']
            # print '    Prime: %d' % priceinfo['prime']
            # print '    Price: %.2f' % priceinfo['price']
            # print '    Shipping: %.2f' % priceinfo['shipping']
                                

    except Exception, e:
        print e
        print 'Exception in function parseAmznInfo(strHTML).'
        print priceinfo
        return priceinfo

    return priceinfo
    
#End of parseAmznInfo(strHTML)


def getAmznUPC(asin):
    '''
    apiInfo = getAmznUPC(aisn)
    Get UPC, brand and mpn using Amazon Product Advertising API

    --Input
    asin: Amazon api.
    
    --Output
    apiInfo: Amazon item information dictionary including following keys if available:
        upc;
        brand;
        mpn;
        description
    Return blank dictionary if error.
    '''
   
    try:
        apiInfo = {}
        apiParams = dict(Operation = 'ItemLookup', ItemId = asin, ResponseGroup = 'ItemAttributes,EditorialReview')
        apiStr, url = amznAPI2str(apiParams)
        print url
        
        if not apiStr: return apiInfo
        
        root = etree.XML(apiStr)
        
        #upc
        upcTag = root.xpath('//*[local-name() = "ItemAttributes"]/*[local-name() = "UPC"][1]')
        upc = upcTag[0].text if upcTag else ''
        apiInfo['upc'] = upc
        
        #brand
        brandTag = root.xpath('//*[local-name() = "ItemAttributes"]/*[local-name() = "Brand"][1]')
        brand = brandTag[0].text if brandTag else ''
        apiInfo['brand'] = brand
        
        #mpn
        mpnTag = root.xpath('//*[local-name() = "ItemAttributes"]/*[local-name() = "MPN"][1]')
        mpn = mpnTag[0].text if mpnTag else ''
        apiInfo['mpn'] = mpn
        
        #product description
        descTag = root.xpath('//*[local-name() = "EditorialReviews"]//*[local-name() = "Content"][1]/text()')
        #print descTag
        description = '<br><br>'.join(descTag)+'<br>'
        apiInfo['description'] = description
        
        return apiInfo
            
    except Exception, e:
        print 'Exception in getAmznUPC function.'
        print 'Asin: '+asin
        return apiInfo
        print e
        
#End of getAmznUPC(asin)
            

def getAmznInfo2DB(asin, itemInfo = {}, cur = None, update_upc = False, verbose = False,writeDB = True, result='source'):
    '''
    getAmznInfo2DB(asin, cur = None, update_upc = False, verbose = False)
    
    Get Amazon info and submit to database.
    
    --Input
    asin: Asin of amazon item(s). It can be a single string or a list of asin strings.
    cur = None: The cursor of the db to be submitted to. If None, just get the amazon info of the asin(s).
    update_upc = False: If true, update item upc, brand and mpn in database.
    verbose = False: If True, asin, title and db submission status of each item will be printed.
    9/20/2013: add writeDB = True to input to provide an option NOT to write to DB
    Add option to return itemsource or itemProduct 
    10/11/2013:
    If add-on ==1 from getAmznInfo, then set availability = 0 when commit to db.
    --Output
    itemSource: Item details from Amazon. Its type is the same as the input asin type (string or list).
    
    '''
    
    
    
    try:
        L = 0
        isInputList = 1
        if not type(asin)==list:
            asinList = [asin]   
            isInputList = 0
        else:
            asinList = asin
        
        itemSourceList = [] 
        itemProductList = [] 
        for i in range(0, len(asinList)):
            itemSource = getAmznInfo(asinList[i])   
            if update_upc:
                itemSource.update(getAmznUPC(asinList[i]))
            itemSourceList.append(itemSource)
            
            if cur or result.lower()=='db':
                itemProduct = {'asin': asinList[i]}
                
                itemProduct['produrl'] = itemSource.get('produrl', '')
                
                if itemSource.get('title', ''):
                    itemProduct['title'] = itemSource['title'].encode('windows-1252', 'ignore')
                    
                if verbose: print '%d: %s, %s' % (i, itemProduct['asin'], itemProduct.get('title', ''))
                
                if itemSource.get('isbn10', ''):
                    itemProduct['isbn10'] = itemSource['isbn10']
                
                if itemSource.get('isbn13', ''):
                    itemProduct['isbn13'] = itemSource['isbn13']
                
                if 'releaseDate' in itemSource:
                    itemProduct['releaseDate'] = itemSource['releaseDate']
                    
                    
                itemProduct['details'] = '<br>'.join([itemSource.get('features', ''), itemSource.get('techdetails', ''), itemSource.get('details', '')])
                if not itemProduct['details']:
                    del itemProduct['details']
                else:
                    itemProduct['details'] = itemProduct['details'].encode('windows-1252', 'ignore')
                
                
                itemProduct['price'] = itemSource.get('price', 4999)
                itemProduct['prime'] = itemSource.get('prime', 0)
                itemProduct['shipping'] = itemSource.get('shipping', 999)
                itemProduct['availability'] = itemSource.get('availability', 0)
                itemProduct['maxQty'] = itemSource.get('maxqty', 1)
                itemProduct['TPFlag'] = itemSource.get('thirdparty', 1)
                
                if itemSource.get('add-on', 0) == 1:
                    itemProduct['availability'] = 0                
                
                if itemSource.get('weight', 0):
                    itemProduct['weight'] = itemSource['weight']
                print len(itemSource.get('dimensions', [0])) 
                if len(itemSource.get('dimensions', [0]))==3:
                    itemProduct.update({['dimensionL', 'dimensionW', 'dimensionH'][j]:
                        itemSource.get('dimensions')[j] for j in range(0, 3)})
                elif len(itemSource.get('dimensions', [0]))==2:
                    itemProduct.update({['dimensionL', 'dimensionW'][j]:
                        itemSource.get('dimensions')[j] for j in range(0, 2)})
                if itemSource.get('imgurl', ''):
                    itemProduct['imgurl'] = itemSource['imgurl']
                
                if 'price' in itemProduct:
                    itemProduct['refreshTime'] = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
                
                if update_upc:
                    if itemSource.get('upc', ''):
                        itemProduct['upc'] = itemSource['upc']
                        
                    if itemSource.get('brand', ''):
                        itemProduct['brand'] = itemSource['brand'].encode('windows-1252', 'ignore')
                    
                    if itemSource.get('mpn', ''):
                        itemProduct['mpn'] = itemSource['mpn'].encode('windows-1252', 'ignore')
                    
                    if itemSource.get('description', ''):
                        itemProduct['description'] = itemSource['description'].encode('windows-1252', 'ignore')
                    
                #print itemProduct
                itemProductList.append(itemProduct)
                if writeDB and cur: 
                    L = insertDB([itemProduct], cur, 'prodAmazon', dupHandling='update')
                    #L = updateDB([asinList[i]], [itemProduct], cur, 'prodAmazon')
                if verbose:
                    if L: print 'Item updated in db.'
                    else: print 'Item not updated in db.'
        
        if isInputList:
            if result.lower() == 'source':
                return itemSourceList
            elif result.lower() =='db':
                return itemProductList
            else:
                return itemSourceList
        else:
            if result.lower() == 'source':
                return itemSourceList[0]
            elif result.lower() == 'db':
                return itemProductList[0]
            else:
                return itemSourceList[0] 
                
    except Exception, e:
        print 'Exception in getAmznInfo2DB function.'
        return itemSourceList
        print e
        
#End of getAmznInfo2DB(asin)



def getAmznPriceHF(asin):
# Get amazon hidden amazon price with the short and fast html.
# Change shipping fee from string to float, Jiong Wang

    priceinfo = dict()
    
    urlPricing = "http://www.amazon.com/gp/product/du/map-popover-update.html?a="+asin
    root = url2HTML(urlPricing)
    
    if not root:
        priceinfo['prime'] = 0
        priceinfo['availability'] = 0
        return priceinfo
        
    priceTag  = root.xpath('.//td[@id="actualPriceContent"]/span[@id="actualPriceValue"]/b[@class="priceLarge"]')
            
            
    if len(priceTag):
        #Get the price info.
        price = priceTag[0].text
        priceinfo['price'] = float(price[1:].replace(',',''))
                
        #Get the shipping info
        shippingTag = priceTag[0].getparent().getparent().xpath('.//span[@id="actualPriceExtraMessaging"]')
        if len(shippingTag):
            #Determining the shipping option according the extra message wording
            shippingStr = etree.tostring(shippingTag[0], method="text", encoding='windows-1252').lower()
            # print shippingStr
            # if  ('super saver shipping' in shippingStr or 'super saving shipping' in shippingStr or 'standard shipping' in shippingStr):
            if ('free' in shippingStr and 'details' in shippingStr):
                priceinfo['prime'] = 1
                priceinfo['availability'] = 1          
                priceinfo['shippingfee'] = 0

            elif  'free shipping' in shippingStr:
                priceinfo['prime'] = 0
                priceinfo['availability'] = 1          
                priceinfo['shippingfee'] = 0

            elif 'shipping' in shippingStr:
                shippingStrSplit = shippingStr.split('\xa0')
                if len(shippingStrSplit) < 2:
                    print asin+": Cannot understand the shipping info by using '\xa0' to split the actualPriceExtraMessaging string."
                else:
                    priceinfo['prime'] = 0
                    priceinfo['availability'] = 1
                    #print shippingStrSplit
                    shippingStr = shippingStrSplit[1].strip('$')
                    #print shippingStr
                    if '.' in shippingStr:
                        priceinfo['shippingfee'] = float(shippingStr.replace(',', ''))
                    elif shippingStr.count(',') == 1:
                        priceinfo['shippingfee'] = float(shippingStr.replace(',', '.'))
                    else:
                        print 'Error: Cannot find shipping info in getAmznPriceHF(asin)'
                                     
            else:
                priceinfo['availability'] = 1          
        else:
            priceinfo['availability'] = 1    
    else:
        priceinfo['prime'] = 0
        priceinfo['availability'] = 0

    return priceinfo        
#End of getAmznpriceHF(asin)



def getOvstkInfo2(sku):

    if sku.find('|')>0:
        sku7,option=sku.split('|')
    else:
        sku7 = sku
        option=''

    itemdetails = {}
    itemDetails = {'sku7' : sku7}
    itemDetails['produrl'] = 'http://www.overstock.com/'+sku7+'/product.html'
    itemDetails['refreshTime'] = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
    
    itemDetails['title'] = ''
    itemDetails['isbn10'] = ''
    itemDetails['isbn13'] = ''
    itemDetails['upc'] = ''
    itemDetails['brand'] = ''
    itemDetails['mpn'] = ''
    itemDetails['releaseDate'] = '0000-00-00'
    itemDetails['details'] = ''
    itemDetails['price'] = 4999
    itemDetails['shipping'] = 0
    itemDetails['prime'] = 1
    itemDetails['availability' ] = 0
    itemDetails['dimensionL' ] = 0
    itemDetails['dimensionW' ] = 0
    itemDetails['dimensionH' ] = 0
    itemDetails['weight' ] = 0
    itemDetails['maxQty'] = 1
    itemDetails['TPFlag'] = 0 #This flag in prodOverstock is used to tell whether options are available for a product
    itemDetails['imgurl'] = ''
    itemDetails['description'] = ''
    itemDetails['sku8'] = ''
    itemDetails['options']=() #Use tuple to record options. Format is (('id','description','price'),('id2','description2','price2), ...) 
        
        
    
    try:
        htmlStr = url2str(itemDetails['produrl'])
        itemDetails.update(parseOvstkInfo(htmlStr, option))
        
    except Exception, e:
        print sku7 
        print e
        return itemDetails

    return itemDetails    
    
def parseOvstkInfo(htmlStr, option=''):
        
    def getHiddenPrice(sku7):
        hiddenprice = 4999
        url = 'http://www.overstock.com/cart?addpro='+sku7
        string = url2str(url)
        root = etree.HTML(string)
        cartitems = root.xpath('//div[@class="grid-container cart-item "]')
        for cartitem in cartitems:
            if cartitem.xpath('.//a/@href')[0].split('/')[-2]==sku7:
                if cartitem.xpath('.//div[@class="item-total-today"]'):
                    hiddenprice = float(cartitem.xpath('.//div[@class="item-total-today"]')[0].text.split('$')[1])
                elif cartitem.xpath('.//div[@class="item-total-sale"]'):
                    hiddenprice = float(cartitem.xpath('.//div[@class="item-total-sale"]')[0].text.split('$')[1])
        print hiddenprice
        return hiddenprice
        
        
    try:
        itemDetails = {}
        optiontuple = ()
        optionprice = 4999
        itemDetails['title'] = ''
        itemDetails['isbn10'] = ''
        itemDetails['isbn13'] = ''
        itemDetails['upc'] = ''
        itemDetails['brand'] = ''
        itemDetails['mpn'] = ''
        itemDetails['releaseDate'] = '0000-00-00'
        itemDetails['details'] = ''
        itemDetails['price'] = 4999
        itemDetails['shipping'] = 0
        itemDetails['prime'] = 1
        itemDetails['availability' ] = 0
        itemDetails['dimensionL' ] = 0
        itemDetails['dimensionW' ] = 0
        itemDetails['dimensionH' ] = 0
        itemDetails['weight' ] = 0
        itemDetails['maxQty'] = 1
        itemDetails['TPFlag'] = 0 #This flag in prodOverstock is used to tell whether options are available for a product
        itemDetails['imgurl'] = ''
        itemDetails['description'] = ''
        itemDetails['sku8'] = ''
        itemDetails['options']=() #Use tuple to record options. Format is (('id','description','price'),('id2','description2','price2), ...) 
    
        root = etree.HTML(htmlStr)

        #produrl and sku
        linkTags= root.xpath('//link[@rel="canonical"]')
        if linkTags:
            itemDetails['produrl'] = linkTags[0].get('href', '')
            if '/product.html' in itemDetails['produrl']:
                sku7 = itemDetails['produrl'].split('/product.html')[0].split('/')[-1]
            else:
                sku7 = None
            if len(sku7) == 7:
                itemDetails['sku7'] = sku7
            else:
                print 'Error: Cannot find overstock sku7 from item page.'
        else:
            print 'Error: Cannot find product url tag in meta tags.'
        
        
        ##Use meta data to get upc and image url
        metablks = root.xpath('//meta')
        for metablk in metablks:
                if 'og:upc' in etree.tostring(metablk).lower():
                        #print etree.tostring(metablk)
                        itemDetails['upc'] = metablk.get('content', default='')
                if 'og:image' in etree.tostring(metablk).lower():
                        #the imgurl in meta data is thumnail. replace 'T' with 'L' to get the large image
                        itemDetails['imgurl'] = metablk.get('content', default='').replace('T','L')
                        #print itemDetails['imgurl']
                if 'og:url' in etree.tostring(metablk).lower():
                        itemDetails['produrl'] = metablk.get('content', default='')
                        #print itemDetails['produrl']
        sku7 = itemDetails['produrl'].split('/')[-2]

        mainblk = root.xpath('(//div[@id="prod_mainCenter"])[1]')
        if mainblk:
                titleblk = mainblk[0].xpath('(//div[@itemprop="name"]/h1)[1]')
                if titleblk:
                        itemDetails['title'] = titleblk[0].text.replace('\n','').replace('&#174;','').replace('&nbsp;',' ').strip()
                        #print itemDetails['title']
                sku = mainblk[0].xpath('(//span[@id="itmNum"])[1]')
                if sku:
                        skuSplit = sku[0].text.split('Item #:')
                        if len(skuSplit)>1:
                                itemDetails['sku8'] = skuSplit[1].strip()
                                #print itemDetails['sku8']

                price = mainblk[0].xpath('(//span[@itemprop="price"])[1]')
                hiddenprice = mainblk[0].xpath('(//span[@class="main-price-red-strike"])[1]')
                if hiddenprice:
                        print "price hidden"
                        price = getHiddenPrice(sku7)
                else:
                        if price:
                            itemDetails['price'] = float(price[0].text.strip().strip('$'))
                if itemDetails['price']<50: itemDetails['shipping']=2.95
                #print itemDetails['price']     
                #print itemDetails['shipping']

                availability = mainblk[0].xpath('(//input[@id="addCartMain_addCartButton"])[1]')
                if availability:
                        itemDetails['availability'] = 1
                        #print itemDetails['availability']

                quantity = mainblk[0].xpath('//div[@id="addCartMain_quantity"]/select/option[last()]')
                if quantity:
                        itemDetails['maxQty'] = int(quantity[0].text.strip())
                        #print itemDetails['maxQty']
                options = mainblk[0].xpath('//div[@id="options"]/div[@id="addCartWrap_productOptions"]')
                if options:
                        options2 = options[0].xpath('.//option')
                        print "%d options available" %(len(options2)-1)
                        optionflag = 0 #this flag is used to check wether the option we want is available or not
                        if len(options2)>=2: itemDetails['TPFlag']=1
                        for option2 in options2:
                            optionid = option2.attrib['value']
                            print optionid, len(optionid)
                            if len(optionid) >= 7: 
                                optiontext = option2.text.split('$')[0].strip().strip('-').strip()
                                optionprice = option2.text.split('$')[1].strip()
                                optiontuple += ((optionid,optiontext,optionprice),)
                            #if option is available or there is no alternative option when item was listed
                            if optionid == option or option=='':
                                optionflag = 1
                                itemDetails['price']=float(optionprice)
                                #add option text to title
                                itemDetails['title'] = optiontext+' '+itemDetails['title']
                        #if option we want is not available
                        if optionflag == 0:
                            itemDetails['price']=4999
                            itemDetails['availability']=0
                        itemDetails['options'] = optiontuple 

        ISBN = root.xpath('(//div[@id="description-text"]//dl[dt="ISBN:"]/dd)[1]')
        if ISBN:
                itemDetails['isbn13'] = ISBN[0].text
        else:
                keywords = root.xpath('(//meta[@name="keywords"])[1]')
                if keywords:
                        content = keywords[0].get('content')
                        contentSplit = content.split(',')
                        for contentText in contentSplit:
                                textSrtip = contentText.strip()
                                if textSrtip.isdigit() and len(textSrtip)==12:
                                        itemDetails['upc'] = textSrtip
                                        break

        #prodblk = root.xpath('(//div[@id="prod_tabs"])[1]')
        prodblk = root.xpath('.//div[@id="prod_tabs"]')
        #print prodblk[0]
        if prodblk:
                ulTag = prodblk[0].xpath('.//ul[@id="details_descFull"]')[0]
                itemDetails['details'] = etree.tostring(ulTag,method='text', encoding='utf-8')
                dlTag = prodblk[0].xpath('.//div[@id="details_descMisc"]//dl')[0]
                itemDetails['details'] += '<br>'+etree.tostring(dlTag,method='text', encoding='utf-8')
                itemDetails['details'] = removenewline(itemDetails['details'])
                #print itemDetails['details']
                if prodblk[0].xpath('.//div[@id="details_descMisc"]//dl[dt="Model No:"]'):
                    model = prodblk[0].xpath('.//div[@id="details_descMisc"]//dl[dt="Model No:"]/dd[last()]')[0].text
                    #print model
                    itemDetails['mpn']=model

    except Exception, e:
        print itemDetails
        print 'option: ' + option
        print e
        return itemDetails

    return itemDetails
#End of parseOvstkInfo(sku)

def getOvstkInfo(sku):

    def getHiddenPrice(sku7):

        hiddenprice = 4999
        url = 'http://www.overstock.com/cart?addpro='+sku7
        string = url2str(url)
        root = etree.HTML(string)
        cartitems = root.xpath('//div[@class="grid-container cart-item "]')
        for cartitem in cartitems:
            if cartitem.xpath('.//a/@href')[0].split('/')[-2]==sku7:
                if cartitem.xpath('.//div[@class="item-total-today"]'):
                    hiddenprice = float(cartitem.xpath('.//div[@class="item-total-today"]')[0].text.split('$')[1])
                elif cartitem.xpath('.//div[@class="item-total-sale"]'):
                    hiddenprice = float(cartitem.xpath('.//div[@class="item-total-sale"]')[0].text.split('$')[1])
        print hiddenprice
        return hiddenprice
    if sku.find('|')>0:
        sku7,option=sku.split('|')
    else:
        sku7 = sku
        option=''
    itemdetails = {}
    optiontuple = ()
    optionprice = 4999
    itemDetails = {'sku7' : sku7}
    itemDetails['title'] = ''
    itemDetails['isbn10'] = ''
    itemDetails['isbn13'] = ''
    itemDetails['upc'] = ''
    itemDetails['brand'] = ''
    itemDetails['mpn'] = ''
    itemDetails['releaseDate'] = '0000-00-00'
    itemDetails['details'] = ''
    itemDetails['price'] = 4999
    itemDetails['shipping'] = 0
    itemDetails['prime'] = 1
    itemDetails['availability' ] = 0
    itemDetails['dimensionL' ] = 0
    itemDetails['dimensionW' ] = 0
    itemDetails['dimensionH' ] = 0
    itemDetails['weight' ] = 0
    itemDetails['maxQty'] = 1
    itemDetails['TPFlag'] = 0 #This flag in prodOverstock is used to tell whether options are available for a product
    itemDetails['refreshTime'] = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
    itemDetails['imgurl'] = ''
    itemDetails['description'] = ''
    itemDetails['produrl'] = 'http://www.overstock.com/'+sku7+'/product.html'
    itemDetails['sku8'] = ''
    itemDetails['options']=() #Use tuple to record options. Format is (('id','description','price'),('id2','description2','price2), ...) 
    try:
        root = url2HTML(itemDetails['produrl'])
        ##Use meta data to get upc and image url
        metablks = root.xpath('//meta')
        for metablk in metablks:
                if 'og:upc' in etree.tostring(metablk).lower():
                        #print etree.tostring(metablk)
                        itemDetails['upc'] = metablk.get('content', default='')
                if 'og:image' in etree.tostring(metablk).lower():
                        #the imgurl in meta data is thumnail. replace 'T' with 'L' to get the large image
                        itemDetails['imgurl'] = metablk.get('content', default='').replace('T','L')
                        #print itemDetails['imgurl']
                if 'og:url' in etree.tostring(metablk).lower():
                        itemDetails['produrl'] = metablk.get('content', default='')
                        #print itemDetails['produrl']
        sku7 = itemDetails['produrl'].split('/')[-2]

        mainblk = root.xpath('(//div[@id="prod_mainCenter"])[1]')
        if mainblk:
                titleblk = mainblk[0].xpath('(//div[@itemprop="name"]/h1)[1]')
                if titleblk:
                        itemDetails['title'] = titleblk[0].text.replace('\n','').replace('&#174;','').replace('&nbsp;',' ').strip()
                        #print itemDetails['title']
                sku = mainblk[0].xpath('(//span[@id="itmNum"])[1]')
                if sku:
                        skuSplit = sku[0].text.split('Item #:')
                        if len(skuSplit)>1:
                                itemDetails['sku8'] = skuSplit[1].strip()
                                #print itemDetails['sku8']

                price = mainblk[0].xpath('(//span[@itemprop="price"])[1]')
                hiddenprice = mainblk[0].xpath('(//span[@class="main-price-red-strike"])[1]')
                if hiddenprice:
                        print "price hidden"
                        price = getHiddenPrice(sku7)
                        if price < 2000:
                            itemDetails['price'] = price
                else:
                        if price:
                            itemDetails['price'] = float(price[0].text.strip().strip('$'))
                if itemDetails['price']<50: itemDetails['shipping']=2.95
                #print itemDetails['price']     
                #print itemDetails['shipping']

                availability = mainblk[0].xpath('(//input[@id="addCartMain_addCartButton"])[1]')
                if availability:
                        itemDetails['availability'] = 1
                        #print itemDetails['availability']

                quantity = mainblk[0].xpath('//div[@id="addCartMain_quantity"]/select/option[last()]')
                if quantity:
                        itemDetails['maxQty'] = int(quantity[0].text.strip())
                        #print itemDetails['maxQty']
                options = mainblk[0].xpath('//div[@id="options"]/div[@id="addCartWrap_productOptions"]')
                if options:
                        options2 = options[0].xpath('.//option')
                        print "%d options available" %(len(options2)-1)
                        optionflag = 0 #this flag is used to check wether the option we want is available or not
                        if len(options2)>=2: itemDetails['TPFlag']=1
                        for option2 in options2:
                            optionid = option2.attrib['value']
                            print optionid, len(optionid)
                            if len(optionid) >= 7: 
                                optiontext = option2.text.split('$')[0].strip().strip('-').strip()
                                optionprice = option2.text.split('$')[1].strip()
                                optiontuple += ((optionid,optiontext,optionprice),)
                            #if option is available or there is no alternative option when item was listed
                            if optionid == option or option=='':
                                optionflag = 1
                                itemDetails['price']=float(optionprice)
                                #add option text to title
                                itemDetails['title'] = optiontext+' '+itemDetails['title']
                        #if option we want is not available
                        if optionflag == 0:
                            itemDetails['price']=4999
                            itemDetails['availability']=0
                        itemDetails['options'] = optiontuple 

        ISBN = root.xpath('(//div[@id="description-text"]//dl[dt="ISBN:"]/dd)[1]')
        if ISBN:
                itemDetails['isbn13'] = ISBN[0].text
        else:
                keywords = root.xpath('(//meta[@name="keywords"])[1]')
                if keywords:
                        content = keywords[0].get('content')
                        contentSplit = content.split(',')
                        for contentText in contentSplit:
                                textSrtip = contentText.strip()
                                if textSrtip.isdigit() and len(textSrtip)==12:
                                        itemDetails['upc'] = textSrtip
                                        break

        #prodblk = root.xpath('(//div[@id="prod_tabs"])[1]')
        prodblk = root.xpath('.//div[@id="prod_tabs"]')
        #print prodblk[0]
        if prodblk:
                ulTag = prodblk[0].xpath('.//ul[@id="details_descFull"]')[0]
                itemDetails['details'] = etree.tostring(ulTag,method='text', encoding='utf-8')
                dlTag = prodblk[0].xpath('.//div[@id="details_descMisc"]//dl')[0]
                itemDetails['details'] += '<br>'+etree.tostring(dlTag,method='text', encoding='utf-8')
                itemDetails['details'] = removenewline(itemDetails['details'])
                #print itemDetails['details']
                if prodblk[0].xpath('.//div[@id="details_descMisc"]//dl[dt="Model No:"]'):
                    model = prodblk[0].xpath('.//div[@id="details_descMisc"]//dl[dt="Model No:"]/dd[last()]')[0].text
                    #print model
                    itemDetails['mpn']=model

    except Exception, e:
        print sku7 
        print e
        return itemDetails

    return itemDetails
#End of getOvstkInfo(sku)





def getEpidInfo(EPID):
    #Note: this function returns the following information from an EPID:
    #prices of new items, Brand, MPN, UPC. MPN and UPC can have multiple values, delimited by comma
    #6-8-2013, also return epid_pic flag. '1' means there is a catalog picture, '0' means no catalog picture for this EPID
    #No ISBN for now, can be expanded later

    #Local functions for price check
    def getPrice1(pblks):
        price = []
        shipping = None
        try:
            for pblk in pblks.findAll('li'):
                itemprice = float(pblk.find('span',{"class":"g-b tb3-prc tb3-fr"}).find(text=True).split('$')[1].replace(',',''))
                if pblk.find('span',{"class":"tb3-fr g-nav tb3-shp"}):
                    shipping = pblk.find('span',{"class":"tb3-fr g-nav tb3-shp"}).find(text=True)
                if shipping is None:
                    price += [itemprice+8]
                elif shipping.count('Free'):
                    price += [itemprice]
                elif shipping.count('$'):
                    price += [itemprice+float(shipping.split('$')[1])]
                else:
                    price += [itemprice+8]
        except Exception,e:
            print e
        return price

    def getPrice2(pblks):
        price = []
        shipping = None
        try:
            for pblk in pblks.findAll('li'):
                itemprice = float(pblk.find('strong',{"class":"pricespan"}).find(text=True).split('$')[1].replace(',',''))
                if pblk.find('span',{"class":"ship"}):
                    shipping = pblk.find('span',{"class":"ship"}).find(text=True)
                bin = pblk.find('span',{"class":"itemCdnSpan"}).find(text=True)
                if bin.count('bids'):
                    continue
                if shipping is None:
                    price += [itemprice+8]
                elif shipping.count('Free'):
                    price += [itemprice]
                elif shipping.count('$'):
                    price += [itemprice+float(shipping.split('$')[1])]
                else:
                    price += [itemprice+8]
        except Exception,e:
            print e
        return price
    #end of local functions

    dict = {'EPID':EPID}
    #produrl = 'http://www.ebay.com/ctg/'+EPID+'?LH_ItemCondition=1000'
    #req_7_bin_qqq_94538 is for buy it now listings only
    produrl = 'http://www.ebay.com/ctg/'+EPID+'?LH_ItemCondition=1000#req_7_bin_qqq_94538'
    soup = url2HTML(produrl,'soup')

    try:
        pblks1 = soup.find('td',{"class":"tb3-b-td"})
        pblks2 = soup.find('ul',{"class":"ls sml"})
        pblks3 = soup.find('ul',{"class":"ls"})
        if pblks1:
            print "pblk1"
            prices=getPrice1(pblks1)
        elif pblks2:
            print "pblk2"
            prices=getPrice2(pblks2)
        elif pblks3:
            print "pblk3"
            prices=getPrice2(pblks3)
        else:
            print "no pblks found"
            prices = [0]
        dict['minprice']= min(prices)
        dict['maxprice'] = max(prices)
        dict['records'] = len(prices)
        dict['avgprice'] = sum(prices)/dict['records']
    except Exception,e:
        print e
        dict['minprice'] = 0
        dict['maxprice'] = 0
        dict['records'] = 0
        dict['avgprice'] = 0
    #print soup.prettify()
    try:
        dict['Brand'] = soup.find(text="Brand").findNext('td').find(text=True)
    except:
        dict['Brand'] = 'NA'
    try:
        dict['MPN'] = soup.find(text="MPN").findNext('td').find(text=True)
    except:
        dict['MPN'] = 'NA'
    try:
        dict['UPC'] = soup.find(text="UPC").findNext('td').find(text=True)
    except:
        dict['UPC'] = 'NA'
    try:
        leftnav = soup.find('div',{"id":"v4-6"})
        imgurl = leftnav.find('img')['src']
        if imgurl.find('Placeholder')>0:
            dict['EPID_PIC'] = '0'
        else:
            dict['EPID_PIC'] = '1'
            dict['imgurl']=imgurl
    except:
        dict['EPID_PIC'] = '0'

    return dict
#end of getEpidInfo(EPID)



def updateDB(listAsins, listItems, cur, strTblName):
    
    try: 
        nAffected = 0
        i = 0
        for i in range(0, len(listItems)):
            iLen = len(listItems[i])
            #Fill the table name and keys into the execusion command.
            strCurExec = ('UPDATE %s SET' + ' %s =,'*iLen) % ((strTblName, )+tuple(listItems[i].keys()))
            #Fill the values into the execusion command.                                                    
            strCurExec = strCurExec[:-1].replace('=', '= %s')  
            #Insert condition on asin.
            strCurExec += ' where asin= %s'     
            #print strCurExec
                    
            nAffected += cur.execute(strCurExec, listItems[i].values()+[listAsins[i]])
    #print strCurExec
    
    except Exception, e: 
        print listAsins[i]
        print e
        return nAffected
    
    return nAffected

#End of updateDB()


def insertDB(listItems, cur, strDbName, dupHandling=''):
    #listItems is a list of dictionary e.g. [{'asin':'B123','upc':'1234'},{'asin':'B456','upc':'4567'}]
    #cur is db cursor; strDbName is the table name e.g. 'prodAmazon'
    #dupHandling options: ignore, update and others.
    nAffected = 0
    if not len(listItems):
        return nAffected
    
    try:
        if type(listItems[0]) == dict: #Insert with keys.
            for itemDetails in listItems:
                iLen = len(itemDetails)
                strCurExec = ('INSERT INTO %s (' + ' %s,'*iLen) % ((strDbName,) + tuple(itemDetails.keys()))
                strCurExec = strCurExec[:-1] + (') VALUES(' + ' %s,'*iLen)
                strCurExec = strCurExec[:-1] + ')'
                
                if dupHandling.lower() == 'ignore':
                    strCurExec = strCurExec.replace('INSERT', 'INSERT IGNORE')                
                    nAffected += cur.execute(strCurExec, itemDetails.values())
                elif dupHandling.lower() == 'update':
                    strCurExec += ' ON DUPLICATE KEY UPDATE' + (' %s =,'*iLen % tuple(itemDetails.keys()))[:-1].replace('=', '= %s')
                    #Debug##########
                    #print strCurExec
                    #print itemDetails.values()+itemDetails.values()
                    ################
                    nAffected += cur.execute(strCurExec, itemDetails.values()+itemDetails.values())
                else:
                    nAffected += cur.execute(strCurExec, itemDetails.values())                    
                # print strCurExec 
                # print itemDetails.values() 

        elif (type(listItems[0]) == list) or (type(listItems[0]) == tuple): #Insert without keys.
            for itemDetails in listItems:
                iLen = len(itemDetails)
                strCurExec = 'INSERT INTO %s' % strDbName 
                strCurExec = (strCurExec + ' VALUES(' + ' %s,'*iLen)[:-1] + ')'
                
                if dupHandling.lower() == 'ignore':
                    strCurExec = strCurExec.replace('INSERT', 'INSERT IGNORE')
                elif dupHandling.lower() == 'update':
                    print 'Error on using insertDB(... dupHandling = "update"). You have to specify column names you want to update.'
                    sys.exit(1)
                
                nAffected += cur.execute(strCurExec, itemDetails)
    
    except Exception, e: 
        print 'Exception in function insertDB'
        print 'itemDetails: '
        print itemDetails
        print e
    
    return nAffected

#End of insertDB() 

def amznAPI2str(api_params):
    '''
    retStr, url = amznAPI2str(api_params)
    Retrieve the xml string using amazon api.
    
    --Input:
    api_params: parameter be be passed to amazon api.
      e.g. url_params = dict(Operation='ItemLookup', ItemId='B004J3Y9U6', ResponseGroup='Large')
      
    --Output:
    retStr: Retrieved xml string.
    url: API xml url
    '''
    
    try:
        import base64, hashlib, hmac, time
        from urllib import urlencode, quote_plus

        AWS_SECRET_ACCESS_KEY = 'X0VeDW25cU5VSIDPrQa+ZGKf8sXsgskS3hpNLLdS'  
        base_url = "http://ecs.amazonaws.com/onca/xml"

        #api_params examples:
        #api_params = dict(Operation='ItemLookup', ItemId='B004J3Y9U6', ResponseGroup='Large')
        #api_params = dict(Operation='BrowseNodeLookup', BrowseNodeId=172526, ResponseGroup='TopSellers', ItemPage=2)
        #api_params = dict(Operation='ItemSearch', BrowseNode=172526, SearchIndex='Electronics', ResponseGroup='ItemAttributes', ItemPage=1, Sort='salesrank')
        #api_params = dict(Operation='BrowseNodeLookup', BrowseNodeId=226684, ResponseGroup='BrowseNodeInfo')

        url_params = api_params.copy()
        url_params['Timestamp'] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        url_params['AWSAccessKeyId'] = 'AKIAJ73HNVFDRRGOASBA'
        url_params['Service'] = 'AWSECommerceService'
        url_params['AssociateTag'] = 'utsav'


        # Sort the URL parameters by key
        keys = url_params.keys()
        keys.sort()

        # Get the values in the same order of the sorted keys
        values = map(url_params.get, keys)

        # Reconstruct the URL parameters and encode them
        url_string = urlencode(zip(keys,values))

        #Construct the string to sign
        string_to_sign = "GET\necs.amazonaws.com\n/onca/xml\n%s" % url_string

        # Sign the request
        signature = hmac.new(
            key=AWS_SECRET_ACCESS_KEY,
            msg=string_to_sign,
            digestmod=hashlib.sha256).digest()

        # Base64 encode the signature
        signature = base64.encodestring(signature).strip()

        # Make the signature URL safe
        urlencoded_signature = quote_plus(signature)
        url_string += "&Signature=%s" % urlencoded_signature

        url = "%s?%s" % (base_url, url_string)
        retStr = url2str(url)
        
        return retStr, url
        
    except Exception, e:
        print 'Exception in amznAPI2str function.'
        print e
        return ''
    
#End of amznAPI2str(url_params)

def asin2idmapping(iddict,cur):
    #iddict is a dictionary with asin (required), UPC (optional) and ISBN10 (optional), Brand (optional), MPN (optional), catnum(optional)
    #iddict can also be a list or tuple of dictionary
    #If asin is not in idmapping, the function inserts record to idmapping table, the function also checks duplicate and generate customlabel
    #If asin is in idmapping already, the function will update UPC/ISBN10/Brand/MPN is they are null
    #iddict={'asin':'B00002N8CX','upc':'023169108028','brand':'xxx','mpn':'xxx','isbn10':'1234567890'}
    #catnum is required when insert record to idmapping

    #Local function mapping()
    def mapping(dict):
        asin = ''
        upc = ''
        isbn10 = ''
        isbn13 = ''
        brand = ''
        mpn = ''
        catnum = ''
        counter = 0
        if 'asin' not in dict:
            print "Required field asin is not in dictionary. Pass"
            return(0)
        elif 'catnum' not in dict:
            print "Required field is not in dictionary. Pass"
            return(0)
        else:
            #asin and catnum are in dictionary
            asin = dict['asin']
            catnum = dict['catnum']
            if 'upc' in dict: upc = dict['upc']
            if 'isbn10' in dict: isbn10 = dict['isbn10']
            if 'isbn13' in dict: isbn13 = dict['isbn13']
            if 'brand' in dict: brand = dict['brand']
            if 'mpn' in dict: mpn = dict['mpn']
            #check if the item is a book (asin = isbn10)
            if (isbn10<>'' and isbn10<>None) or (isbn13<>'' and isbn13<>None):
                #if the item is a book
                return insertDB([{'asin':asin,'catnum':catnum,'isbn10':isbn10,'isbn13':isbn13}],cur,'idmapping','ignore')

            else:
                #if the item is not a book
                print "item is not a book"
                #check if asin in idmapping
                #counter=cur.execute("select asin,upc,brand,mpn,catnum,customlabel from idmapping where asin=%s",(asin,))
                #check if upc in dict
                if upc <> '' and upc <> None:
                    #upc in dict, insert dict to idmapping with update option
                    print "insert upc to idmapping"
                    return cur.execute("""insert into idmapping (asin,upc,catnum,brand,mpn) values (%s,%s,%s,%s,%s)
                                          on duplicate key update asin=%s""",(asin,upc,catnum,brand,mpn,asin))
                else:
                    #no upc nor isbn in dict
                    if counter > 0:
                        #asin in idmapping already
                        #update brand mpn to idmapping
                        if brand <> '' and brand <> None and mpn <> '' and mpn <> None:
                            return cur.execute("""update idmapping set catnum=%s,brand=%s,mpn=%s where asin = %s""",(catnum,brand,mpn,asin))
                    else:
                        #asin not in idmapping
                            return insertDB([{'asin':asin,'catnum':catnum,'brand':brand,'mpn':mpn}],cur,'idmapping','ignore') 
        return 0
    #end of local function mapping()
    i = 0
    if type(iddict) == list or type(iddict) == tuple:
        for item in iddict:
            print item
            i+=mapping(item)
        return(i)
    elif type(iddict) == dict:
        i+=mapping(iddict)
        return(i)
    else:
        print "Wrong input parameter,please use list, tuple or dictionary"
        return(0)
#End of asin2idmapping()


def ebayListingInfo(listID):
    '''
    ebayListingInfo(listID)
    Get details of an eBay listing
    
    --Input:
    listID: eBay listing id in string
    
    --Output:
    itemDetals: Listing item details in dict.
    '''
    
    itemDetails = {}
    try:
    #item number
        listURL = 'http://www.ebay.com/itm/?item=%s' % listID
        urlStr = url2str(listURL)
        if urlStr:
            itemDetails = parseEbayListingPg(urlStr, listURL)
        else:
            print 'Warning in function ebayListingInfo(%s)' % listID
            print 'Blank string returned from url: '+listURL
        
        #sales history
        if itemDetails.get('qtySold', 0) > 0:
            listHistURL = 'http://offer.ebay.com/ws/eBayISAPI.dll?ViewBidsLogin&item=%s' % listID
            urlStr = url2str(listHistURL)
            if urlStr:
                itemDetails.update(parseEbayListHist(urlStr, listHistURL))
            else:
                print 'Warning in function ebayListingInfo(%s)' % listID
                print 'Blank string returned from url: '+listHistURL
                
            
        return itemDetails
    
    
    except Exception, e:
        print 'Exception in ebayListingInfo function.'
        print 'ListID: '+listID
        print e
        return itemDetails
        
#End of ebayListingInfo('listID')


def parseEbayListingPg(urlStr, url = ''):
    '''
    parseEbayListingPg(urlStr, url = '')
    Get details of an eBay listing page string
    
    --Input:
    urlStr: Listing page html string.
    url = '': Url.
    
    --Output:
    itemDetals: Listing item details in dict.
        keys (if available) in itemDetails: title, price, isbn10, isbn13, upc, epid, catNum, catName, asin (if it is a Happitail listing), availQty, qtySold, imgLink,condition,shipToCountry(this is a list)
    
    --Example:
    operation3.parseEbayListingPg(stra)
    
    {'asin': 'B000OL22T2',
     'availQty': 2,
     'catName': 'Home Speakers & Subwoofers',
     'catNum': '14990',
     'epid': '69565624',
     'price': 221.13,
     'qtySold': 2,
     'title': 'Sony SA-W3000/Z Subwoofer (Each, Black) Brand New!',
     'upc': '027242706422'}
     
     New optional fields:
     brand:
     mpn:
     manufacturer:
     model:
     (manufacturer and model are useful for Newegg ebay items)     
    
    
    '''
    
    itemDetails = {}
    
    try:
        if not urlStr:
            return itemDetails
        
        # f = open('ebayTest.html', 'w')
        # f.write(urlStr)
        # f.close()
        
        root = etree.HTML(urlStr)
#         print len(root)
        if not len(root):
            return itemDetails
        
        #title
        itemDetails['title'] = ''
        titleList = root.xpath("//meta[@property='og:title']/@content")
        if titleList: itemDetails['title'] = titleList[0].encode('latin1','ignore')
        
        #price 
        priceTags = root.xpath('//span[@id="prcIsum"]')
        if priceTags:
            if priceTags[0].text.find('$')>=0:
                itemDetails['price'] = float(priceTags[0].text.replace(',', '').split('$')[1].split()[0])
            else:
                #price is not USD denominated
                print "i am here"
                priceTags2 = root.xpath('//div[@id="prcIsumConv"]/span')
                if priceTags2:
                    itemDetails['price'] = float(priceTags2[0].text.replace(',', '').split('$')[1].split()[0])

        else: itemDetails['price'] = 0
        
        
        #isbn-10
        isbn10Tags = root.xpath('//td[contains(text(), "ISBN-10:")]/following-sibling::td[1]')
        if isbn10Tags: 
            isbn10Texts = isbn10Tags[0].xpath('.//text()')
            if isbn10Texts:
                itemDetails['isbn10'] = isbn10Texts[-1].strip()
            else: 
                itemDetails['isbn10'] = isbn10Tags[0].text.split()[0]
        
        #isbn-13
        isbn13Tags = root.xpath('//td[contains(text(), "ISBN-13:")]/following-sibling::td[1]')
        if isbn13Tags: 
            isbn13Texts = isbn13Tags[0].xpath('.//text()')
            if isbn13Texts:
                itemDetails['isbn13'] = isbn13Texts[-1].strip()
            else: 
                itemDetails['isbn13'] = isbn13Tags[0].text.split()[0]	
            
        # 		#upc, choose the first upc not beginning with '0'
        # 		upcTags = root.xpath('//div[@class="prodDetailSec"]//td[font="UPC"]/following-sibling::td/font[1]')
        # 		if upcTags:
        # 			upcSplit = upcTags[0].text.split(',')
        # 			for upc in upcSplit:
        # 				upc = upc.strip()
        # 				if not upc[0]=='0':
        # 					break
        # 			itemDetails['upc'] = upc
        
        
        #upc
        upcTags = root.xpath('//td[contains(text(), "UPC:")]/following-sibling::td[1]')
        #print upcTags
        if upcTags:
            upcTexts = upcTags[0].xpath('.//text()')
            if upcTexts:
                itemDetails['upc'] = upcTexts[-1].strip().zfill(12)
            else: 
                itemDetails['upc'] = upcTags[0].text.split()[0].zfill(12)
        
        #brand
        brandTags = root.xpath('//td[contains(text(), "Brand:")]/following-sibling::td[1]')
        #print brandTags
        if brandTags:
            brandTexts = brandTags[0].xpath('.//text()')
            if brandTexts:
                itemDetails['brand'] = brandTexts[-1].strip()
            else: 
                itemDetails['brand'] = brandTags[0].text.strip()
        
        #mpn
        mpnTags = root.xpath('//td[contains(text(), "MPN:")]/following-sibling::td[1]')
        #print upcTags
        if mpnTags:
            mpnTexts = mpnTags[0].xpath('.//text()')
            if mpnTexts:
                itemDetails['mpn'] = mpnTexts[-1].strip()
            else: 
                itemDetails['mpn'] = mpnTags[0].text.strip()  
                      
        #manufacturer
        manTags = root.xpath('//td[contains(text(), "Manufacturer:")]/following-sibling::td[1]')
        #print manTags
        if manTags:
            manTexts = manTags[0].xpath('.//text()')
            if manTexts:
                itemDetails['manufacturer'] = manTexts[-1].strip()
            else: 
                itemDetails['manufacturer'] = manTags[0].text.strip()
                        
        #model
        modelTags = root.xpath('//td[contains(text(), "Model:")]/following-sibling::td[1]')
        #print upcTags
        if modelTags:
            modelTexts = modelTags[0].xpath('.//text()')
            if modelTexts:
                itemDetails['model'] = modelTexts[-1].strip()
            else: 
                itemDetails['model'] = modelTags[0].text.strip()
        
        
        #epid, catName and catNum
        epidTags = root.xpath('//li[contains(text(), "Listed as")][1]/a[1]')
        if epidTags:
            itemDetails['epid'] = epidTags[0].get('href', '').split('/')[-1].split('?')[0]
            catTags = epidTags[0].getparent().getparent().xpath('./following-sibling::td/table//li[last()]/a[1]')
            if catTags:
                itemDetails['catName'] = catTags[0].text
                catNumSplit = catTags[0].get('href', '').split('/')
                if len(catNumSplit)>1:
                    itemDetails['catNum'] = catNumSplit[-2]
            topCatTags = epidTags[0].getparent().getparent().xpath('./following-sibling::td/table//li[1]/a[1]')
            if topCatTags:
                itemDetails['topCatName'] = topCatTags[0].text
                topCatNumSplit = topCatTags[0].get('href', '').split('/')
                if len(topCatNumSplit)>1:
                    itemDetails['topCatNum'] = topCatNumSplit[-2]
        else:
            catTags0 = root.xpath('//li[contains(text(), "Listed in category:")][1]')
            if catTags0:
                catTags = catTags0[0].getparent().xpath('./following-sibling::td/table//li[last()]/a[1]')
                if catTags:
                    itemDetails['catName'] = catTags[0].text
                    catNumSplit = catTags[0].get('href', '').split('/')
                    if len(catNumSplit)>1:
                        itemDetails['catNum'] = catNumSplit[-2]
                topCatTags = catTags0[0].getparent().xpath('./following-sibling::td/table//li[1]/a[1]')
                if topCatTags:
                    itemDetails['topCatName'] = topCatTags[0].text
                    topCatNumSplit = topCatTags[0].get('href', '').split('/')
                    if len(topCatNumSplit)>1:
                        itemDetails['topCatNum'] = topCatNumSplit[-2]
        # 		print 'catName: ' + itemDetails.get('catName', '')
        # 		print 'catNum: ' + itemDetails.get('catNum', '')
        # 		print 'epid: '+itemDetails.get('epid', 'not found')
        
        
        #asin
        skuList = root.xpath('//text()[contains(., "|SKU|:")][1]')
        if skuList:
            website, sku = skudec(skuList[0].split('|SKU|:')[1].split()[0])
            itemDetails['source'] = website
            itemDetails['asin'] = sku
        else:
            skuList = root.xpath('//text()[contains(., "SKU:")][1]')
            if skuList:
                if '|' in skuList[0]:
                    website, sku = skudec(skuList[0].split('SKU:')[1].split()[0])
                    itemDetails['source']= website 
                    itemDetails['asin'] = sku
        # 	    print 'asin: '+itemDetails.get('asin', '')
        
        #available quantity
        qtyLabelTags = root.xpath('(//label[@for="qtyTextBox"])[1]')
        if qtyLabelTags:
            availTags = qtyLabelTags[0].xpath('(../../..//*[contains(text(), "available")])[1]')
            if availTags:
                #print '"%s"' % availTags[0].text.split('available')[0].split()[-1]
                try:
                    itemDetails['availQty'] = int(availTags[0].text.split('available')[0].split()[-1])
                except:
                    pass
                
            soldTags = qtyLabelTags[0].xpath('(../../..//*[contains(text(), "sold")])[1]')
            if soldTags:
                #print '"%s"' % soldTags[0].text.split('sold')[0].split()[-1]
                #print soldTags[0].get('href', '')
                try:
                    itemDetails['qtySold'] = int(soldTags[0].text.split('sold')[0].split()[-1])
                except:
                    pass

              
        #Image link
        imgTags = root.xpath('//img[@class="img img300"]')
        if imgTags:
            imgLink = imgTags[0].get('src', '')
            #print imgLink
            imgLinkSplit = imgLink.split('.')
            #Get img 500 link from img 300 link, i.e. replace '_35.jpg' to '_12.jpg'
            if len(imgLinkSplit)>1:
                if imgLinkSplit[-2][-2:] == '35':
                    imgLink = '.'.join(imgLinkSplit[:-1])[:-2]+'12.'+imgLinkSplit[-1]
            
            itemDetails['imgurl'] = imgLink
            
       
        #item condition
        conditionTags = root.xpath('//div[contains(text(), "Item condition:")][1]')
        if conditionTags:
            conditionTag = conditionTags[0].xpath('./following-sibling::*')
            if conditionTag:
                condition = conditionTag[0].text
                itemDetails['condition'] = condition
        else:
            itemDetails['condition'] = 'Unknown'
       
        #Ship to countries
        shiptoTags = root.xpath('//div[contains(text(), "Shipping to:")][1]')
        if shiptoTags:
            shipToCountry = shiptoTags[0].text.split(':')[1].split(',')
            liststrip(shipToCountry)
            itemDetails['shipToCountry'] = shipToCountry
        else:
            itemDetails['shipToCountry'] = ['United States']
        return itemDetails
    
    except Exception, e:
        print 'Exception in ebayListingInfo function.'
        print 'url: '+ url
        print e
        return itemDetails
    
#End of parseEbayListingPg(urlStr, url = '')
    
    
def parseEbayListHist(urlStr, url = ''):
    '''
    parseEbayListHist(urlStr, url = '')
    Get last sold item info from ebay listing history page
    
    --Input:
    urlStr: Listing page html string.
    url = '': Url.
    
    --Output:
    itemDetals: Listing item details in dict.
        keys (if available) in itemDetails: lastPrice, lastQty, lastDate
    '''
    itemDetails = {}
    
    try:
        if not urlStr:
            return itemDetails
            
        
        root = etree.HTML(urlStr)
#         print len(root)

        if not len(root):
            return itemDetails
        
        #Last sold, quantity, and purchase date
        priceTags = root.xpath('(//div[@class="BHbidSecBorderGrey"]//td[@class="contentValueFont"])[position()<4]')
        if len(priceTags)>0:
            try:
                #The '$' sign is hard coded, subject to change if we want to scrape a international site.
                itemDetails['lastPrice'] = float(priceTags[0].text.replace(',', '').split('$')[1].split()[0])
                
            except Exception,e:
                print 'Exception in parseEbayListHist function.'
                print 'Cannot parse lastPrice information.'
                print 'url: '+ url
                print e
                pass
        if len(priceTags)>1:
            itemDetails['lastQty'] = int(priceTags[1].text)
        if len(priceTags)>2:
            try:
                lastDate = time.strptime(' '.join(priceTags[2].text.split()[:-1]), '%b-%d-%y %H:%M:%S')
                itemDetails['lastDate'] = time.strftime('%Y-%m-%d %H:%M:%S')
            except Exception, e:
                print 'Exception in parseEbayListHist function.'
                print 'Cannot parse lastDate information.'
                print 'url: '+ url
                print e
                pass
        
        return itemDetails
    
    except Exception, e:
        print 'Exception in parseEbayListHist function.'
        print 'url: '+ url
        print e
        return itemDetails

#End of def parseEbayListHist(urlStr, url = '')

prefixEnc = {'amazon': 'A!', 'overstock': 'O!'} 
prefixDec = {'A': 'amazon', 'O': 'overstock'}

def skuenc(id, website='amazon'):
	prefix = prefixEnc.get(website, '')
	sku = prefix
	id = str(id).upper()
	L = 36 # The size of the character set, 0-10 plus A-Z
	for i in range(0, len(id)): #Encoding part, the same algorithm as decoding
		num = ord(id[i])-48-(id[i]>='A')*7 #Convert character to number 0-35
		num =  (2*(2**i % L) - num) % L #Encoding: mirror the number to (2**i % L)
		sku += chr(num+48+(num>9)*7) #Convert number back to character
	
	return sku
#End of skuenc(id, website='amazon')
	
def skudec(sku):
	sku = str(sku).upper()
	#Prefix '|', old format
	prefixSplit = sku.split('|') 
	if len(prefixSplit)>1:
		website = prefixDec.get(prefixSplit[0], '')
		sku = prefixSplit[1]
	else:
	    #Prefix '!', new format
	    prefixSplit = sku.split('!')
	    if len(prefixSplit)>1:
		    website = prefixDec.get(prefixSplit[0], '')
		    sku = prefixSplit[1]
	    else:
		    website = ''
	
	id = ''
	L = 36
	for i in range(0, len(sku)): #Decoding part, the same algorithm as encoding
		num = ord(sku[i])-48-(sku[i]>='A')*7 #Convert character to number 0-35
		num =  (2*(2**i % L) - num) % L #Encoding: mirror the number to (2**i % L)
		id += chr(num+48+(num>9)*7) #Convert number back to character
		
	#Take care of a bug that amazon asin is longer than 10 chars.
	if website == 'amazon':
	    id = id[-10:]    
		
	return (website, id)
#End of skudec(sku)

def buyercheck(buyerid):
    #check ebay buyer credential
    #input buyer ebay id
    #output a dictionary with newbuyerflag ('1' means new buyer) and feedback score.
    #buyerid='josephioii'
    #buyerdict default is {'feedback':-1,'newbuyerflag':-1}
    buyerdict={'feedback':-1,'newbuyerflag':-1}
    url = "http://myworld.ebay.com/"+buyerid
    root = url2HTML(url,parser='soup')

    ######debug##############################
    #html = url2str(url)
    #with open("results.html", "w") as f:
    #    f.write(html)
    #print root.find('a',{'id':re.compile('feedBack')}).find(text=True)
    #print root.find('img',{'alt':re.compile('New eBay Member')})
    #########################################
    scoreblk = root.find('a',{'id':'feedBackScoreDiv3'})
    if scoreblk:
        buyerdict['feedback']=float(scoreblk.find(text=True))
    if root.find('img',{'alt':re.compile('New eBay Member')}):
        buyerdict['newbuyerflag'] = 1
    else:
        buyerdict['newbuyerflag'] = 0
    #print buyerdict
    return buyerdict
    
#End of buyercheck(buyerid)    
    
    
    
###Wrapper for scrapy function
from scrapy.contrib.loader import XPathItemLoader
from scrapy.item import Item, Field
from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
from scrapy.conf import settings
from scrapy.crawler import CrawlerProcess
from scrapy import project, signals
from scrapy.http import Request


from multiprocessing.queues import Queue
import multiprocessing




#I believe for this for this not frequently used code, setting User-Agent is good enough. May improve later.
urllib2Header = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.57 Safari/537.1'}

class GenericItem(Item):
    details = Field()


class CrawlerWorker(multiprocessing.Process):
 
    def __init__(self, spider, result_queue):
        multiprocessing.Process.__init__(self)
        self.result_queue = result_queue
 
        self.crawler = CrawlerProcess(settings)
        if not hasattr(project, 'crawler'):
            self.crawler.install()
        self.crawler.configure()
 
        self.items = []
        self.spider = spider
        dispatcher.connect(self._item_passed, signals.item_passed)
 
    def _item_passed(self, item):
        self.items.append(item['details'])
  
    def run(self):
        self.crawler.crawl(self.spider)
        self.crawler.start()
        self.crawler.stop()
#         print self.items
        self.result_queue.put(self.items)


class GenericSpider(BaseSpider):
    """Our ad-hoc spider"""
    name = "GenericSpider"
    allowed_domains = [ "http://amazon.com"]
    start_urls = []
#     print 'installed'

    def __init__(self, urlList, parser):
        self.start_urls = urlList
#         print self.start_urls
        self.parser = parser

    def updateUrl(self, urlList):
        self.start_urls = urlList
        
    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, headers = urllib2Header)
        
    def parse(self, response):
        #filename = response.url.split("www.")[-1].split('/')[0][:-4]
        #open(filename, 'wb').write(response.body)
        print  "Url read: "+response.url
        # a = response.body
        genItem = GenericItem()
        # genItem['details'] = {}
        genItem['details'] = self.parser(response.url, response.body)
        # print 'item detail: ', self.parser(response.url, response.body)
        yield genItem
        

def crawl(urlList, parser):
    resultsQue = Queue()
    crawler = CrawlerWorker(GenericSpider(urlList, parser), resultsQue)
    print 'crawler created'
    crawler.start()
    print 'crawler started'
    resultList = []
    for item in resultsQue.get():
        resultList.append(item)
    return resultList

def imageprocess(inputurl,filepath,filename):
    def resize(im,pixel):
      try:
        size = im.size
        w1 = size[0]
        h1 = size[1]
        if w1 >= h1:
            w2 = pixel
            h2 = int(float(w2)/float(w1)*float(h1))
        else:
            h2 = pixel
            w2 = int(float(h2)/float(h1)*float(w1))
        im1=im.resize((w2,h2),Image.ANTIALIAS)
      except Exception,e:
        print e
        im1 = im
      return im1

    f_imgurl = ''
    #Save image on local drive
    f = open(filepath+filename,'wb')
    f.write(urllib.urlopen(inputurl).read())
    f.close()
    
    #check image size
    try:
        im = Image.open(filepath+filename)
    except Exception,e:
        print e
        return f_imgurl 
    size = im.size

    if max(size) < 350:
        return f_imgurl
    elif max(size) < 500:
        im1 = resize(im,500)
        im1.save(filepath+filename)
    else:
        pass
    
    #FTP to GoDaddy
    #establish ftp connection
    sftp = ftplib.FTP()
    sftp.connect('184.168.61.1','21')
    print sftp.getwelcome()
    sftp.login('happ9228','Weare777!')
    sftp.cwd("ebayimg") 
    #uploadlist.append(filename)
    f_imgurl = "http://www.happitail.info/ebayimg/"+filename
    try:
        #sftp = ftplib.FTP('184.168.61.1','happ9228','Weare777!')
        fp=open(filepath+filename,'rb')
        print filepath+filename
        print 'STOR ebayimg/'+filename
        sftp.storbinary('STOR '+filename,fp)
        fp.close
    except Exception,e:
        print e
        sftp = ftplib.FTP()
        sftp.connect('184.168.61.1','21')
        print sftp.getwelcome()
        sftp.login('happ9228','Weare777!')
        sftp.cwd("ebayimg")
        fp=open(filepath+filename,'rb')
        print filepath+filename
        print 'STOR ebayimg/'+filename
        sftp.storbinary('STOR '+filename,fp)
        fp.close
    return f_imgurl

def readFeedback(ebayaccount,feedbacktype):
    #This function reads the most recent 200 feedbacks for the given ebayaccount (e.g. 'icelynne','dealsea') and feedbacktype ('positive','negative','neutral')
    #Return a list of tuple. [('1','buyer1'),('1','buyer2'),...]
    feedbacklist = []
    if feedbacktype == 'neutral': feedbackflag = '0'
    elif feedbacktype == 'negative': feedbackflag = '-1'
    elif feedbacktype == 'positive': feedbackflag = '1'
    else:
        print "please enter valid feedback type: positive, negative or neutral"
    feedbackurl = "http://feedback.ebay.com/ws/eBayISAPI.dll?ViewFeedback2&userid="+ebayaccount+"&iid=-1&de=off&items=200&which="+feedbacktype+"&interval=30&_trkparms=positive_30"
    soup = url2HTML(feedbackurl,'soup')

    for buyerblk in soup.findAll('span',{"class":"mbg-nw"}):
        buyerid = buyerblk.find(text=True)
        if buyerid <> ebayaccount:
            feedbacklist.append((feedbackflag,buyerid))
    return feedbacklist


def seller_item_id_extract(seller,sort_option):
    '''
    seller_item_id_extract(seller,sort_option)
    Get eBay item id, title, and start date of items from one seller.
    
    --Input
    seller: Seller id in str and sort_option
    
    --Output
    items: Item details as a list, each item is a dictionary.
    '''
    
   #   Initialization
    items = []
    try:
        #Get etree root of the user ebay page.
        #urlStr = operation3.url2str("http://www.ebay.com/sch/m.html?_sop=16&_ipg=200&_ssn="+seller)
        #See the acitve items page with all categories.
        urlStr = url2str("http://www.ebay.com/sch/m.html?_sop="+sort_option+"&_ipg=200&_ssn="+seller+"&_sac=1#seeAllAnchorLink")
        if not urlStr:
            return items
        root = etree.HTML(urlStr)
        #print root
        
        # #Check number of pages.
        # nPage = 0;
        # pageTag = root.xpath('//div[@class="pgr-t" and @id="ResultSetTopPager"]/div[1]')
        # try:
            # nPage = int(pageTag[0].text.split('of')[-1]) if pageTag else 0
        # except Exception, e:
            # print e

        #Added by Larry 6-10-2013. eBay changed layout. The above nPage code no longer worked
        #New nPage code added below
        
        rcnt = int(root.xpath('//span[@class="rcnt"]')[0].text.replace(',',''))
        print rcnt
        if rcnt <=9800:
            nPage = (int(rcnt)-1)/200 + 1
            print nPage
        
            items += searchpage_item_id_parser(urlStr)
            print 'Seller: %s, Page 1' %seller
            for iPage in range(2, nPage+1):
            #for iPage in range(2, 4):
                print 'Seller: %s, Page %d' %(seller, iPage)
                urlStr = url2str("http://www.ebay.com/sch/m.html?_sop="+sort_option+"&_ipg=200&_ssn=%s&_pgn=%d" %(seller, iPage))
                if urlStr: items += searchpage_item_id_parser(urlStr)
        
        else:
            categories = root.xpath('//div[@class="catsgroup"]/div[@class="cat-t"]/a')
            #for iCat in [0]:
            for iCat in range(0, len(categories)):
                htmlStr = categories[iCat].get('href', 'http://www.ebay.com/sch/m.html').split('m.html')[0]+'m.html'
                print htmlStr
                urlStr = url2str("%s?_sop=%s&_ipg=200&_ssn=%s" % (htmlStr, sort_option, seller))
                root = etree.HTML(urlStr)
                rcnt = int(root.xpath('//span[@class="rcnt"]')[0].text.replace(',',''))
                print rcnt
                nPage = (int(rcnt)-1)/200 + 1
                if nPage>=50: nPage = 49
                print nPage
                items += searchpage_item_id_parser(urlStr)
                print 'Seller: %s, Category %d, Page 1' % (seller, iCat)
                
                # #Debug purpose
                # itemsT = []
                # file = open('1.html', 'w')
                # file.write(urlStr)
                # file.close()
                # itemsT = searchpage_item_id_parser(urlStr)
                # listIDs = [t['listID'] for t in items]
                # for item in itemsT:
                    # if item['listID'] in listIDs:
                        # print 'Set mismatch'
                        # print item
                        # raw_input()
                    # if item['listID'] == '360688251778':
                        # print 'Item found'
                        # print item
                        # raw_input()
                # items += itemsT
                
                
                for iPage in range(2, nPage+1):
                    print 'Seller: %s, Category %d, Page %d' %(seller, iCat, iPage)
                    urlStr = url2str("%s?_sop=%s&_ipg=200&_ssn=%s&_pgn=%d" % (htmlStr, sort_option, seller, iPage))
                    if urlStr: 
                        items += searchpage_item_id_parser(urlStr)
                        
                        # #Debug purpose
                        # itemsT = []
                        # file = open('%d.html' % iPage, 'w')
                        # file.write(urlStr)
                        # file.close()
                        # itemsT = searchpage_item_id_parser(urlStr)
                        # listIDs = [t['listID'] for t in items]
                        # for item in itemsT:
                            # if item['listID'] in listIDs:
                                # print 'Set mismatch'
                                # print item
                                # raw_input()
                            # if item['listID'] == '360688251778':
                                # print 'Item found'
                                # print item
                                # raw_input()
                        # items += itemsT
                
        return items
        
    except Exception, e:
        print e
        return items
 
#End of seller_item_id_extract(seller)
    
    
def searchpage_item_id_parser(urlStr, url=''):
    '''
    seller_item_id_parser(urlStr)
    Get id, title, and start date of items from one ebay search result page.
    
    --Input
    urlStr: url string of the ebay item search result page.
    url: url address of the input string
    
    --Output
    items: Item details as a list, each item is a dictionary.
    '''
    
    #   Initialization
    items = []
    try:
        if not urlStr and url == '':
            return items
        elif url <> '':
            urlStr = url2str(url)
        root = etree.HTML(urlStr)
        listingTags = root.xpath('//div[@class = "ittl"]/a[1]')
        ##Added by Larry 6-10-2013. eBay layout change
        listingTags = root.xpath('//div[@class = "ittl"]//a[1]')
        #listingTags = root.xpath('//table[@itemprop="offers"]')
        if not listingTags: print "no tag found"
        count = 0
        timeNow = datetime.now()
        for listing in listingTags:
            count +=1
#             if count>1:
#                 break
            #print count + 1
            items += [{'listID': '', 'title': '', 'listTime': '','price': ''}]
            item = items[-1]
            #print item
            
            # #debug purpose
            # listID = listing.get('href', '').split('itm/')[-1].split('?')[0].split('/')[-1]
            # exIDs = [t['listID'] for t in items]
            # print exIDs
            # print listID
            # if listID in exIDs:
                # raw_input()
           
            item['listID'] = listing.get('href', '').split('itm/')[-1].split('?')[0].split('/')[-1]
            item['title'] = listing.text
            ##Added by Larry 10-16-2013 to include price
            pricetag = listing.xpath('../../../..//div[@itemprop = "price"]')
            if pricetag:
                item['price'] = pricetag[0].text.strip().strip('$')
            listTimeTags = listing.xpath('../../../..//span[@class = "tme"]/span[1]')
            if listTimeTags:
                try:
                    listTime = datetime.strptime(listTimeTags[0].text, '%b-%d %H:%M')
                    listTime = listTime.replace(year=2013)
                    if listTime>timeNow:
                        listTime = listTime.replace(year = timeNow.year-1)
                    item['listTime'] = str(listTime)
                except Exception, e:
                    print 'Exception in searchpage_item_id_parser function.'
                    print 'Cannot parse listTime information.'
                    print 'url: '+ url
                    print e
 
 # count += 1
            # if count >2:
                # break
        listIDs = [t['listID'] for t in items]
        listIDsSet = set(listIDs)
        if len(listIDs) != len(listIDsSet):
            print 'Subset mismatch.'
            raw_input()

        return items
        
    except Exception, e:
        print e
        return items

#End of searchpage_item_id_parser(urlStr)


def getAmznCAInfo(asin):
   
    priceinfo = {'sku' : asin}
    priceinfo['produrl'] = 'http://www.amazon.ca/dp/'+asin
    priceinfo['title'] = ''
    priceinfo['shipping'] = 999
    priceinfo['prime'] = 0
    priceinfo['availability' ] = 0
    priceinfo['maxqty'] = 1
    priceinfo['thirdparty'] = 1
    priceinfo['qtyInStock'] = 20
    priceinfo['add-on'] = 0
  
    try:
        url = 'http://www.amazon.ca/dp/'+asin
        htmlStr = url2str(url)

        priceinfo.update(parseAmznCAInfo(htmlStr))
   


    except Exception, e:
        print asin
        print e
        return priceinfo

    return priceinfo

#End of getAmznCAInfo(asin)

def parseAmznCAInfo(strHTML):

    priceinfo = {}

    #Initial values. Note: 'price' is not intialized.
    priceinfo['title'] = ''
    priceinfo['shipping'] = 999
    priceinfo['prime'] = 0
    priceinfo['availability' ] = 0
    priceinfo['maxqty'] = 1
    priceinfo['thirdparty'] = 1
    priceinfo['qtyInStock'] = 20
    priceinfo['add-on'] = 0
    priceinfo['currency'] = 'CAD'

    try:
        root = etree.HTML(strHTML)

        #produrl and sku from meta header
        linkTags= root.xpath('//link[@rel="canonical"]')
        if linkTags:
            priceinfo['produrl'] = linkTags[0].get('href', '')

            if 'dp/' in priceinfo['produrl']:
                sku = priceinfo['produrl'].split('dp/')[-1]
            else:
                sku = priceinfo['produrl'].split('/')[-1]
            if len(sku) == 10:
                priceinfo['sku'] = sku
            # else:
                # print 'error: cannot find amazon asin.'
        else:
            print 'Error: Cannot find product url tag in meta tags.'

        #Get product details and correct sku
        details = ''
        asin = ''
        isbn10 = ''
        detailblk = root.xpath('.//div[@id="detail-bullets_feature_div"]')
        if not detailblk:
            detailblk = root.xpath('.//h2[text()="Product Details"]/..')
        if detailblk:
            for bullet in detailblk[0].xpath('.//li'):
                detail = bullet.xpath('.//text()')
                liststrip(detail)
                detailtext = ' '.join(detail)
                detailtextlower = detailtext.lower()
                #see if it's customer review. If yes, stop
                if 'average customer' in detailtextlower:
                    break
                elif 'amazon' in detailtextlower:
                    break
                elif 'asin' in detailtextlower:
                    asin = detailtextlower.split('asin:')[-1].strip().upper()
                    continue
                elif 'shipping:' in detailtextlower:
                    continue

                #Dimension
                elif 'dimensions:' in detailtextlower:
                    #canada
                    dims = detailtextlower.split('dimensions:')[-1].split('cm')[0].split('x')
                    priceinfo['dimensions'] = sorted([float(dim) for dim in dims], reverse = True)

                #Weight
                elif 'weight:' in detailtextlower:
                    if 'kg' in detailtextlower:
                         #canada
                         priceinfo['weight'] = float(detailtextlower.split('weight:')[-1].split('kg')[0])
                    elif 'ounces' in detailtextlower:
                         priceinfo['weight'] = float(detailtextlower.split('weight:')[-1].split('ounces')[0])/16
                    detailtext = detailtext.split('(')[0]

                #Isbn10
                elif 'isbn-10:' in detailtextlower:
                    isbn10 = detailtextlower.split('isbn-10:')[-1].strip().upper()
                    if len(isbn10) == 10:
                        priceinfo['isbn10'] = isbn10

                #Isbn13
                elif 'isbn-13:' in detailtextlower:
                    priceinfo['isbn13'] = detailtextlower.split('isbn-13:')[-1].strip().replace('-', '').upper()

                #Grab release date in various cases.
                elif 'publisher:' in detailtextlower:
                    strRelDate = detailtextlower.split('(')[-1].split(')')[0].strip()
                    try:
                        timeRelDate = time.strptime(strRelDate, '%B %d, %Y')
                        priceinfo['releaseDate'] = time.strftime("%Y-%m-%d", timeRelDate)
                    except Exception, e:
                        try:
                            timeRelDate = time.strptime(strRelDate, '%B %Y')
                            priceinfo['releaseDate'] = time.strftime("%Y-%m-%d", timeRelDate)
                        except Exception, e:
                            try:
                                timeRelDate = time.strptime(strRelDate, '%Y')
                                priceinfo['releaseDate'] = time.strftime("%Y-%m-%d", timeRelDate)
                            except Exception, e:
                                print ("Warning: Cannot get release date from item url: ")
                                print e
                                print detailtext


                details = details+detailtext+'<br>'
        priceinfo['details'] = details
        if len(asin) == 10:
            priceinfo['sku'] = asin
        elif len(isbn10) == 10:
            priceinfo['sku'] = isbn10
        if not (len(priceinfo.get('sku', '')) == 10):
            print 'error: cannot find amazon asin.'
            return priceinfo

        sku = priceinfo['sku']


        #Amazon product page are formatted based on several different templates.
        #Format 1: The old format. Based on <form id="handleBuy">
        buyBlkTags = root.xpath('.//form[@id="handleBuy"]')
        if buyBlkTags:
            #Format 1. The conventional format.
            print 'Format 1'
            buyblk = buyBlkTags[0]

            #Get title.
            title = ''.join(buyblk.xpath('.//span[@id="btAsinTitle"]//text()'))
            priceinfo['title']=title.strip()

            #Get price and prime info.
            pricetag = buyblk.xpath('.//td[@id="actualPriceContent"]/span[@id="actualPriceValue"]/b[@class="priceLarge"]')
            #Larry added on 3-14-13 to catch some books with both new and rental
            if not pricetag: pricetag = buyblk.xpath('.//td[@class="rightBorder buyNewOffers"]/span[@class="rentPrice"]')
            #Larry added on 9-6-13 to catch some books with both new and rental
            #if not pricetag: pricetag = buyblk.xpath('.//td[@class=re.compile("buyNewOffers")]/span[@class="rentPrice"]')
            if not pricetag: pricetag = buyblk.xpath('.//td[@class=" buyNewOffers"]/span[@class="rentPrice"]')
            if (pricetag): #if price is displayed
                #canada
                priceinfo['price'] = float(pricetag[0].text.split('$')[-1].strip().replace(',',''))
                priceinfo['prime'] = 0
                priceinfo['shipping'] = 999
                priceinfo['availability'] = 0
                #if free shipping available, it's prime eligible
                if 'free' in etree.tostring(pricetag[0].getparent().getparent(), method='text', encoding='utf-8').lower():
                    priceinfo['prime'] = 1
                    priceinfo['shipping'] = 0

            else: #If price is "too low to display"
                if buyblk.xpath('.//td[@id="actualPriceContent"]/span[@id="actualPriceValue"]//a[@target="WhyNoPrice"]'):
                    extrainfo = getAmznPriceHF(sku)
                    if 'price' in extrainfo:
                        priceinfo['price'] = extrainfo['price']
                        priceinfo['prime'] = 0
                        priceinfo['shipping'] = 999
                        priceinfo['availability'] = 0
                        #if free shipping available, it's prime eligible
                        shptag = buyblk.xpath('.//td[@id="shippingMessageStandAlone"]')
                        if shptag:
                            if 'free' in etree.tostring(shptag[0], method='text', encoding='utf-8').lower():
                                priceinfo['prime'] = 1
                                priceinfo['shipping'] = 0

            if not ('price' in priceinfo):
                priceinfo['price'] = 4999
                priceinfo['maxqty'] = 0
                priceinfo['availability'] = 0
            else:
            #Get the shipping info if not prime.
                if not priceinfo.get('prime', 0):
                    shptag = buyblk.xpath('.//span[@class="plusShippingText"]')
                    if shptag:
                        if 'free' in shptag[0].text.lower():
                            priceinfo['shipping'] = 0
                        else:
                            if len(shptag[0].text.split('$'))>1:
                                priceinfo['shipping'] = float(shptag[0].text.split('$')[1].split(u'\xa0')[0])

                #Get availability info.
                priceinfo['availability']=0
                availtag = buyblk.xpath('.//span[@class="availGreen"]')
                if availtag:
                    priceinfo['availability'] = 1
                    #Get the qtyInStock information. This field is only meaningful when availability = 1.
                    availtext = availtag[0].text
                    if 'Only' in availtext:
                        priceinfo['qtyInStock'] = int(availtext.split(' ')[1])
                else:
                    availtag = buyblk.xpath('.//span[@class="availOrange"]')
                    if availtag:
                        availtext = availtag[0].text
                        if 'released' in availtext.lower():
                            priceinfo['availability'] = 1
                        elif 'day' in availtext.lower():
                            priceinfo['availability'] = availtext.lower().split('day')[0].split()[-1]
                if availtag:
                    sellertext = ''.join(availtag[0].xpath('../descendant-or-self::text()'))
                    #canada
                    if 'sold by amazon.ca' in sellertext.lower():
                        priceinfo['thirdparty'] = 0
                    else:
                        priceinfo['thirdparty'] = 1

            #Get maximum order quantity info.
            maxqty = 0
            if buyblk.xpath('.//select[@id="quantity"]/option'):
                #print etree.tostring(buyblk.xpath('.//select[@id="quantity"]/option')[0])
                maxqty = int(buyblk.xpath('.//select[@id="quantity"]/option')[-1].text)
                priceinfo['maxqty'] = maxqty


        else:
            price_feature = root.xpath('.//div[@id="price_feature_div"]')
            #print "price_feature"
            #print etree.tostring(price_feature[0])
            if price_feature:
                #Format 2: The new format. Added 10-15-2013.
                print 'Format 2'

                #Get title
                title = ''.join(root.xpath('.//h1[@id="title"]//text()'))
                priceinfo['title']=title.strip()

                #Price
                priceText = ''.join(price_feature[0].xpath('.//span[@id="priceblock_ourprice"]//text()'))
                if '$' in priceText:
                    priceinfo['price'] = float(priceText.split('$')[-1])
                #Prime
                primeText = ''.join(price_feature[0].xpath('.//span[@id="ourprice_shippingmessage"]//text()'))
                if 'free' in primeText.lower():
                    priceinfo['prime'] = 1
                    priceinfo['shipping'] = 0

                #If cannot get price info, use the getAmznPriceHF() function.
                if not ('price' in priceinfo):
                    extrainfo = getAmznPriceHF(sku)
                    if 'price' in extrainfo:
                        priceinfo['price'] = extrainfo['price']
                        priceinfo['prime'] = extrainfo['prime']
                        priceinfo['shipping'] = extrainfo['shippingfee']
                        priceinfo['availability'] = extrainfo['availability']

                if not ('price' in priceinfo):
                    priceinfo['price'] = 4999
                    priceinfo['maxqty'] = 0
                    priceinfo['availability'] = 0
                else:
                    #Get shipping fee
                    if not priceinfo.get('prime', 0):
                        shpText = ''.join(root.xpath('//span[contains(@class, "shipping3P")]//text()'))
                        if 'free' in shpText.lower():
                            priceinfo['shipping'] = 0
                        elif '$' in shpText:
                            priceinfo['shipping'] = float(shpText.split('$')[1].split()[0].replace(',', ''))

                    #Get availability, instock qty, and third party info.
                    availabilityTags = root.xpath('//div[@id="availability_feature_div"]')
                    if availabilityTags:
                        #print "availabilityTags"
                        #Availability
                        availabilityText = ''.join(availabilityTags[0].xpath('./div[@id="availability"]//text()'))
                        if 'in stock' in availabilityText.lower():
                            priceinfo['availability'] = 1
                        if 'week' in availabilityText.lower():
                            priceinfo['availability'] = 0
                        elif 'day' in availabilityText.lower():
                            availStr = availabilityText.lower().split('day')[0].split()[-1]
                            if '-' in availStr:
                                availStr = availStr.split('-')[-1].strip()
                            priceinfo['availability'] = int(availStr)
                        #Instock qty
                        if 'only' in availabilityText.lower():
                            priceinfo['qtyInStock'] = int(availabilityText.lower().split('only')[1].split()[0])
                        #Third party flag
                        merchantText = ''.join(availabilityTags[0].xpath('./div[@id="merchant-info"]//text()'))
                        if 'sold by amazon.com' in merchantText.lower():
                            priceinfo['thirdparty'] = 0
                        else:
                            priceinfo['thirdparty'] = 1

                    #Get maximum order quantity info.
                    maxqtyTags = root.xpath('.//select[@id="quantity"]/option')
                    if maxqtyTags:
                        #print etree.tostring(maxqtyTags[0])
                        maxqty = int(maxqtyTags[-1].text)
                        priceinfo['maxqty'] = maxqty

            else:
                'Format 3'
                print 'Format 3: book format'
                #print priceinfo['availability']
                #print 'No buy block found'
                #print priceinfo

                #Get title when "handleBuy" does not exist.This is usually for books
                title = ''.join(root.xpath('.//h1[@id="title"]//text()'))
                priceinfo['title']=title.split('\n')[0].strip()

                #Get price, availability, prime information for books
                buyboxes = root.xpath('.//div[@id="buybox"]')
                print 'Number of buyboxes: %d' % len(buyboxes)
                if buyboxes:
                    buybox = buyboxes[0]
                    #Only get price related information for new items
                    newprice = ''.join(buybox.xpath('.//div[@id="buyNewSection"]//text()'))
                    #print str(newprice)
                    if newprice.find('$')>0:
                        priceinfo['price'] = float(newprice.split('$')[1].replace(',',''))
                    # else:
                        # priceinfo['price'] = 4999

                    #Get prime info: option1
                    if buybox.xpath('.//div[@id="buyNewSection"]//span[@class="primeBadge inlineBlock-display prime-padding"]'):
                        priceinfo['prime'] = 1
                        priceinfo['shipping']=0
                    else:
                        priceinfo['prime'] = 0
                        #hardcode shipping to $4
                        priceinfo['shipping']= 4

                    #get availability, maxquantity and third party flag
                    #Still missing availability and qtyInStock -Jiong
                    buyNewInner = buybox.xpath('.//div[@id="buyNewInner"]')
                    if buyNewInner:
                        #print "inside buyNewInner"
                        buyNewInner0 = buyNewInner[0]
                        #Get maximum order quantity info.
                        maxqty = 0
                        if buyNewInner0.xpath('.//select[@id="quantity"]/option'):
                            maxqty = int(buyNewInner0.xpath('.//select[@id="quantity"]/option')[-1].text.strip('+'))
                            priceinfo['maxqty'] = maxqty
                        #Get availability
                        priceinfo['availability']=0
                        availText = ''.join(buyNewInner0.xpath('.//div[@id="availability"]//text()'))
                        print availText
                        if availText.lower().find('in stock')>0:
                            priceinfo['availability']=1
                        #Get thirdparty information
                        priceinfo['thirdparty']=1
                        merchantText = ''.join(buyNewInner0.xpath('.//div[@id="merchant-info"]//text()'))
                        if 'amazon.com' in merchantText.lower():
                            priceinfo['thirdparty']=0
                        #Get prime info: option2
                        if ''.join(buyNewInner0.xpath('.//text()')).find('on orders over $35')>0:
                            priceinfo['prime'] = 1
                            priceinfo['shipping']=0
                        else:
                            priceinfo['prime'] = 0
                            #hardcode shipping to $4
                            priceinfo['shipping']= 4

                    else:
                        priceinfo['availability']=0
                        priceinfo['maxqty']=0
                        priceinfo['thirdparty']=1


                    #If cannot get price info, use the getAmznPriceHF() function.
                    if not ('price' in priceinfo):
                        print 'Cannot get price info from the item page, use getAmznPriceHF() to extract info.'
                        print sku
                        extrainfo = getAmznPriceHF(sku)
                        if 'price' in extrainfo:
                            priceinfo['price'] = extrainfo['price']
                            priceinfo['prime'] = extrainfo['prime']
                            priceinfo['shipping'] = extrainfo['shippingfee']
                            priceinfo['availability'] = extrainfo['availability']

                    if not ('price' in priceinfo):
                        priceinfo['price'] = 4999
                        priceinfo['maxqty'] = 0
                        priceinfo['availability'] = 0


        #print priceinfo
        ##Extract fields without dependence on "handleBuy" block.
        #Add-on
        addonTags = root.xpath('//div[@id="addonBuyboxID"]/child::*')
        centercol = root.xpath('//div[@id="centerCol"]')
        if addonTags: priceinfo['add-on'] = 1
        #added 11-24-2013 by Larry
        elif centercol:
            if etree.tostring(centercol[0]).find('This item is available because of the Add-on program')>0:
                priceinfo['add-on'] = 1


        #Get product features
        #Format 2
        features = ''
        featureblk = root.xpath('.//div[@id="featurebullets_feature_div"]')
        if not featureblk:
            featureblk = root.xpath('.//h2[text()="Product Features"]/..')
        if featureblk:
            for bullet in featureblk[0].xpath('.//li'):
                features = features + ' '.join(bullet.xpath('.//text()')) + '<br>'
            priceinfo['features'] = features+'<br>'+priceinfo['features'] if 'features' in priceinfo else features
                # if bullet.text:
                    # features = features + bullet.text + '<br>'
            # priceinfo['features'] = features

        #Format 1
        #Features may be loacated right after price.
        if not features:
            featureblk = root.xpath('.//div[@id="feature-bullets-atf"]')
            if featureblk:
                for bullet in featureblk[0].xpath('.//li'):
                    features = features + ' '.join(bullet.xpath('.//text()')) + '<br>'
                priceinfo['features'] = features+'<br>'+priceinfo['features'] if 'features' in priceinfo else features

        #Format 3
        if not features:
            featureblk = root.xpath('//div[@id="bookDescription_feature_div"]/noscript[1]')
            if featureblk:
                features = features + etree.tostring(featureblk[0]).split('<noscript>')[-1].split('</noscript>')[0].strip()
                priceinfo['features'] = features+'<br><br>'+priceinfo['features'] if 'features' in priceinfo else features


        #Get technical details
        techdetails = ''
        techblk = root.xpath('.//div[@id="technical-data_feature_div"]')
        if not techblk:
            techblk = root.xpath('.//h2[text()="Technical Details"]/..')
        if techblk:
            for bullet in techblk[0].xpath('.//li'):
                if bullet.text:
                    techdetails = techdetails + bullet.text + '<br>'
            if techdetails == '':
                for bullet in techblk[0].xpath('.//li'):
                    techdetail = bullet.xpath('.//text()')
                    liststrip(techdetail)
                    techdetails = techdetails+''.join(techdetail)+'<br>'
        priceinfo['techdetails'] = techdetails




        #Get large image url
        imgurl = ''
        imgblk = root.xpath('.//table[@class="productImageGrid"][1]')
        if imgblk:
            imgtag = imgblk[0].xpath('.//img[@id="main-image"][1]')
            if imgtag:
                #print etree.tostring(imgtag[0])
                imgurl = imgtag[0].get('rel', '')
                if not imgurl:
                    imgurl = imgtag[0].get('src', '')
            #canada
            else:
                imgblk = root.xpath('.//div[@id="main-image-container"]')
                if imgblk:
                    imgtag = imgblk[0].xpath('.//img[1]')
                    if imgtag:
                        imgurl = imgtag[0].get('data-old-hires', '')
                        if not imgurl:
                            imgurl = imgtag[0].get('src', '')
        else:
            print "productImgeGrid not found"
            imgblk = root.xpath('.//div[@id="main-image-container"]')
            if imgblk:
                imgtag = imgblk[0].xpath('.//img[1]')
                if imgtag:
                    imgurl = imgtag[0].get('data-old-hires', '')
                    if not imgurl:
                        imgurl = imgtag[0].get('src', '')

        imgurlSplit = imgurl.split('/I/', 1)
        if len(imgurlSplit)>1:
            imgurl = imgurlSplit[0]+'/I/'+imgurlSplit[1].split('.', 1)[0]+'.'+imgurlSplit[1].split('.')[-1]
        priceinfo['imgurl'] = imgurl

        #Get variations Format 2 only
        twister_feature = root.xpath('.//div[@id="twister_feature_div"]')
        if twister_feature:
            variations = twister_feature[0].xpath('.//li[@class="swatchSelect"]/@title')
            for item in variations:
                variation = item.split('select')[1].strip()
                priceinfo['title']=variation+' '+priceinfo['title']
        #get variations Format 1 only
        else:
            table_variations = root.xpath('.//table[@class="variations"]')
            if table_variations:
                variations = table_variations[0].xpath('.//b[@class="variationLabel"]/text()')
                for variation in variations:
                    priceinfo['title']=variation+' '+priceinfo['title']

        #get similar products Format 2 only. Added 12-29-2013
        sims = []
        sims_feature = root.xpath('.//div[@id="purchase-sims-feature"]')
        if sims_feature:
            simslist = sims_feature[0].xpath('.//a[@class="sim-img-title"]/@href')
            for sim in simslist:
                sims.append(sim.split('dp/')[-1].split('/')[0])
        if sims:
            priceinfo['sims'] = sims

    except Exception, e:
        print e
        print 'Exception in function parseAmznInfo(strHTML).'
        return priceinfo

    return priceinfo

#End of parseAmznCAInfo(strHTML)


def getAmznCAInfo2DB(asin, itemInfo = {}, cur = None, update_upc = False, verbose = False,writeDB = True, result='source'):
    '''
    getAmznCAInfo2DB(asin, cur = None, update_upc = False, verbose = False)

    Get Amazon.ca info and submit to database.
    This was copied from getAmznInfo2DB on 1-21-2014
    --Input
    asin: Asin of amazon item(s). It can be a single string or a list of asin strings.
    cur = None: The cursor of the db to be submitted to. If None, just get the amazon info of the asin(s).
    update_upc = False: If true, update item upc, brand and mpn in database.
    verbose = False: If True, asin, title and db submission status of each item will be printed.
    9/20/2013: add writeDB = True to input to provide an option NOT to write to DB
    Add option to return itemsource or itemProduct
    10/11/2013:
    If add-on ==1 from getAmznInfo, then set availability = 0 when commit to db.
    --Output
    itemSource: Item details from Amazon. Its type is the same as the input asin type (string or list).

    '''



    try:
        L = 0
        isInputList = 1
        if not type(asin)==list:
            asinList = [asin]  
            isInputList = 0
            itemProduct = itemInfo
        else:
            asinList = asin

        itemSourceList = []
        itemProductList = []
        for i in range(0, len(asinList)):
            itemSource = getAmznCAInfo(asinList[i])  
            if update_upc:
                itemSource.update(getAmznUPC(asinList[i]))
            itemSourceList.append(itemSource)

            if cur or result.lower()=='db':
                itemProduct = {'asin': asinList[i]}

                itemProduct['produrl'] = itemSource.get('produrl', '')

                if itemSource.get('title', ''):
                    itemProduct['title'] = itemSource['title'].encode('windows-1252', 'ignore')

                if verbose: print '%d: %s, %s' % (i, itemProduct['asin'], itemProduct.get('title', ''))

                if itemSource.get('isbn10', ''):
                    itemProduct['isbn10'] = itemSource['isbn10']

                if itemSource.get('isbn13', ''):
                    itemProduct['isbn13'] = itemSource['isbn13']

                if 'releaseDate' in itemSource:
                    itemProduct['releaseDate'] = itemSource['releaseDate']


                itemProduct['details'] = '<br>'.join([itemSource.get('features', ''), itemSource.get('techdetails', ''), itemSource.get('details', '')])
                if not itemProduct['details']:
                    del itemProduct['details']
                else:
                    itemProduct['details'] = itemProduct['details'].encode('windows-1252', 'ignore')


                itemProduct['price'] = itemSource.get('price', 4999)
                itemProduct['prime'] = itemSource.get('prime', 0)
                itemProduct['shipping'] = itemSource.get('shipping', 999)
                itemProduct['availability'] = itemSource.get('availability', 0)
                itemProduct['maxQty'] = itemSource.get('maxqty', 1)
                itemProduct['TPFlag'] = itemSource.get('thirdparty', 1)

                if itemSource.get('add-on', 0) == 1:
                    itemProduct['availability'] = 0

                if itemSource.get('weight', 0):
                    itemProduct['weight'] = itemSource['weight']
                print len(itemSource.get('dimensions', [0]))
                if len(itemSource.get('dimensions', [0]))==3:
                    itemProduct.update({['dimensionL', 'dimensionW', 'dimensionH'][j]:
                        itemSource.get('dimensions')[j] for j in range(0, 3)})
                elif len(itemSource.get('dimensions', [0]))==2:
                    itemProduct.update({['dimensionL', 'dimensionW'][j]:
                        itemSource.get('dimensions')[j] for j in range(0, 2)})
                if itemSource.get('imgurl', ''):
                    itemProduct['imgurl'] = itemSource['imgurl']

                if 'price' in itemProduct:
                    itemProduct['refreshTime'] = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())

                if update_upc:
                    if itemSource.get('upc', ''):
                        itemProduct['upc'] = itemSource['upc']

                    if itemSource.get('brand', ''):
                        itemProduct['brand'] = itemSource['brand'].encode('windows-1252', 'ignore')

                    if itemSource.get('mpn', ''):
                        itemProduct['mpn'] = itemSource['mpn'].encode('windows-1252', 'ignore')

                    if itemSource.get('description', ''):
                        itemProduct['description'] = itemSource['description'].encode('windows-1252', 'ignore')

                #print itemProduct
                itemProductList.append(itemProduct)
                if writeDB and cur:
                    L = insertDB([itemProduct], cur, 'prodAmazonCA', dupHandling='update')
                    #L = updateDB([asinList[i]], [itemProduct], cur, 'prodAmazon')
                if verbose:
                    if L: print 'Item updated in db.'
                    else: print 'Item not updated in db.'

        if isInputList:
            if result.lower() == 'source':
                return itemSourceList
            elif result.lower() =='db':
                return itemProductList
            else:
                return itemSourceList
        else:
            if result.lower() == 'source':
                return itemSourceList[0]
            elif result.lower() == 'db':
                return itemProductList[0]
            else:
                return itemSourceList[0]

    except Exception, e:
        print 'Exception in getAmznCAInfo2DB function.'
        return itemSourceList
        print e

#End of getAmznCAInfo2DB(asin)



def carrierConvert(serviceName):
    
    if ('fedex' in serviceName.lower()) or ('federal express' in serviceName.lower()):
        carrierEbay = 'FEDEX'
    elif ('ups' in serviceName.lower()) or ('united parcel service' in serviceName.lower()):
    	carrierEbay = 'UPS'
    elif ('usps' in serviceName.lower()) or ('us postal service' in serviceName.lower()) or ('united states postal service' in serviceName.lower()):
        carrierEbay = 'USPS'
    elif 'dhl' in serviceName.lower():
        carrierEbay = 'DHL Global Mail'
    elif 'parcelpool' in serviceName.lower():
        carrierEbay = 'Parcel Pool'
    elif 'a-1 courier' in serviceName.lower():
        carrierEbay = 'A1 Courier Services'
    elif 'amzn_us' in serviceName.lower():
        #eBay does not support AMZN_US, use UPS instead so tracking can be uploaded
        carrierEbay = 'UPS'
    else:
        carrierEbay = serviceName
        
    return carrierEbay

#End of carrierConvert(serviceName)

def getPage(url, data=None, cookie=None, referer=None, decoder='UTF-8'):
    req=urllib2.Request(url)
    req.add_header('Host','bookdepository.com')
    req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.2; rv:25.0) Gecko/20100101 Firefox/25.0')
    req.add_header('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    req.add_header('Accept-Language','en-US,en;q:0.5')
    req.add_header('Accept-Encoding','gzip, deflate')
    req.add_header(r'Connection',r'keep-alive')
    if referer:
        req.add_header('Referer',referer)
    if cookie:
        req.add_header('Cookie',cookie)
    if data:
        req.add_header('Content-Type','application/x-www-form-urlencoded')
        page=urllib2.urlopen(req, data, timeout=300)
    else:
        page=urllib2.urlopen(url, timeout=300)
    if page.headers.get('Set-cookies'):
        cookie=page.headers.get('Set-cookies')
    try:
        return page.read().decode(decoder), cookie
    except:
        return str(page.read()), cookie
#End of getPage()

def getBDInfo(url):
    itemInfo={}
    itemInfo['title']=''
    itemInfo['availability'] = 0
    itemInfo['price'] = 4999
    itemInfo['prime'] = 0 
    itemInfo['shipping'] = 999
    referer='http://www.bookdepository.com'
    if url.find(referer)<0:
        url = referer+'/'+url    
    try:
        page, cookie=getPage(url, referer=referer)
        itemInfo = parseBDInfo(page, url)
    except Exception as error:
        print(error)
    return itemInfo 
#End of getBDInfo()

def parseBDInfo(page, url):
    itemDetails={}
    itemDetails['prime'] = 1
    parser=etree.HTMLParser()
    tree=etree.parse(io.StringIO(page), parser=parser)

    '''Get itemid'''
    itemid = url.replace('http://www.bookdepository.com/', '')
    itemDetails['itemid'] = itemid

    '''Get title'''
    title=tree.xpath('//meta[@property="og:title"]/@content')
    if title:
        itemDetails['title']=title[0]
    else:
        title=tree.xpath('//h1/strong/span')
        itemDetails['title']=title[0].text+' '+title[1].text

    '''Get category'''
    category=tree.xpath('//li[@class="categories"]/span[@class="linkSurround"]/a')
    temp=[]
    for item in category:
        if item.text!=None:
            temp.append(item.text)
    category='|'.join(temp)
    itemDetails['category']=category if category else ''

    '''Get isbn-10'''
    isbn10=tree.xpath('//span[@class="isbn10"]/span')
    itemDetails['isbn10']=isbn10[0].text if isbn10[0].text else ''

    '''Get isbn-13'''
    isbn13=tree.xpath('//span[@class="isbn13"]/span')
    itemDetails['isbn13']=isbn13[0].text if isbn13[0].text else ''

    '''Get upc'''
    upc=''
    itemDetails['upc']=upc

    '''Get brand'''
    brand=''
    itemDetails['brand']=brand

    '''Get model'''
    model=''
    itemDetails['model']=model

    '''Get mpn'''
    mpn=''
    itemDetails['mpn']=mpn

    '''Get releaseDate'''
    months = {'January':'01', 'February':'02', 'March':'03', 'April':'04', 'May':'05', 'June':'06',
              'July':'07', 'August':'08', 'September':'09', 'October':'10', 'November':'11', 'December':'12'}
    releaseDate = tree.xpath('//li[@class="publishDate"]/span')
    temp = releaseDate[0].text.split(' ')
    releaseDate = temp[2]+'-'+months[temp[1]]+'-'+temp[0]
    itemDetails['releaseDate'] = releaseDate if releaseDate else '0000-00-00'

    '''Get details'''
    details = ''
    itemDetails['details']=details

    '''Get description'''
    features = tree.xpath('//p[@class="shortDescription"]/text()')
    itemDetails['description'] = features[0].replace("\\","") if features[0] else ''
   
    '''Check if available'''
    unavailable=tree.xpath('//div[contains(@class, "priceBlock")]')
    if unavailable:
        itemDetails['price']=4999.0
        itemDetails['shipping'] = 999
        itemDetails['availability'] = 0
    else:
        '''Get price'''
        price = tree.xpath('//span[@class="price"]/strong/text()')
        itemDetails['price']=float(price[0][1:]) if price else 4999.0

        '''Get shipping'''
        shipping=tree.xpath('//strong[@class="deliveryMessage"]/text()')
        if 'Free' in shipping[0]:
            itemDetails['shipping'] = 0
        else:
            itemDetails['shipping']=float(shipping[0])

        '''Get availability'''
        availability=tree.xpath('//span[@class="dispatchMessage"]/text()')
        availability = int(availability[0].split(' ')[3]) / 24
        itemDetails['availability'] = availability

    '''Get imgUrl'''
    imgurl= None
    imgurls=tree.xpath('//meta[@property="og:image"]/@content')
    for img in imgurls:
        if 'large' in img:
            imgurl=img
    itemDetails['imgurl']=imgurl if imgurl else ''

    '''Get format'''
    form=tree.xpath('//li[@class="format"]/span/text()')
    itemDetails['format']=form[0]

    '''Get related'''
    related=tree.xpath('//h3/a/@href')
    itemDetails['related']=(related)

    '''Get salesRank'''
    salesRank=tree.xpath('//li[@class="salesRank"]/text()')
    if salesRank:
        for item in salesRank:
            value=item.replace('\n', '').replace('\t', '').replace(' ', '').replace(',', '')
            if value!='':
                itemDetails['saleRank']=int(value)
                break
    else:
        itemDetails['saleRank']=9999999

    '''Go to bibliographic data page'''
    newUrl = tree.xpath('//span[contains(@id, "Bibliographic")]/span/a/@href')
    page, cookie = getPage(newUrl[0], referer = url)
    tree=etree.parse(io.StringIO(page), parser=parser)

    dimensions=tree.xpath('//dd[@class="physicalProperties"]')
    dimensions=etree.tostring(dimensions[0])

    '''Get dimensionL'''
    try:
        temp=dimensions.index('Width')
        start=temp+dimensions[temp:].index('</em>')+5
        stop=start+dimensions[start:].index('<br')
        dimensionL=dimensions[start:stop]
        if 'mm' in dimensionL:
            dimensionL=int(dimensionL.replace('mm', '').strip(' '))*0.0393700787
        itemDetails['dimensionL']=dimensionL
    except:
        itemDetails['dimensionL']=0

    try:
        temp=dimensions.index('Height')
        start=temp+dimensions[temp:].index('</em>')+5
        stop=start+dimensions[start:].index('<br')
        dimensionW=dimensions[start:stop]
        if 'mm' in dimensionW:
            dimensionW=int(dimensionW.replace('mm', '').strip(' '))*0.0393700787
        itemDetails['dimensionW']=dimensionW
    except:
        itemDetails['dimensionW']=0

    try:
        temp=dimensions.index('Thickness')
        start=temp+dimensions[temp:].index('</em>')+5
        stop=start+dimensions[start:].index('<br')
        dimensionH=dimensions[start:stop]
        if 'mm' in dimensionH:
            dimensionH=int(dimensionH.replace('mm', '').strip(' '))*0.0393700787
        itemDetails['dimensionH']=dimensionH
    except:
        itemDetails['dimensionH']=0

    try:
        temp=dimensions.index('Weight')
        start=temp+dimensions[temp:].index('</em>')+5
        stop=start+dimensions[start:].index('<br')
        weight=dimensions[start:stop]
        if 'g' in weight:
            weight=int(weight.replace('g', '').strip(' '))*0.00220462262
        itemDetails['weight']=weight
    except:
        itemDetails['weight']=0

    '''Get maxQty'''
    itemDetails['maxQty']=10

    '''Get TPFlag'''
    itemDetails['TPFlag']=0

    '''Go to full description page'''
    newUrl = tree.xpath('//span[contains(@id, "Fulldescription")]/span/a/@href')
    page, cookie = getPage(newUrl[0], referer = url)
    tree=etree.parse(io.StringIO(page), parser=parser)

    '''Get description'''
    description=tree.xpath('//p[@class="paragraph"]/text()')
    itemDetails['description']=description[0] if description else ''

    return itemDetails
#end of parseDBInfo
       
       
       #http://www.ebay.com/sch/i.html?_nkw=the+davinci+code&_sop=12
#&_sop=12 means best match; &LH_BIN=1 means buy it now; &LH_ItemCondition=4 means used, 3 means new; LH_PreFloc=1 means US Only
#on productised item page. ?&tabs=15 for all items. &LH_BIN=1 for buy it now
#Two possible returns - one is product page for items with productized listing. Second is regular search result
#Tell by looking for <meta property="og:type" content="ebay-objects:item>
#Can also use <meta proerty="og:url" content="http://www.ebay.com/ctg/..../43435374">
#No matter what type of results, take top 5 and analyze them to get the desired information
#get up to 5 ebay item id from the keyword search
def eBaySearch(keywords):
    #keywords is a dictionary; two members keywords['barcode'],keywords['title']; return a list of eBay item url
    barcode = ''
    title = ''
    urlList = []
    if 'barcode' in keywords:
        barcode = keywords['barcode']
    if 'title' in keywords:
        title = keywords['title'].strip().replace(' ','+')
    if barcode <> '':
        url = 'http://www.ebay.com/sch/i.html?_nkw='+barcode+'&_sop=12&LH_BIN=1'
    elif title <> '':
        url = 'http://www.ebay.com/sch/i.html?_nkw='+title+'&_sop=12&LH_BIN=1'
    else:
        #print "No barcode nor title in keywords. Abort"
        return []
    root = url2HTML(url)
    #Detect whether page is productized page or normal search results
    #Productized page has this <meta proerty="og:url" content="http://www.ebay.com/ctg/..../43435374">
    typeTags = root.xpath('.//meta[@property="og:url"]')
    if typeTags:
        url2 = typeTags[0].xpath('@content')[0]
        epid = url2.split('/')[-1]
        #Append url2 so the return page is buy-it-now items with all conditions
        url2 = url2 + '?&tabs=15&LH_BIN=1'
        #refresh page with url2
        root2 = url2HTML(url2)

        #get ebay items on page
        itemTags = root2.xpath('.//a[@class="ls-ic"]')
        if itemTags:
            for itemTag in itemTags:
                urlList+=itemTag.xpath('@href')
    #when the result page is regular search result page
    else:
        itemTags = root.xpath('.//table[@itemprop="offers"]')
        if itemTags:
            for itemTag in itemTags:
                itemid = itemTag.xpath('@listingid')
                if itemid:
                    urlList+=['http://www.ebay.com/itm/?item='+itemid[0]]
    #print "%d results found" %len(urlList)
    return urlList
#end of eBaySearch()   


def percentile(N, percent, key=lambda x:x):
    """
    Find the percentile of a list of values.

    @parameter N - is a list of values. Note N MUST BE already sorted.
    @parameter percent - a float value from 0.0 to 1.0.
    @parameter key - optional key function to compute value from each element of N.

    @return - the percentile of the values
    """
    if not N:
        return None
    k = (len(N)-1) * percent
    f = math.floor(k)
    c = math.ceil(k)
    if f == c:
        return key(N[int(k)])
    d0 = key(N[int(f)]) * (c-k)
    d1 = key(N[int(c)]) * (k-f)
    return d0+d1
#End of percentile(N, percent, key=lambda x:x)
