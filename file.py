import serial
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from drawnow import *

def main():

    arduino = serial.Serial('com4', 9600) 
    cantidad = 'a'

    while isinstance(cantidad, float) == False:
        try:
            min = float(input('Time to record '))

            cantidad = min*60*250 
        except:
            min = input('Re-enter the time to record ')

    print('Starting')

    plt.ion() # modo interactivo para plotear en tiempo real.

    # Function to plot in real time.
    def grafRT(): 
        plt.ylim(100,650) # Limits of y-axis
        plt.plot(data) # graph ecg, array data data.
        plt.xlabel('time (milliseconds)')
        plt.ylabel('voltage (mV)')
        plt.title('Electrocardiogram')
        plt.ticklabel_format(useOffset=False) #do not autoscale the Y axis.

    # Fix for saving the data obtained from the sensor.
    data = []
    

    while len(data) < cantidad:
        try:
            info = arduino.readline()
            data.append(float(info))

            drawnow(grafRT)                       
            plt.pause(.00000001)

        except ValueError:
            print("Problem capturing data", end='\n')
            guardar = input('You want to save the data: y = yes, n = no: ')

            if guardar.lower() == 's':
                ecg_data = pd.DataFrame(data=data) #Guardar datos en un dataframe de pandas.
                name = input("file name: ")
                archivo = name + ".csv"
                ecg_data.to_csv(archivo) # Generar un archivo csv con los datos del ECG.
            else:
                pass

            
    print('Captured data ', end='\n')

    # Analizar datos adquiridos con el sensor.
    ecg_data = pd.DataFrame(data=data)
    name = input("file name: ")
    archive = name + ".csv"
    ecg_data.to_csv(archive)


    data = pd.read_csv(archivo,delimiter=",")

    ecg_data = data.iloc[:, 1].values 

    # Detección de picos R en la señal de ECG.
    peaks, _ = find_peaks(ecg_data, distance=150)
    distances = np.diff(peaks)

    #print(peaks.size, end='\n')
    #print(distances.size)

    media = np.mean(distances)
    #print(type(media))

    # Calcular y mostrar los latidos por minuto (BPM).
    bpm = (ecg_data.size/media)/(ecg_data.size/15000)

    print('Recorded {} beats per minute.'.format(round(bpm)))

    fig1 = plt.figure(1)
    plt.plot(ecg_data, 'b')
    plt.plot(peaks, ecg_data[peaks], 'rx')

    fig2 = plt.figure(2)
    plt.hist(distances)
    plt.xlabel('distance (samples)')
    plt.ylabel('frequency')
    plt.title('Distance distribution between local maxima (peaks)')
    plt.show()


    save = input('Save images = yes, dont save = n:')

    if save.lower() ==  's':
        fig1.savefig(name + "ecg.png")
        fig2.savefig(name + "dist.png")
    else:
        pass

if __name__ == '__main__':
  main()