import PIL
import cv2
import numpy as np
import sys
import os
import time
import imutils
from pyzbar import pyzbar
from picamera import PiCamera
from imutils.video import VideoStream
from gpiozero import PWMLED
import socket


def main():
    speaker = PWMLED("BOARD40")
    speaker.value = 0.5
    time.sleep(0.25)
    speaker.value = 0
    userList = {}
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverAddress = ("",2222)
    s.bind(serverAddress)
    print("WAITING FOR CONNECTION")
    s.listen(1)
    connection, client_address = s.accept()
    print("CONNECTED TO DEVICE")
    connection.sendall("HERE's A MESSAGE".encode('utf-8'))

    
    vs = VideoStream(usePiCamera=True).start()
    

    print("Instantiated QR Camera")
    while True:
    #1. Read from camera every 2 seconds and see if qr-code present
        try:
            frame = vs.read()
            frame = imutils.resize(frame, width=400)
            cv2.imshow("GLIDERZ DRINK MANAGER", frame)
            
            qrcodes = pyzbar.decode(frame)
            for qrcode in qrcodes:
                data = qrcode.data.decode('utf-8')
                print("Scanned Data: " + str(data))
                speaker.value = 0.5
                #os.system("omxplayer -o local gumbuttons.wav")
                time.sleep(0.2)
                speaker.value = 0
                
                splitData = data.split(",")
                name = splitData[0]
                if (name in userList.keys()):
                    userList[name] += 1;
                else:
                    userList[name] = 0
                connection.sendall(str(userList[name]).encode('utf-8'))
                time.sleep(2)
            cv2.waitKey(1)
        except Exception as e:
            print("NO PY CAMERA FOUND: " + str(e))
            connection.close()
            break
        
while True:
    main()