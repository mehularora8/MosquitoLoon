#!/usr/bin/env python
# coding: utf-8

################################################################################
# A) Import the librairies needed to execute the script
################################################################################


#Activate pinout to control the LEDs and the RELAY
from gpiozero import LED
from gpiozero import Servo

#Servo control
import pigpio

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

directory="/home/pi/Desktop/Mosquitoloon/"

pi = pigpio.pi()
SERVO_GPIO = 17

led = LED(18)
camera = PiCamera()

camera.resolution = (640, 480)
camera.iso = 60

nb_frame=300

CLIP_DURATION = 60
BUFFER_CLIP_DURATION = 120

################################################################################
# E) Define simple functions making the whole sequence
################################################################################

#function changes desired angle to pwm signal value
def angleToPWM(angle):
    if angle > 90:
        angle = 90
    elif angle < -90:
        angle = -90
    return 1500 + (angle * 850) / 90

#function takes a video for duration seconds and saves it with name number in Mosquitoloon folder
def record(camera, filename, duration):
    camera.start_recording(filename)
    camera.wait_recording(duration)
    camera.stop_recording()


#First function to run in order to turn on the blue LED as well as the relay to make the I2C operational
def start():
    
    print("STARTING")
    
    #Inform on the statut of the operation
    print("Starting : engaged")
    
    #create a directory if the directory doesn't exist yet
    if not os.path.exists(directory):
        os.makedirs(directory)

    #Inform on the statut of the operation
    print("Starting : done")


################################################################################

#This function will prepare the pump and the valves to realize the loading operation
def init():
    
    print("INITIALIZING")
    
    #Inform on the statut of the operation
    print("Initializing : engaged")

    #Inform on the status of the operation
    print("Initializing : done")


################################################################################

#This function records videos using camera modules 
def image():
    
    print("IMAGING")
    
    #Inform on the statut of the operation
    print("Imaging : engaged")
    
    #start the preview only during the acquisition
    camera.start_preview(fullscreen=False, window = (160, 0, 640, 480)) #x,y,w,h

    for i in range(5):
        #set the angle to take a video from
        angle = 36 * i - 90
        pi.set_servo_pulsewidth(SERVO_GPIO, angleToPWM(angle))

        #get the actual date
        date_now = datetime.now().strftime("%m_%d_%Y")
        day_now = directory + str(date_now)
        
        #create a directory if the directory doesn't exist yet
        if not os.path.exists(day_now):
            os.makedirs(day_now)
            
        #get the actual date
        hour_now = datetime.now().strftime("%H")
        hour = directory + str(date_now) + "/" + str(hour_now)
        
        #create a directory if the directory doesn't exist yet
        if not os.path.exists(hour):
            os.makedirs(hour)
        
        #get the time now
        time = datetime.now().strftime("%M_%S_%f")

        #create a filename from the date and the timeq
        filename = directory + str(date_now) + "/" + str(hour_now) + "/"+str(time) + ".h264"

        #capture a video with the specified filename
        record(camera, filename, CLIP_DURATION)

    
    #stop the preview during the rest of the sequence
    camera.stop_preview()
    
    #Inform on the status of the operation
    print("Imaging : done")


#wait will make the pi sleep until the next hour
def wait():

    #get the actual date
        date_now = datetime.now().strftime("%m_%d_%Y")
        day_now = directory + str(date_now)
        
        #create a directory if the directory doesn't exist yet
        if not os.path.exists(day_now):
            os.makedirs(day_now)
            
        #get the actual date
        hour_now = datetime.now().strftime("%H")
        hour = directory + str(date_now) + "/" + str(hour_now)
        
        #create a directory if the directory doesn't exist yet
        if not os.path.exists(hour):
            os.makedirs(hour)
        
        #get the time now
        time = datetime.now().strftime("%M_%S_%f")
        buffer_directory = directory + str(date_now)+"/"+str(hour_now)+"/"+str(time)+"BUF.h264"
        
        print("WAITING")
        
        #Inform on the statut of the operation
        print("Waiting : engaged")

        print("Recording buffer now")
        # Buffer record for 2 minutes
        record(camera, buffer_directory, BUFFER_CLIP_DURATION)
        
        #Inform on the status of the operation
        print("Waiting : done")


#stop will turn off the green LED and turn on the red one
def stop():
    #Inform on the statut of the operation
    print("The sequence is done.")


#Main function
def main():
    start()
    led.on()
    init()

    while True:
        wait()
        image()
        
    stop()

main()

