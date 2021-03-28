#Jennifer Louie, Brandon Gipson, Jeremy Ide, Dylan Scholten
#2021 HooHacks
# with help from https://www.waveshare.com for display info
import sys
import os
picsdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd2in9d
import time
from PIL import Image,ImageDraw,ImageFont
import traceback
import socket
import pyqrcode
import png
from pyqrcode import QRCode

logging.basicConfig(level=logging.DEBUG)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("192.168.0.186", 2222))
print(s.recv(1024).decode('utf-8'))

drinkCt=0
bac=0
bacStr=str(bac)
Lname=input("Enter last name: ")
print(Lname)
Fname=input ("Enter first name: ")
print(Fname)
licenseAgeStr = input ("Enter license age: ")
print (licenseAgeStr)
licenseAge=float(licenseAgeStr)
genderStr=input("gender: female=1 male =0")
print(genderStr)
gender=float(genderStr)

if gender==1:
    gender=0.55
    genderStr=str(gender)
    print(gender)
    print('female checked')

else:
    gender=0.68
    genderStr=str(gender)
    print(gender)
    print('male checked')
    
bWeightStr = input ("Weight: ")
bWeight=float(bWeightStr)
event=input("Today's Event: ")

try:
    while True:
        #information
        drinkInfo = "%s %s, %s" % (Fname, Lname, drinkCt)

        #Generate QR Code
        img = pyqrcode.create(drinkInfo)

        #Save QR Code
        img.png(os.path.join(picsdir, 'drinkInfo.png'), scale = 6)
        
        drinkCtStr=str(drinkCt)
        logging.info("drink counter")
        
        epd = epd2in9d.EPD()
        logging.info("init and Clear")
        epd.init()
        epd.Clear(0xFF)
        
        #font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
        #font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)

        #Calculate bac
        bac=((drinkCt*0.031)/(bWeight*gender))*100
        bacStr="{:.2f}".format(bac)
        
        # Writes drink info
        logging.info("drink info printed")
        drinkInfo = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
        draw = ImageDraw.Draw(drinkInfo)
        draw.text((125, 25), Lname+', '+Fname)
        draw.text((125, 40), drinkCtStr +' TOTAL DRINKS')
        draw.text((125, 55), '1:06:53 ELAPSED')
        draw.text((125, 70), bacStr+'% APPROX BAC')
        draw.text((70,5), '-THE LONELY MALLARD-')
        draw.rectangle((125, 90, 290, 125), outline = 0)
        draw.text((145,100), event)
        
        #epd.display(epd.getbuffer(drinkInfo))
        #time.sleep(2)

        #Drink Warning
        logging.info("create drink warning")
        drinkWarning=Image.new('1',(50,50),255)
        warningImg=Image.open(os.path.join(picsdir,'warning_2.png'))

        #Over 21
        logging.info("create age")
        createAge=Image.new('1',(50,50),255)
        ageImg=Image.open(os.path.join(picsdir,'21p.png'))

        #QR Code
        logging.info("print QR code")
        createQR = Image.new('1', (110, 110), 255)  # 255: clear the frame
        qrImg = Image.open(os.path.join(picsdir, 'drinkInfo.png'))
        qrImg = qrImg.resize((110,110))

        #Event
        logging.info("create update box")
        createEvent=Image.new('1',(50,50),255)
        eventImg=Image.open(os.path.join(picsdir,'rect.png'))

        #Print onto display
        drinkInfo.paste(qrImg, (2,15))
        if bac>0.08:
            drinkInfo.paste(warningImg, (235,45))
        if licenseAge>21:
            drinkInfo.paste(ageImg, (230, 5))
        #drinkInfo.paste(eventImg, (113, 88))
        epd.display(epd.getbuffer(drinkInfo))
       
        time.sleep(2)

        print("WAITING FOR UPDAATE")
        data = s.recv(1024).decode('utf-8')
        if (data):
            drinkCt = int(data)
            
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd2in9d.epdconfig.module_exit()
    exit()
