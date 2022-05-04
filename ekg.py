from asyncore import read
from datetime import datetime
import serial
import time
import os
import pandas as pd
import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from drawnow import *

def handleSerial():
    # change '/dev/cu.usbmodel1301' to whichever usb port is being
    # used, this can be found in arduino IDE
    arduino = serial.Serial('/dev/ttyACM0', 9600) 
    amount = 'a'
    while isinstance(amount, float) == False:
        try:
            min = float(input('Time to record in seconds: '))

            amount = min
        except:
            min = input('Re-enter the time to record ')

    print('Starting')

    plt.ion() # interactive mode to plot in real ti

    # Function to plot in real time.
    def grafRT(): 
        plt.ylim(100,650) # Limits of y-axis
        plt.xticks(0,amount)
        plt.plot(data) # graph ecg, array data data.
        plt.xlabel('time (milliseconds)')
        plt.ylabel('voltage (mV)')
        plt.title('Electrocardiogram')
        plt.ticklabel_format(useOffset=False) #do not autoscale the Y axis.

    # Fix for saving the data obtained from the sensor.
    data = []
    
    t_end = time.time() + amount
    while time.time() < t_end:
        try:
            info = arduino.readline()
            data.append(float(info))

            # drawnow(grafRT)                       
            # plt.pause(.00000001)

        except ValueError:
#            print("Problem capturing data", end='\n')
#            guardar = input('You want to save the data: y = yes, n = no: ')

#            if save.lower() == 'y':
             ecg_data = pd.DataFrame(data=data) # save data into PD dataframe
             name = input("file name: ")
             archive = name + ".csv"
             ecg_data.to_csv(archive) # write data to csv
            
              

            
    print('Captured data ', end='\n')

    ecg_data = pd.DataFrame(data=data)
    name = input("file name: ")
    archive = name + ".csv"
    ecg_data.to_csv(archive)


    data = pd.read_csv(archive,delimiter=",")

    ecg_data = data.iloc[:, 1].values

    peaks, _ = find_peaks(ecg_data, distance=150)
    distances = np.diff(peaks)

    #print(peaks.size, end='\n')
    #print(distances.size)

    media = np.mean(distances)
    #print(type(media))

    bpm = (ecg_data.size/media)/(ecg_data.size/15000)

    print(f'Recorded {int(bpm)} beats per minute.')

    fig1 = plt.figure(1)
    plt.plot(ecg_data, 'b')
    plt.plot(peaks, ecg_data[peaks], 'rx')

    fig2 = plt.figure(2)
    plt.hist(distances)
    plt.xlabel('distance (samples)')
    plt.ylabel('frequency')
    plt.title('Distance distribution between local maxima (peaks)')
    plt.show()

    fig1.savefig(name + "ecg.png")
    ecgpng = name + "ecg.png"
    fig2.savefig(name + "dist.png")
    bpm = ("Your recorded BPM is {}").format(round(bpm))   
    return (bpm, ecgpng)

def send_email(recipient, ecgbpm, ecgpng):
    port = 587
    smtp_server = "smtp.gmail.com"
    sender_email = "ecgproject578@gmail.com"
    password = "578wireless$$"
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient
    msg['Subject'] = "Your ECG Results"
    msg.attach(MIMEText(ecgbpm, 'plain'))
    body = "Link: http://127.0.0.1:5000"
    body = MIMEText(body)
    msg.attach(body)
    img_data = open(ecgpng, 'rb')
    image = MIMEImage(img_data.read(), name=os.path.basename(ecgpng))
    msg.attach(image)

    context = ssl.create_default_context()
    try:
        smtp_server = smtplib.SMTP(smtp_server, port)
        smtp_server.starttls(context=context)
        smtp_server.login(sender_email, password)
        smtp_server.sendmail( sender_email, recipient, msg.as_string())
    except Exception as e:
        print(e)
    finally:
        smtp_server.quit()

user_name = input("Enter user name: ")
recipient = input('Enter recipient email: ')
ecgbpm, ecgpng_name = handleSerial()
send_email(recipient, ecgbpm, ecgpng_name)
   
