# Spi-Box
Motion Activated Security Camera based on raspberry pi.

<img src="https://cdn.shopify.com/s/files/1/1217/2104/products/SKU03273_1800x1800.jpg?v=1558360585" width="300">

**Steps for PiTalk software installation -** 

1. Open Terminal and download the code by writing: 
   ```
   git clone https://github.com/sbcshop/Spi-Box.git
   ```
   
2. Your code will be downloaded to '/home/pi' directory. You can use 'ls' command to check the list of directories.

3. Go to 'Spi-Box' directory. Move 'SPi-Box' and 'SPi-Box Config' (shortcut icon) to Desktop

4. Install 'SSMTP' (SSMTP is for mail configuration) and 'MPACK' (MPACK is used for sending attachements) using commands:
   ```
   sudo apt-get install ssmtp
   sudo apt-get install mpack
   ```   
   
5. Install MP4Box with:
     ```
     sudo apt-get install -y gpac
     ```

   
6. Edit SSMTP configuration file:
   ```
   sudo nano /etc/ssmtp/ssmtp.conf
   ```
   
   Add the following configuration and save it;
   ```
   root=postmaster
   mailhub=smtp.gmail.com:465
   hostname=raspberrypi
   AuthUser=user_name@gmail.com
   AuthPass=user_password
   FromLineOverride=YES
   UseTLS=YES
   ```

7. Send a test mail using command:
   ```
   mpack -s "subject" file_path recipient@gmail.com
   ```
   Example:
   ```
   mpack -s "test mail" /home/pi/image.png abc@gmail.com
   ```
   
8. Google will block your sign-in attempts. Check your mail Inbox and allow to less securing apps so that Raspberry can send Emails

9. Repeat Step 6 for sending a test mail

10. Double Click on 'SPi-Box Config' icon placed on desktop, and configure it:
   - Tick on "turn on email"
   - Enter the subject
   - Enter the email recipient address
   - Click on "Test Email" for checking configuration is correct
   - Press "save and quit"
   
11. Connect the Camera with Raspberry pi and PIR sensor output to 'GPIO 4' i.e. Pin 7 of Raspberry Pi

12. Enable Camera in Raspberry Pi Configuration and Restart the Raspberry Pi

13. Double Click on "SPi-Box" icon on Desktop, to run the script and if motion is dectected it will click and image and email it

