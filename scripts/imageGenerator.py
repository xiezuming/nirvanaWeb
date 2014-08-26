#!/usr/bin/python

#Usage:
#Input is an image array eg. imageList = [1042,1043,1044]
#If image is converted successfully, set syncWp flag to 'Y' in item_image table


import operation3
import sys
import MySQLdb
import os
import urllib
import ftplib
import json
import os
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

FONT = os.path.dirname(os.path.realpath(__file__)) + '/arial.ttf'

def add_watermark(in_file, text, out_file, angle=23, opacity=0.8):
    img = Image.open(in_file).convert('RGB')
    watermark = Image.new('RGBA', img.size, (0,0,0,0))
    size = 2
    n_font = ImageFont.truetype(FONT, size)
    n_width, n_height = n_font.getsize(text)
    while n_width+n_height < watermark.size[0]:
        size += 2
        n_font = ImageFont.truetype(FONT, size)
        n_width, n_height = n_font.getsize(text)
    draw = ImageDraw.Draw(watermark, 'RGBA')
    draw.text(((watermark.size[0] - n_width) / 2,
              (watermark.size[1] - n_height) / 2),
              text, fill = (0,255,0), font=n_font)
    watermark = watermark.rotate(angle,Image.BICUBIC)
    alpha = watermark.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
    watermark.putalpha(alpha)
    Image.composite(watermark, img, watermark).save(out_file, 'JPEG')

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


dblogin = operation3.getDBLogin('webdb2')
#connect to mysqldb
conn = None
try:
    conn=MySQLdb.connect(host=dblogin['host'], user=dblogin['username'], passwd=dblogin['password'], db=dblogin['database'])
    cursor = conn.cursor()
except MySQLdb.Error, e:
    print "Error %d: %s" % (e.args[0], e.args[1])
    sys.exit(1)

#hard code imageList
imageList = [1047,1048,1049]
#Use the following code to upload all images that have not been uploaded
#imageList = []
#cursor.execute("select Global_Item_Image_ID from wetag.item_image where synchWp = 'N'")
#imageTuple = cursor.fetchall()
#for item in imageTuple:
#    imageList.append(item[0])
try:
    imageList = json.loads(sys.argv[1])
except:
    print "ERROR: Falied to parse input argument. argv[1] = " + sys.argv[1]
    sys.exit(1)

######################

#hard code image url path
if os.name == 'nt':
    filepath = "D:/temp/uploads/wetag_app/"
else:
    filepath = "/var/uploads/wetag_app/"

print 'The image id list = ' + str(imageList)

for image in imageList:
  try:
    cursor.execute("""select userId, imageName from 
                      wetag.item a join wetag.item_image b on a.Global_Item_ID = b.Global_Item_ID 
                      where b.Global_Item_Image_ID = %s""",(image,))
    data = cursor.fetchone()
    userid = data[0]
    filename = data[1]
    thumnail = filename.split('.')[0]+'-360.jpg'
    bigpicture = filename.split('.')[0]+'-800.jpg' 
    watermark = filename.split('.')[0]+'-360sold.jpg'
    
    print "  Start to create image files for " + filename

    im = Image.open(filepath+userid+'/'+filename)
    size = im.size
    sizetext = str(max(size))+","+str(min(size))
    print "  Current size", sizetext

    im1 = resize(im,360)
    im1.save(filepath+userid+'/'+thumnail)
    print "  Create thumnial image file successfully. " + filepath+userid+'/'+thumnail
    
    im2 = resize(im,800)
    im2.save(filepath+userid+'/'+bigpicture)
    print "  Create big image file successfully. " + filepath+userid+'/'+bigpicture
    
    add_watermark(filepath+userid+'/'+thumnail,'SOLD!',filepath+userid+'/'+watermark)
    size = im1.size
    sizetext = str(max(size))+","+str(min(size))
    print "  Create watermark file successfully. New size", sizetext
    
    #upload to godaddy
    #establish ftp connection
    ftp = operation3.getDBLogin('godaddyftp')
    sftp = ftplib.FTP()
    sftp.connect(ftp['host'],'21')
    print sftp.getwelcome()

    try:
        sftp.login(ftp['username'],ftp['password'])
    except Exception,e:
        print 'Failed to login, try again. e = ' + str(e)
        sftp.login(ftp['username'],ftp['password'])

    sftp.cwd("wetagimg")
    #check if userid folder exist or not
    if userid not in sftp.nlst():
        #create userid folder
        sftp.mkd(userid)
    #enter new folder
    sftp.cwd(userid)
    try:
        fp=open(filepath+userid+'/'+thumnail,'rb')
        print 'STOR wetagimg/'+userid+'/'+thumnail
        sftp.storbinary('STOR '+thumnail,fp)
        fp=open(filepath+userid+'/'+watermark,'rb')
        print 'STOR wetagimg/'+userid+'/'+watermark
        sftp.storbinary('STOR '+watermark,fp)
        fp=open(filepath+userid+'/'+bigpicture,'rb')
        print 'STOR wetagimg/'+userid+'/'+bigpicture
        sftp.storbinary('STOR '+bigpicture,fp)
        fp.close
        cursor.execute("""update wetag.item_image set synchWp='Y' where Global_Item_Image_ID = %s""",(image,))
        conn.commit()
        #close sftp
        sftp.quit()
    except Exception,e:
        print e
  except Exception,e:
    print image
    print e


cursor.close()
conn.close()
