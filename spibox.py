#!/usr/bin/env python3

import time
import datetime
import subprocess
import os
from configparser import ConfigParser
import RPi.GPIO as GPIO

PIR = 4

#  Directory Path
Base_Dir = os.path.dirname(os.path.realpath(__file__)) + '/'


def get_file_name():
    return datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

def photo():
    capturename = get_file_name()
    print('Motion detected! Taking snapshot')
    cmd = "raspistill -w 640 -h 480 -n -t 10 -q 10 -e jpg -th none -o {}capture/{}.jpg".format(Base_Dir, capturename)
    camerapid = subprocess.call(cmd, shell=True)
    
    
def video(RecordTime):
    capturename = get_file_name()
    print('Motion detected! Taking Video')
    # User can change video time in milliseconds. Ex- 5000 is 5 sec
    cmd="raspivid -o {}capture/{}.h264 -t {}".format(Base_Dir, capturename, RecordTime)
    camerapid = subprocess.call(cmd,shell=True)
        
    #  Change raw video to mp4
    cmd="MP4Box -add {0}capture/{1}.h264 {0}capture/{1}.mp4".format(Base_Dir, capturename)
    camerapid = subprocess.call(cmd,shell=True)
        
    #  Remove raw file
    cmd="sudo rm {}capture/{}.h264".format(Base_Dir, capturename)
    camerapid = subprocess.call(cmd,shell=True)
        
        
class spiboxMessenger:
    def init(self):
        spiboxConf = ConfigParser()
        spiboxConf.read(Base_Dir + 'Configuration/spibox.conf')
        self.emailsubject = spiboxConf.get('email','emailsubject')
        self.emailrecipient = spiboxConf.get('email','emailrecipient')
        self.emailon = spiboxConf.get('email','on')
        self.recordtype = spiboxConf.get('email','recordtype')
        self.recordtime = int(spiboxConf.get('email','recordtime'))

    def getFileList(self):
       self.filelist = []
       i = 0
       for file in os.listdir(Base_Dir + "capture"):
          if file.endswith('.jpg') or file.endswith('.mp4'):
             self.filelist.extend([None])
             self.filelist[i] = file
             i = i+1

    def moveFiles(self):
        for filename in self.filelist:
            print('moving ' + filename + ' to archive')
            pid = subprocess.call(['sudo','mv', Base_Dir + 'capture/' + filename, Base_Dir + 'capture/archive/'])

    def emailFiles(self):
        print(len(self.filelist))
        if self.emailon == 'YES':
            for filename in self.filelist:
                print('emailing ' + filename)
                cmd = 'mpack -s "{0}" {1}capture/{2} {3}'.format(self.emailsubject, Base_Dir, filename, self.emailrecipient)
                pid = subprocess.call(cmd, shell=True)


if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PIR, GPIO.IN, GPIO.PUD_DOWN)
    messenger = spiboxMessenger()
    messenger.init()
    try:
        print("Turning on motion sensor...")
 
        # Loop until PIR indicates nothing is happening
        while GPIO.input(PIR)==1:
            Current_State  = 0
 
        print("  Sensor ready")
 
        while True:
            print('Waiting for movement')
            GPIO.wait_for_edge(PIR,GPIO.RISING)
            
            if messenger.recordtype == 'IMG':
                photo()
            elif messenger.recordtype == 'VID':
                video(RecordTime = messenger.recordtime * 1000)
                
            messenger.getFileList()
            messenger.emailFiles()
            messenger.moveFiles()

    except KeyboardInterrupt:
      print("  Bye for now")
      # Reset GPIO
      GPIO.cleanup()




