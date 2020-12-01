#!/usr/bin/env python
#-----------------------------------------------------------------------------
# Curtain controller software inclusdes portions of sparkfun autophat exampe code used with following copyright and permission.
# Updated Dan Lang November, 2020
#
    #------------------------------------------------------------------------
    #
    # Written by Mark Lindemer
    # SparkFun Electronics, April 2020
    # 
    # This python library supports the SparkFun Electroncis qwiic 
    # qwiic sensor/board ecosystem on a Raspberry Pi (and compatable) single
    # board computers. 
    #
    # More information on qwiic is at https://www.sparkfun.com/qwiic
    #
    # Do you like this library? Help support SparkFun. Buy a board!
    #
    #==================================================================================
    # Copyright (c) 2019 SparkFun Electronics
    #
    # Permission is hereby granted, free of charge, to any person obtaining a copy 
    # of this software and associated documentation files (the "Software"), to deal 
    # in the Software without restriction, including without limitation the rights 
    # to use, copy, modify, merge, publish, distribute, sublicense, and/or sell 
    # copies of the Software, and to permit persons to whom the Software is 
    # furnished to do so, subject to the following conditions:
    #
    # The above copyright notice and this permission notice shall be included in all 
    # copies or substantial portions of the Software.
    #
    # THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
    # IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
    # FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
    # AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
    # LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
    # OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE 
    # SOFTWARE.
#==================================================================================
# 
#


from __future__ import print_function
import ephem  
import datetime
import sys
import time
import math
import qwiic_scmd
import qwiic_dual_encoder_reader
from gpiozero import Button

tmpstr="null"

version="0.4"
print("VERSION", version)
fo=open("curtainlog.txt","a")

fo.write(str(datetime.datetime.now()))
   
tmpstr=  " version= " + version +"\n"
#fo.write("version=")
#fo.write(str(version))
#fo.write("\n")
fo.write(tmpstr)

myMotor = qwiic_scmd.QwiicScmd()
myEncoders = qwiic_dual_encoder_reader.QwiicDualEncoderReader()

NumRotations = 0
exact_revolutions=0
direction='null'
OperateMotor=False
        
button = Button(17)

fullrotationsneeded=1



####################################################################################################
##  
##  function:    runmotor()
##  inputs: diretion (open|close), rotations(int)
##  return: 
##  Description: this function will run the motor in the direction set for the rotations requested
##
####################################################################################################
##// BEGIN runmotor//###
def runmotor(direction,rotations):
    print("running motor in direction ", direction, " and for rotations= ", rotations)
    
    #get direction from user
    if direction=="open":
        DIR=1
    elif direction=="close":
        DIR=0
    else:
        print("ERROR: INVALID DIRECTION")
        return
     
    NumRotations=rotations
    
    #initialize motors
    if myMotor.connected == False:
        print("Motor Driver not connected. Check connections.", \
            file=sys.stderr)
        return
    myMotor.begin()
    print("Motor initialized.")
    time.sleep(.250)

	#initialize encoders
    if myEncoders.connected == False:
        print("The Qwiic Dual Encoder Reader device isn't connected to the system. Please check your connection", \
            file=sys.stderr)
        return
    
	myEncoders.begin()
    print("Encoder initialized.")
    time.sleep(.250)

    # Zero Motor Speeds
    myMotor.set_drive(0,0,0)

    myMotor.enable()
    print("Motor enabled")
    time.sleep(.250)
    
    #init counters
    print("Initialize Counters")
    myEncoders.count1=0
    loopcount=0
    totalRotations=0
    i=0
    print("NumRotations is ",NumRotations)
                    
    while i<NumRotations:
        print("i= ", i)
        myEncoders.count1=0
            
        while abs(myEncoders.count1)<5462:
            speed = 255
            myMotor.set_drive(0,DIR,speed)
            time.sleep(.15)             #need just a little delay to let count propagate correction
            myMotor.set_drive(0,0,0)    #stop to let motor position detection occur
            time.sleep(.15)             #need just a little delay to let count propagate correction

            print("rotation_count: ",myEncoders.count1)
            print("in loop ",loopcount)
            loopcount=loopcount+1
            if abs(myEncoders.count1)>=5462:
                totalRotations=totalRotations+abs(myEncoders.count1)


        print("Rotations ",(i+1))
        i=i+1
        
    #shut down motor    
    myMotor.set_drive(0,0,0)
    #myMotor.disable()
        
    #print the exact numbr of rotations performed
    exact_revolutions=totalRotations/5462.22
    print("Revolutions: ",exact_revolutions)    
    
    myMotor.disable()
    
    
    
