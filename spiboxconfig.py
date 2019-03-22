import Tkinter
import re
from os import fsync
import ConfigParser
import subprocess

class spibox_tk(Tkinter.Tk):
    def __init__(self,parent):
        Tkinter.Tk.__init__(self,parent)
        self.parent = parent
        self.initialize()

    def writeSpiBoxConfig(self):
        conf = ConfigParser.ConfigParser()
        conf.read('/home/pi/Spi-Box/spibox.conf')
        conf.set('email','emailsubject',self.emailsubject.get())
        conf.set('email','on',self.emailon.get())
        conf.set('email','emailrecipient',self.emailrecipient.get())
        with open('/home/pi/Spi-Box/spibox.conf','wb') as configfile:
            conf.write(configfile)

    def writeConfig(self):
        self.writeSpiBoxConfig()
        self.quit()

    def testEmail(self):
        subprocess.call(['mpack','-s',self.emailsubject.get(),'-c','image/jpeg','/home/pi/Spi-Box/capture/test.image',self.emailrecipient.get()])

    def initialize(self):
        self.emailsubject = Tkinter.StringVar()
        self.emailrecipient = Tkinter.StringVar()
        self.emailon = Tkinter.StringVar()

        def makeentry(parent, caption, rw, **options):
            Tkinter.Label(parent, text=caption).grid(column=0,row=rw,sticky="EW")
            entry = Tkinter.Entry(parent, width=40, **options).grid(column=1, row=rw, sticky="EW")
            return entry

        def makeradiobutton(parent, caption, rw, col, **options):
           if col == 1:
               Tkinter.Label(parent, text=caption).grid(column=0,row=rw, sticky="EW")
           button = Tkinter.Radiobutton(parent, **options).grid(column=col, row=rw, sticky="EW")
        
        def readSpiBoxConfig(self):
           spiboxConf = ConfigParser.ConfigParser()
           spiboxConf.read('/home/pi/Spi-Box/spibox.conf')
           text = spiboxConf.get('email','emailsubject')
           self.emailsubject.set(text)
           text = spiboxConf.get('email','emailrecipient')
           self.emailrecipient.set(text)
           text = spiboxConf.get('email','on')
           self.emailon.set(text)

        self.grid()

        self.lbl_email = Tkinter.Label(self,text="Email Configuration")
        self.lbl_email.grid(column=1,row=0,sticky='EW')
        
        self.ent_emailOn = makeradiobutton(self, "Email configuration", 1, 1, text="Email Off", variable=self.emailon, value = 'NO')
        self.ent_emailOn = makeradiobutton(self, "Email configuration", 1, 2, text="Email On", variable=self.emailon, value = 'YES')
        self.ent_emailsubject = makeentry(self, "Email subject", 2, textvariable=self.emailsubject)
        self.ent_emailrecipient = makeentry(self, "Email recipient", 3, textvariable=self.emailrecipient)
        
        btTestEmail = Tkinter.Button(self,text="Test Email", command= lambda: spibox_tk.testEmail(self))
        btTestEmail.grid(column=1,row=16)

        self.bt_saveAndClose = Tkinter.Button(self,text="Save and Quit", command=lambda: spibox_tk.writeConfig(self))
        self.bt_saveAndClose.grid(column=1,row=26)

        readSpiBoxConfig(self)

if __name__ == "__main__":
    app = spibox_tk(None)
    app.title('SPi-Box Setup')
    app.mainloop()
