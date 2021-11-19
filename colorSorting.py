from __future__ import print_function
from time import sleep
from picamera import PiCamera #IMPORTI POTREBNI KAMERI DA USLIKA SLIKU

import RPi.GPIO as GPIO
import time #IMPORTI ZA MOTOR


import binascii
import struct
from PIL import Image
import numpy as np
import scipy
import scipy.misc
import scipy.cluster #IMPORTI POTREBNI DA SE PRONADJE DOMINANTNA BOJA

#POCETNE TRI BOJE (SVE POSTAVIMO NA NULA)
#rgb prve boje
r1 = 0
g1 = 0
b1 = 0
#rgb druge boje
r2 = 0
g2 = 0
b2 = 0
#rgb trece boje
r3 = 0
g3 = 0
b3 = 0

#POZICIJA DRUGOG MOTORA (ON IMA 3 POZICIJE - 3 KUTIJICE ZA BOBE)
pozicija = 1

#VARIJABLE ZA MOTOR
 
delay = 0.0055
 
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
 
#PINOVI ZA UPRAVLJANJE MOTORA 1
 
coil_A_1_pin = 18
coil_A_2_pin = 23
coil_B_1_pin = 24
coil_B_2_pin = 25

#***********************************************
#PINOVI ZA UPRAVLJANJE MOTORA 2
faza1 = 4
faza2 = 17
faza3 = 27
faza4 = 22

#POSTAVLJANJE PINOVA MOTORA 2 KAO IZLAZNI
GPIO.setup(faza1, GPIO.OUT)
GPIO.setup(faza2, GPIO.OUT)
GPIO.setup(faza3, GPIO.OUT)
GPIO.setup(faza4, GPIO.OUT)

#FUNKCIJA MOTORA 2
def setStep2(w1, w2, w3, w4):
  GPIO.output(faza1, w1)
  GPIO.output(faza2, w2)
  GPIO.output(faza3, w3)
  GPIO.output(faza4, w4)

#*******************************************************************
  
setStep2(0,0,0,0)

#POSTAVLJANJE PINOVA MOTORA 1 KAO IZLAZNI
GPIO.setup(coil_A_1_pin, GPIO.OUT)
GPIO.setup(coil_A_2_pin, GPIO.OUT)
GPIO.setup(coil_B_1_pin, GPIO.OUT)
GPIO.setup(coil_B_2_pin, GPIO.OUT)
 
 
#FUNKCIJA ZA MOTOR 1
def setStep(w1, w2, w3, w4):
  GPIO.output(coil_A_1_pin, w1)
  GPIO.output(coil_A_2_pin, w2)
  GPIO.output(coil_B_1_pin, w3)
  GPIO.output(coil_B_2_pin, w4)

#SVE PINOVE MOTORA 1 VRATI NA LOW
setStep(0,0,0,0)