##// END runmotor//###

####################################################################################################
##  
##  function:    getsuntime()
##  inputs: direction (sunset | sunrise)
##  return: 
##  Description: this function will run the motor in the direction set for the rotations requested
##
####################################################################################################
##// BEGIN getsuntime//###
def getsuntime(direction):
    o=ephem.Observer()  
    o.lat='41.99'  
    o.long='-87.98'  
    s=ephem.Sun()  
    s.compute()  
    #print ephem.localtime(o.next_rising(s))  
    #print ephem.localtime(o.next_setting(s))  

    sunrise = ephem.localtime(o.next_rising(s))  
    sunset=ephem.localtime(o.next_setting(s))  

    #print(sunrise)
    #print(sunset)
    #print(now)

    #set up test times
    tsunrise= sunrise.replace(month=11, day=30, microsecond=0) #make it today
    tsunset= sunset.replace(month=11, day=30, microsecond=0) #make it today


    #print(tsunrise)
    #print(tsunset)
    #print(timetocheck)

    if(direction=="sunrise"):
        return tsunrise         #change to sunrise for not testcase
    elif(direction=="sunset"):
        return tsunset          #change to sunset for not testcase
    else:
        return null
##// END getsuntime//###

###  MAIN ##########
def curtain_controller():
    now = datetime.datetime.now()       
    today1am = now.replace(hour=1, minute=0, second=0, microsecond=0)
    timetocheck = now.replace(month=11, day=30, hour=int(sys.argv[1]), minute=0, second=0, microsecond=0)

    #print(timetocheck)
        
    openRunOnce = False
    closeRunOnce= False

    #this value needs to represent the absolute position from position sensor
    curtainOpen=True

    #remove if not testing
    if(sys.argv[2]=='t'):
        curtainOpen=True #grab a test initial position
    elif(sys.argv[2]=='f'):
        curtainOpen=False

    #main run loop
    while True:
        #sun this routine to OPEN curtain
        if(timetocheck>getsuntime("sunrise") and not openRunOnce and not curtainOpen and not timetocheck>getsuntime("sunset")):    #replace timetocheck with now for not testcase>
            fo.write(str(datetime.datetime.now()))
            fo.write(" sunrise open called\n")
            openRunOnce=True
            runmotor("open",fullrotationsneeded)
            curtainOpen=True
            print("sunrise open")

            
        
        #run this routine to CLOSE curtain
        if(timetocheck>getsuntime("sunset") and not closeRunOnce and curtainOpen and not timetocheck<getsuntime("sunrise")):
            fo.write(str(datetime.datetime.now()))
            fo.write(" sunset close called\n")
            closeRunOnce=True
            runmotor("close",fullrotationsneeded)
            curtainOpen=False
            print("sunset close")
        
        #run this routine to reset time automatic open/close flags
        if(today1am==timetocheck.replace(minute=0, second=0, microsecond=0)):
            fo.write(str(datetime.datetime.now()))
            fo.write(" reset day\n")
            openRunOnce = False
            closeRunOnce= False
            print("reset for day")
        
        #check for manual current open/close request
        while button.is_pressed:
            time.sleep(.5)
            button.wait_for_release()
            time.sleep(.5)
            print("button released")
            if curtainOpen:
                runmotor("close",fullrotationsneeded)
                curtainOpen=False
                print("curtain manually closed")
                fo.write(str(datetime.datetime.now()))
                fo.write(" user requested manual close\n")
            else:
                runmotor("open",fullrotationsneeded)
                curtainOpen=True
                print("curtain manually opened")
                fo.write(str(datetime.datetime.now()))
                fo.write(" user requested manual close\n")
            time.sleep(.1)





    
if __name__ == '__main__':
    try:
        curtain_controller()
    except (KeyboardInterrupt, SystemExit) as exErr:
        print("Ending program")
        myMotor.disable()
        fo.write(str(datetime.datetime.now()))
        fo.write(" ERROR/EXIT\n")
        fo.close()
        sys.exit(0)