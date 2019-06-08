#!/usr/bin/env python3

import tkinter as tk
from tkinter import messagebox
import re
from os import fsync, path
from configparser import ConfigParser
import subprocess

#  Directory Path 
Base_Dir = path.dirname(path.realpath(__file__)) + '/'

class spibox_tk(tk.Tk):
    def __init__(self, parent):
        tk.Tk.__init__(self,parent)
        
        # Gets the requested values of the height and widht.
        windowWidth = self.winfo_reqwidth()
        windowHeight = self.winfo_reqheight()
        print("Width", windowWidth, "Height", windowHeight)
 
        # Gets both half the screen width/height and window width/height
        positionRight = int(self.winfo_screenwidth()/3 - windowWidth/2)
        positionDown = int(self.winfo_screenheight()/2- windowHeight/2)
 
        # Positions the window in the center of the page.
        self.geometry("+{}+{}".format(positionRight, positionDown))
        
        self.parent = parent
        self.resizable(False, False)
        self.initialize()

    def writeSpiBoxConfig(self, recordtime):
        conf = ConfigParser()
        conf.read(Base_Dir + 'Configuration/spibox.conf')
        conf.set('email','emailsubject', self.emailsubject.get())
        conf.set('email','on', self.emailon.get())
        conf.set('email','emailrecipient',self.emailrecipient.get().lower())
        conf.set('email', 'bootstart', self.startatboot.get())
        conf.set('email', 'recordtype', self.recordtype.get())
        conf.set('email', 'recordtime', recordtime)
        with open(Base_Dir + 'Configuration/spibox.conf','w+') as configfile:
            conf.write(configfile)

    def EmailValidator(self, email):
        if len(email) > 0 and '@' in email:
            spl = email.split('@')
            if len(spl) > 0:
                spl2 = spl[1].split('.')
                if len(spl2) > 1:
                    if len(spl2[0]) and len(spl2[1]) > 0:
                        return 1
    
    def SubjectValidator(self, Subject):
        if len(Subject) > 0:
            return 1
        else:
            return 0
        
    def StartService(self):
        #  Add service file systemd
        cmd = "sudo cp {}Configuration/Spi-Box.service /etc/systemd/system".format(Base_Dir)
        subprocess.call(cmd, shell=True)
        
        
        #  Enable Service
        subprocess.call("sudo systemctl enable Spi-Box", shell=True)
        
        #  Daemon Reload 
        cmd = "sudo systemctl daemon-reload".format(Base_Dir)
        subprocess.call(cmd, shell=True)
        
        #  Reload Service service file systemd
        cmd = "sudo systemctl restart Spi-Box".format(Base_Dir)
        subprocess.call(cmd, shell=True)
        
        
    def StopService(self):
        #  stop Service from systemd
        subprocess.call("sudo systemctl stop Spi-Box", shell=True)
        
        #  Disable Service
        subprocess.call("sudo systemctl disable Spi-Box", shell=True)
        
        #  Remove Service from systemd
        cmd = "sudo rm /etc/systemd/system/Spi-Box.service"
        subprocess.call(cmd, shell=True)
        
    
    def writeConfig(self):
        EmailStatus = self.EmailValidator(self.emailrecipient.get())
        SubjectStatus = self.SubjectValidator(self.emailsubject.get())
        try:
            rtime = int(self.recordtime.get())
        except ValueError:
            rtime = 0
        if self.timeunit.get() == 'Min':
            rtime *= 60
            
        TimeValidator = 300 >= rtime >= 1 
        
        if EmailStatus and SubjectStatus and TimeValidator:
            if self.startatboot.get() == 'YES':
                self.StartService()
            elif self.startatboot.get() == 'NO':
                self.StopService()
            self.writeSpiBoxConfig(str(rtime))
            self.quit()
            
        elif not SubjectStatus:
            messagebox.showerror("Incorrect Subject", "Please enter subject for E-mail.")
            
        elif not EmailStatus:
            messagebox.showerror("Email error", "Please enter a valid E-mail.")
        
        elif not TimeValidator:
            messagebox.showerror("Invalid Time", "Please enter Time in range (5 - 300 secs).")

    def testEmail(self):
        EmailStatus = self.EmailValidator(self.emailrecipient.get())
        SubjectStatus = self.SubjectValidator(self.emailsubject.get())
        
        if EmailStatus and SubjectStatus and self.emailon.get() == 'YES':
            cmd = 'mpack -s "{0}" -c image/jpeg {1}capture/test.image {2}'.format(self.emailsubject.get().lower(), Base_Dir, self.emailrecipient.get())
            subprocess.call(cmd, shell = True)
            
        elif not SubjectStatus:
            messagebox.showerror("Incorrect Subject", "Please enter subject for E-mail.")
            
        elif not EmailStatus:
            messagebox.showerror("Email error", "Please enter a valid E-mail.")
        
        elif self.emailon.get() == 'NO':
            messagebox.showinfo("Email Configuration", "Please change 'E-mail configuration' to 'Email On' for sending E-mail.")
        
    def initialize(self):
        self.emailsubject = tk.StringVar()
        self.emailrecipient = tk.StringVar()
        self.emailon = tk.StringVar()
        self.startatboot = tk.StringVar()
        self.recordtype = tk.StringVar()
        self.recordtime = tk.StringVar()
        self.timeunit = tk.StringVar()
        

        def makeentry(parent, caption, rw, **options):
            tk.Label(parent, text=caption).grid(column=0, row=rw, sticky="W", padx = 10)
            entry = tk.Entry(parent, width=30, **options).grid(column=1, row=rw, sticky="EW")
            return entry
           
        def readSpiBoxConfig(self):
           spiboxConf = ConfigParser()
           spiboxConf.read(Base_Dir + 'Configuration/spibox.conf')
           text = spiboxConf.get('email','emailsubject')
           self.emailsubject.set(text)
           text = spiboxConf.get('email','emailrecipient')
           self.emailrecipient.set(text)
           text = spiboxConf.get('email','on')
           self.emailon.set(text)
           text = spiboxConf.get('email','bootstart')
           self.startatboot.set(text)
           text = spiboxConf.get('email','recordtype')
           self.recordtype.set(text)
           text = spiboxConf.get('email','recordtime')
           self.recordtime.set(text)
        
        
        #  Radio Buttons
        self.lbl_email = tk.Label(self,text="Email Notification").grid(row = 1, column = 0, sticky="W", padx = 10)
        self.ent_emailOn = tk.Radiobutton(self, text="Off", variable = self.emailon, width = 20, value = 'NO', anchor='w').grid(row = 1, column = 1)
        self.ent_emailOn = tk.Radiobutton(self, text="On", variable = self.emailon, width = 20, value = 'YES', anchor='w').grid(row = 1, column = 2)
        
        #  Start program at bootup
        self.lbl_email = tk.Label(self, text = "Start at Bootup").grid(row = 2, column = 0, sticky="W", padx = 10)
        self.ent_startatboot = tk.Radiobutton(self, text = "Yes", variable = self.startatboot, width = 20, value = 'YES', anchor = 'w').grid(row = 2, column = 1)
        self.ent_startatboot = tk.Radiobutton(self, text = "No", variable = self.startatboot, width = 20, value = 'NO', anchor='w').grid(row = 2, column = 2)
        
        
        #  Recording Time in secs
        self.lbl_email = tk.Label(self, text = "Record Time", anchor = 'e').grid(row = 4, column = 1, sticky = "E", padx = 10)
        self.ent_recordtime = tk.Entry(self, width = 10, textvariable = self.recordtime).grid(column = 2, row = 4, padx = 5, sticky = "W")
        
        #  Recording Type (Image or Video)
        self.lbl_email = tk.Label(self, text = "Record Type", anchor = 'e').grid(row = 3, column = 0, sticky="W", padx = 10)
        self.ent_recordtype = tk.Radiobutton(self, text = "Image", variable = self.recordtype, width = 20, value = 'IMG', anchor='w').grid(row = 3, column = 1)
        self.ent_recordtype = tk.Radiobutton(self, text = "Video", variable = self.recordtype, width = 20, value = 'VID', anchor='w').grid(row = 3, column = 2)
            
        #  Record Time unit
        self.timeunit.set('Sec')
        tk.OptionMenu(self, self.timeunit, 'Sec', 'Min').grid(row = 4, column = 2, sticky = 'E', padx = 10)
        
        
        #  Email Subject
        self.ent_emailsubject = makeentry(self, "Email Subject", 5, textvariable = self.emailsubject)
        
        #  Recipient's Email
        self.ent_emailrecipient = makeentry(self, "Email Recipient", 6, textvariable = self.emailrecipient)
        
        #  Test Email
        btTestEmail = tk.Button(self, text = "Test Email", command = lambda: spibox_tk.testEmail(self), activebackground = 'DARKGREY')
        btTestEmail.grid(column=1, row=7, pady = 10, stick = 'W')
        
        #  Save Data and Quit
        self.bt_saveAndClose = tk.Button(self,text="Save and Quit", command = lambda: spibox_tk.writeConfig(self), activebackground = 'DARKGREY')
        self.bt_saveAndClose.grid(column=2, row=7, pady = 10, stick = 'W')

        #self.grid()
        readSpiBoxConfig(self)


if __name__ == "__main__":
    app = spibox_tk(None)
    app.title('Spi-Box Setup')
    Image = tk.PhotoImage(file = Base_Dir + 'icons/SPI-BOXLogo.png')
    app.tk.call('wm', 'iconphoto', app._w, Image)
    app.mainloop()