for k in range(0,10):


    #MOTOR 1 DOVODI BOBU SA POCETNE TACKE DO KAMERE 
    for i in range(0, 12): #UNAPRIJED
        setStep(1,0,1,0)
        time.sleep(delay)
        setStep(0,1,1,0)
        time.sleep(delay)
        setStep(0,1,0,1)
        time.sleep(delay)
        setStep(1,0,0,1)
        time.sleep(delay)

    #SVE PINOVE MOTORA 1 VRATI NA LOW
    setStep(0,0,0,0)

    #KAMERA SLIKA BOBU
    camera = PiCamera()
    camera.resolution = (1024, 768)
    camera.start_preview()
    sleep(2)
    camera.capture('slika.jpg')
    camera.close()

    #ANALIZIRA SE SLIKA, I DOMINANTNA BOJA SE STAVI U VARIJABLU PEAK
    NUM_CLUSTERS = 5
    print('reading image')
    im = Image.open('slika.jpg')
    im = im.resize((150, 150))      
    ar = np.asarray(im)
    shape = ar.shape
    ar = ar.reshape(scipy.product(shape[:2]), shape[2]).astype(float)
    print('finding clusters')
    codes, dist = scipy.cluster.vq.kmeans(ar, NUM_CLUSTERS)
    print('cluster centres:\n', codes)
    vecs, dist = scipy.cluster.vq.vq(ar, codes)
    counts, bins = scipy.histogram(vecs, len(codes))
    index_max = scipy.argmax(counts)
    peak = codes[index_max]
    colour = binascii.hexlify(bytearray(int(c) for c in peak)).decode('ascii')
    print('most frequent is %s (#%s)' % (peak, colour))

    #RGB KOMPONENTE VARIJABLE PEAK
    rp=int(peak[0])
    gp=int(peak[1])
    bp=int(peak[2])

    nasao_boju1=False
    nasao_boju2=False
    nasao_boju3=False

    #*******UPOREDJIVANJE PRONADJENE BOJE SA 3 BOJE********

    #UPOREDJIVANJE SA PRVOM BOJOM
    if (rp-r1) == rp: #ovo znaci da je peak prva boja koja se pojavila, jer je r1 == 0
        r1 = rp
        g1 = gp #sada je boja1 jednaka ovoj prvoj pronadjenoj boji
        b1 = bp
        nasao_boju1=True
    #UPOREDJIVANJE SA DRUGOM BOJOM
    elif (rp-r2) == rp: #ovo znaci da je peak prva boja koja se pojavila, jer je r2 == 0
        r2 = rp
        g2 = gp #sada je boja2 jednaka ovoj pronadjenoj boji
        b2 = bp
        nasao_boju2=True
    #UPOREDJIVANJE SA TRECOM BOJOM
    elif (rp-r3) == rp: #ovo znaci da je peak prva boja koja se pojavila, jer je r3 == 0
        r3 = rp
        g3 = gp #sada je boja3 jednaka ovoj pronadjenoj boji
        b3 = bp
        nasao_boju3=True

    if ((((abs(rp-r1)) <= 15) and ((abs(gp-g1)) <= 15) and ((abs(bp-b1)) <= 15)) or nasao_boju1==True): #ako su priblizno jednake, odstupanje npr manje od 15 ILI ako je ovo prva boja
        nasao_boju1=False
        #BOBA IDE U PRVU KUTIJU
        if pozicija == 1:
        #MOTOR 1 dovede bobu do tobogana
            for i in range(0, 13): #UNAPRIJED
                setStep(1,0,1,0)
                time.sleep(delay)
                setStep(0,1,1,0)
                time.sleep(delay)
                setStep(0,1,0,1)
                time.sleep(delay)
                setStep(1,0,0,1)
                time.sleep(delay)
            #SVE PINOVE MOTORA 1 VRATI NA LOW
            setStep(0,0,0,0)  
                
        if pozicija == 2:
        #MOTOR 2 SE IZ POZICIJE 2 VRACA JEDNOM UNAZAD DA DODJE U POZICIJU 1
            for i in range(0, 3): #nazad
                setStep2(1,0,1,0)
                time.sleep(delay)
                setStep2(0,1,1,0)
                time.sleep(delay)
                setStep2(0,1,0,1)
                time.sleep(delay)
                setStep2(1,0,0,1)
                time.sleep(delay)
            #SVE PINOVE MOTORA 2 VRATI NA LOW
            setStep2(0,0,0,0)
            #motor 1 dovede bobu do tobogana
            for i in range(0, 13):
                setStep(1,0,1,0) #UNAPRIJED
                time.sleep(delay)
                setStep(0,1,1,0)
                time.sleep(delay)
                setStep(0,1,0,1)
                time.sleep(delay)
                setStep(1,0,0,1)
                time.sleep(delay)
            #SVE PINOVE MOTORA 1 VRATI NA LOW
            setStep(0,0,0,0)
            pozicija = 1
        
        if pozicija == 3:
        #MOTOR 2 SE IZ POZICIJE 3 VRACA DVA PUTA UNAZAD DA DODJE U POZICIJU 1
            for i in range(0, 6): #nazad
                setStep2(1,0,1,0)
                time.sleep(delay)
                setStep2(0,1,1,0)
                time.sleep(delay)
                setStep2(0,1,0,1)
                time.sleep(delay)
                setStep2(1,0,0,1)
                time.sleep(delay)
            #SVE PINOVE MOTORA 2 VRATI NA LOW
            setStep2(0,0,0,0)
        #motor 1 dovede bobu do tobogana
            for i in range(0, 13):
                setStep(1,0,1,0)
                time.sleep(delay)
                setStep(0,1,1,0)
                time.sleep(delay)
                setStep(0,1,0,1)
                time.sleep(delay)
                setStep(1,0,0,1)
                time.sleep(delay)
            #SVE PINOVE MOTORA 1 VRATI NA LOW
            setStep(0,0,0,0)
            pozicija = 1
            






    elif ((((abs(rp-r2)) <= 15) and ((abs(gp-g2)) <= 15) and ((abs(bp-b2)) <= 15)) or nasao_boju2==True): #ako su priblizno jednake, odstupanje npr manje od 15
        nasao_boju2==False
        #BOBA IDE U DRUGU KUTIJU
        if pozicija == 2:
        #MOTOR 1 DOVEDE BOBU DO TOBOGANA
            for i in range(0, 13): #UNAPRIJED
                setStep(1,0,1,0)
                time.sleep(delay)
                setStep(0,1,1,0)
                time.sleep(delay)
                setStep(0,1,0,1)
                time.sleep(delay)
                setStep(1,0,0,1)
                time.sleep(delay)
            #SVE PINOVE MOTORA 1 VRATI NA LOW
            setStep(0,0,0,0)
                
        if pozicija == 1:
        #MOTOR 2 IDE JEDNOM NAPRIJED DA IZ POZICIJE 1 DODJE U POZICIJU 2
            for i in range(0, 3): 
                setStep2(1,0,0,1) #naprijed
                time.sleep(delay)
                setStep2(0,1,0,1)
                time.sleep(delay)
                setStep2(0,1,1,0)
                time.sleep(delay)
                setStep2(1,0,1,0)
                time.sleep(delay)
            #SVE PINOVE MOTORA 2 VRATI NA LOW
            setStep2(0,0,0,0)
        #motor 1 dovede bobu do tobogana
            for i in range(0, 13):
                setStep(1,0,1,0)
                time.sleep(delay)
                setStep(0,1,1,0)
                time.sleep(delay)
                setStep(0,1,0,1)
                time.sleep(delay)
                setStep(1,0,0,1)
                time.sleep(delay)
            #SVE PINOVE MOTORA 1 VRATI NA LOW
            setStep(0,0,0,0)
            pozicija = 2
        
        if pozicija == 3:
        #MOTOR 2 IDE JEDNOM UNAZAD DA IZ POZICIJE 3 DODJE U POZICIJU 2 
            for i in range(0, 3): #nazad
                setStep2(1,0,1,0)
                time.sleep(delay)
                setStep2(0,1,1,0)
                time.sleep(delay)
                setStep2(0,1,0,1)
                time.sleep(delay)
                setStep2(1,0,0,1)
                time.sleep(delay)
            #SVE PINOVE MOTORA 2 VRATI NA LOW
            setStep2(0,0,0,0)
        #motor 1 dovede bobu do tobogana
            for i in range(0, 13):
                setStep(1,0,1,0)
                time.sleep(delay)
                setStep(0,1,1,0)
                time.sleep(delay)
                setStep(0,1,0,1)
                time.sleep(delay)
                setStep(1,0,0,1)
                time.sleep(delay)
            #SVE PINOVE MOTORA 1 VRATI NA LOW
            setStep(0,0,0,0)
            pozicija = 2







    elif ((((abs(rp-r3)) <= 15) and ((abs(gp-g3)) <= 15) and ((abs(bp-b3)) <= 15)) or nasao_boju3==True): #ako su priblizno jednake, odstupanje npr manje od 15
        nasao_boju3==False
        #BOBA IDE U TRECU KUTIJU
        if pozicija == 3:
        #prvi motor bobu dovede do tobogana
            for i in range(0, 13): #UNAPRIJED
                setStep(1,0,1,0)
                time.sleep(delay)
                setStep(0,1,1,0)
                time.sleep(delay)
                setStep(0,1,0,1)
                time.sleep(delay)
                setStep(1,0,0,1)
                time.sleep(delay)
            #SVE PINOVE MOTORA 1 VRATI NA LOW
            setStep(0,0,0,0)
                
        if pozicija == 1:
        #motor 2 ide dva puta naprijed
            for i in range(0, 6): 
                setStep2(1,0,0,1) #naprijed
                time.sleep(delay)
                setStep2(0,1,0,1)
                time.sleep(delay)
                setStep2(0,1,1,0)
                time.sleep(delay)
                setStep2(1,0,1,0)
                time.sleep(delay)
            #SVE PINOVE MOTORA 2 VRATI NA LOW
            setStep2(0,0,0,0)
        #motor 1 dovede bobu do tobogana
            for i in range(0, 13): #UNAPRIJED
                setStep(1,0,1,0)
                time.sleep(delay)
                setStep(0,1,1,0)
                time.sleep(delay)
                setStep(0,1,0,1)
                time.sleep(delay)
                setStep(1,0,0,1)
                time.sleep(delay)
            #SVE PINOVE MOTORA 1 VRATI NA LOW
            setStep(0,0,0,0)
            pozicija = 3
        
        if pozicija == 2:
        #motor 2 ide jednom naprijed
            for i in range(0, 3): 
                setStep2(1,0,0,1) #naprijed
                time.sleep(delay)
                setStep2(0,1,0,1)
                time.sleep(delay)
                setStep2(0,1,1,0)
                time.sleep(delay)
                setStep2(1,0,1,0)
                time.sleep(delay)
            #SVE PINOVE MOTORA 2 VRATI NA LOW
            setStep2(0,0,0,0)
        #motor 1 dovede bobu do tobogana
            for i in range(0, 13):
                setStep(1,0,1,0)
                time.sleep(delay)
                setStep(0,1,1,0)
                time.sleep(delay)
                setStep(0,1,0,1)
                time.sleep(delay)
                setStep(1,0,0,1)
                time.sleep(delay)
            #SVE PINOVE MOTORA 1 VRATI NA LOW
            setStep(0,0,0,0)
            pozicija = 3

    else:
        print('greska')
    #motor 1 vratiti gdje je bio, da ode po drugu bobu
    for i in range(0, 25):
        setStep(1,0,0,1) #UNAZAD
        time.sleep(delay)
        setStep(0,1,0,1)
        time.sleep(delay)
        setStep(0,1,1,0)
        time.sleep(delay)
        setStep(1,0,1,0)
        time.sleep(delay)
    #SVE PINOVE MOTORA 1 VRATI NA LOW
    setStep(0,0,0,0)