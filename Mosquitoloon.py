#!/usr/bin/env python
# coding: utf-8

################################################################################
# A) Import the librairies needed to execute the script
################################################################################


#Activate pinout to control the LEDs and the RELAY
from gpiozero import LED
from gpiozero import Servo

#Allow to access the I2C BUS from the Raspberry Pi
import smbus

#Time librairy in order to sleep when need
from time import sleep

#Picamera library to take images
from picamera import PiCamera

#Enable calculation of remaining duration and datetime
from datetime import datetime, timedelta

#Enable creation of new folders
import os


################################################################################
# C) Configuration file
################################################################################

led = LED(18)
camera = PiCamera()

camera.resolution = (640, 480)
camera.iso = 60

nb_frame=300

duration_loading=120 #(sec)
duration_flushing=20 #(sec)
duration_aeration=30 #(sec)
CLIP_DURATION = 10


################################################################################
# E) Define simple functions making the whole sequence
################################################################################

#function takes a video for CLIP_DURATION seconds and saves it with name number in Mosquitoloon folder
def record(camera, filename):
    camera.start_recording(filename)
    camera.wait_recording(CLIP_DURATION)
    camera.stop_recording()
#First function to run in order to turn on the blue LED as well as the relay to make the I2C operationnal
def start():
    
    print("###############") 
    print("STARTING")
    print("###############")
    
    #Inform on the statut of the operation
    print("Starting : engaged")
    
    directory="/home/pi/Desktop/Mosquitoloon/"
    #create a directory if the directory doesn't exist yet
    if not os.path.exists(directory):
        os.makedirs(directory)

    #Inform on the statut of the operation
    print("Starting : done")


################################################################################

#This function will prepare the pump and the valves to realize the loading operation
def init():
    
    print("###############") 
    print("INITIALIZING")
    print("###############")
    
    #Inform on the statut of the operation
    print("Initializing : engaged")

    
    #Inform on the statut of the operation
    print("Initializing : done")


################################################################################

#image is very a basci way to take images
def image():
    
    print("###############") 
    print("IMAGING")
    print("###############")
    
    #Inform on the statut of the operation
    print("Imaging : engaged")
    
    #start the preview only during the acquisition
    camera.start_preview(fullscreen=False, window = (160, 0, 640, 480)) #x,y,w,h
    #allow the camera to warm up
    #sleep(2)
    
    #for frame in range(nb_frame):
        
    #turn the green LED ON (even if it's written off here)
    led.on()
    #sleep(0.5)
    
    #get the actual date
    date_now = datetime.now().strftime("%m_%d_%Y")
    day_now="/home/pi/Desktop/Mosquitoloon/"+str(date_now)
    
    #create a directory if the directory doesn't exist yet
    if not os.path.exists(day_now):
        os.makedirs(day_now)
        
    #get the actual date
    hour_now = datetime.now().strftime("%H")
    hour="/home/pi/Desktop/Mosquitoloon/"+str(date_now)+"/"+str(hour_now)
    
    #create a directory if the directory doesn't exist yet
    if not os.path.exists(hour):
        os.makedirs(hour)
    
    #get the time now
    time = datetime.now().strftime("%M_%S_%f")
    #create a filename from the date and the timeq
    filename="/home/pi/Desktop/Mosquitoloon/"+str(date_now)+"/"+str(hour_now)+"/"+str(time)+".h264"

    #capture a video with the specified filename
    #camera.capture(filename)
    record(camera, filename)
    
    #wait to complete the imaging process and print info on the terminal
    print("Imaging : "+str(frame)+"/"+str(nb_frame))
    print(datetime.now())
    
    #turn the green LED OFF (even if it's written on here)
    #sleep(0.5)
    led.off()
 
    #stop the preview during the rest of the sequence
    camera.stop_preview()
    
    #Inform on the status of the operation
    print("Imaging : done")


################################################################################

#wait will make the pi sleep until the next hour
def wait():
    
    print("###############") 
    print("WAITING")
    print("###############")
    
    #Inform on the statut of the operation
    print("Waiting : engaged")
    
    # Calculate the delay to the start of the next hour
    next_hour = (datetime.now() + timedelta(hours=1)).replace(
    minute=0, second=0, microsecond=0)
    delay = (next_hour - datetime.now()).seconds
    
    #wait to complete the waiting process and print info on the terminal
    for i in range(delay):
        print("Waiting : "+str(i)+"/"+str(delay))
        sleep(1) 
    
    #Inform on the status of the operation
    print("Waiting : done")


################################################################################

#stop will turn off the green LED and turn on the red one
def stop():
    
    #Inform on the statut of the operation
    print("The sequence is done.")


################################################################################
# F) Execute the sequence
################################################################################


start()

while True: 
    init()
    image()
    wait()
    
stop()

