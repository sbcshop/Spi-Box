import time
import datetime
import subprocess
import os
import ConfigParser
import RPi.GPIO as GPIO

PIR = 4

def get_file_name():
    return datetime.datetime.now().strftime("%Y-%m-%d_%H.%M.%S")

def photo():
    for i in range(1,2):
        capturename = get_file_name()
        print('Motion detected! Taking snapshot')
        cmd="raspistill -w 640 -h 480 -n -t 10 -q 10 -e jpg -th none -o /home/pi/Spi-Box/capture/" + capturename+"_%d.jpg" % (i)
        camerapid = subprocess.call(cmd,shell=True)

class spiboxMessenger:
    def init(self):
        spiboxConf = ConfigParser.ConfigParser()
        spiboxConf.read('/home/pi/Spi-Box/spibox.conf')
        self.emailsubject = spiboxConf.get('email','emailsubject')
        self.emailrecipient = spiboxConf.get('email','emailrecipient')
        self.emailon = spiboxConf.get('email','on')

    def getFileList(self):
       self.filelist = []
       i = 0
       for file in os.listdir("/home/pi/Spi-Box/capture"):
          if file.endswith(".jpg"):
             self.filelist.extend([None])
             self.filelist[i] = file
             i = i+1

    def moveFiles(self):
        for filename in self.filelist:
            print('moving'+filename)
            pid = subprocess.call(['sudo','mv','/home/pi/Spi-Box/capture/'+filename,'/home/pi/Spi-Box/capture/archive/'])

    def emailFiles(self):
        print(len(self.filelist))
        for filename in self.filelist:
            print('emailing'+filename)
            cmd = 'mpack -s "'+self.emailsubject+'" -c image/jpeg /home/pi/Spi-Box/capture/'+filename + ' '+self.emailrecipient
            pid = subprocess.call(cmd, shell=True)


GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR, GPIO.IN, GPIO.PUD_DOWN)
messenger = spiboxMessenger()
messenger.init()


try:
    print "Turning on motion sensor..."
 
    # Loop until PIR indicates nothing is happening
    while GPIO.input(PIR)==1:
        Current_State  = 0
 
    print "  Sensor ready"
 
    while True:
        print('Waiting for movement')
        GPIO.wait_for_edge(PIR,GPIO.RISING)
        photo()
        messenger.getFileList()
        if messenger.emailon == "YES":
            messenger.emailFiles()
        messenger.moveFiles()

        

except KeyboardInterrupt:
  print "  Bye for now"
  # Reset GPIO
  GPIO.cleanup()

