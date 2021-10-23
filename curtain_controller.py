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
from adafruit_motorkit import MotorKit
from gpiozero import Button

live=True
#version string
version="0.25"
lf="/home/pi/Documents/curtaincontroller/curtainlog.txt"

print("VERSION", version)

myMotor = qwiic_scmd.QwiicScmd()
myEncoders = qwiic_dual_encoder_reader.QwiicDualEncoderReader()

#initialize globals
NumRotations = 0
exact_revolutions=0
direction='null'
OperateMotor=False     
buttonL = Button(17)
buttonR = Button(18)
tmpstr="null"
fullrotationsneeded=2
timetoclose=16
timetoopen=16
AllMotors=0
LeftMotor=1
RightMotor=2

####################################################################################################
##  
##  function:    logevent(string)
##  inputs: string filename, string test
##  return: 
##  Description: ths function will open a file for appending, and added passed test with a timestamp
##
####################################################################################################
##// BEGIN logevent()//###
def logevent(logfilename,eventstring):
    fo=open(logfilename,"a")
    fo.write(str(datetime.datetime.now()))
    tmpstring=" " + eventstring +"\n"
    fo.write(tmpstring)
    fo.close()
    return
##// END logevent()//###


####################################################################################################
##  
##  function:    runmotor(string,int)
##  inputs: diretion (open|close), rotations(int)
##  return: 
##  Description: this function will run the motor in the direction set for the rotations requested
##
####################################################################################################
##// BEGIN runmotor//###
def runmotor(motorid,direction,rotations):
    print("running motor ", motorid, " in direction ", direction, " and for rotations= ", rotations)
    
    #get direction from user
    if direction=="open":
        DIR=1
    elif direction=="close":
        DIR=0
    else:
        print("ERROR: INVALID DIRECTION")
        return
     
    #NumRotations=rotations

    kit = MotorKit()
    rotation=0
    kit.motor1.throttle = 0   
    kit.motor2.throttle = 0    
    
    if direction=="open":
 
        #intDuration=2.95


        #open
        #intDuration=2.75*9.5
        intDuration=2.75*rotations
        rotation=1.0
        
        if(motorid==0):
            kit.motor1.throttle = rotation
            kit.motor2.throttle = rotation
        elif(motorid==1):
            kit.motor1.throttle = rotation
        elif(motorid==2):
            kit.motor2.throttle = rotation
        
        time.sleep(intDuration)
        kit.motor1.throttle = 0
        kit.motor2.throttle = 0
    elif direction=="close":
     
        #intDuration=2.95


        #open
        #intDuration=2.75*9.5
        intDuration=2.75*rotations
        rotation=-1.0
            
        if(motorid==0):
            kit.motor1.throttle = rotation
            kit.motor2.throttle = rotation
        elif(motorid==1):
            kit.motor1.throttle = rotation
        elif(motorid==2):
            kit.motor2.throttle = rotation
            
        time.sleep(intDuration)
        kit.motor1.throttle = 0
        kit.motor2.throttle = 0
    else:
        return
    
    return
    
    
##// END runmotor()//###

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

#live time   
    if(live):
        tsunrise= sunrise.replace(second=0, microsecond=0) #make it today
        tsunset= sunset.replace(second=0, microsecond=0) #make it today
    else:
        #set up test times
        tsunrise= sunrise.replace(month=12, day=1, second=0, microsecond=0) #make it today
        tsunset= sunset.replace(month=12, day=1, second=0, microsecond=0) #make it today


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


####################################################################################################
##              THIS IS MY MAIN FUNCTION                                                         ###
####################################################################################################  
##  function:    curtain_controller()
##  inputs: none
##  command line args: int hourtostart int minutetostart bool testmode
##  return: 
##  Description: this function will run the motor in the direction set for the rotations requested
##
####################################################################################################
##// BEGIN curtain_controller()//###
def curtain_controller():

    tmpstr=  " version= " + version +"\n"
    logevent(lf, tmpstr)
    if(live):
        tmpstr="LIVE MODE"
        logevent(lf,tmpstr) 
        
    logevent(lf, "begin execution")
    
    timehour=int(sys.argv[1])
    timemin=int(sys.argv[2])
            
    now = datetime.datetime.now()       
    
    if(not live):
        #use this line for test
        timetocheck = now.replace(month=12, day=1, hour=timehour, minute=timemin, second=0, microsecond=0)
        tmpstr="time to check= " +str(timetocheck)
        logevent(lf,tmpstr)       
    
    #print(timetocheck)
        
    openRunOnce = False
    closeRunOnce= False

    #this value needs to represent the absolute position from position sensor
    curtainOpen=False
    LcurtainOpen=False
    RcurtainOpen=False

    #remove if not testing
    if(sys.argv[3]=='t'):
        curtainOpen=True #grab a test initial position
        LcurtainOpen=True
        RcurtainOpen=True
        
    elif(sys.argv[3]=='f'):
        curtainOpen=False
        LcurtainOpen=False
        RcurtainOpen=False
    
    tmpstr="sunrise = " +str(getsuntime("sunrise"))
    logevent(lf,tmpstr)
    tmpstr="sunset = " +str(getsuntime("sunset"))
    logevent(lf,tmpstr)

    #main run loop
    while True:
        time.sleep(0.45)
        now = datetime.datetime.now()       
        
        if(live):
            today1am = now.replace(hour=1, minute=0, second=0, microsecond=0)
        else:
            today1am = now.replace(month=12, day=1, hour=1, minute=0, second=0, microsecond=0)
        
        if(live):
            timetocheck = now.replace(microsecond=0)
        

        #logevent(lf,str(timetocheck))
        
        #sun this routine to OPEN LEFT curtain
        if(timetocheck==getsuntime("sunrise") and not openRunOnce and not LcurtainOpen and not timetocheck==getsuntime("sunset")):    #replace timetocheck with now for not testcase>

            logevent(lf," Left curtain sunrise open called\n")
            openRunOnce=True
            runmotor(LeftMotor, "open",timetoopen)
            LcurtainOpen=True
            print("Left curtain sunrise open")

            
        
        #run this routine to CLOSE LEFT curtain
        if(timetocheck==getsuntime("sunset") and not closeRunOnce and LcurtainOpen and not timetocheck==getsuntime("sunrise")):

            logevent(lf," Left curtain sunset close called\n")
            closeRunOnce=True
            runmotor(LeftMotor,"close",timetoclose)
            LcurtainOpen=False
            print("Left curtain sunset close")

        #run this routine to OPEN RIGHT curtain 
        if(timetocheck==getsuntime("sunrise") and not openRunOnce and not RcurtainOpen and not timetocheck==getsuntime("sunset")):    #replace timetocheck with now for not testcase>

            logevent(lf," Right curtain sunrise open called\n")
            openRunOnce=True
            runmotor(RightMotor, "open",timetoopen)
            RcurtainOpen=True
            print("Right curtain sunrise open")

            
        
        #run this routine to CLOSE RIGHT curtain
        if(timetocheck==getsuntime("sunset") and not closeRunOnce and RcurtainOpen and not timetocheck==getsuntime("sunrise")):

            logevent(lf," Right curtain sunset close called\n")
            closeRunOnce=True
            runmotor(RightMotor,"close",timetoclose)
            RcurtainOpen=False
            print("Right curtain sunset close")           
            
            
            
            
        
        #run this routine to reset time automatic open/close flags
        #if(today1am==timetocheck.replace(minute=0, second=0, microsecond=0)):
        if(today1am==timetocheck.replace(microsecond=0)):
            logevent(lf, " reset day\n")
            openRunOnce = False
            closeRunOnce= False
            print("reset for day")
            tmpstr="New sunrise = " +str(getsuntime("sunrise"))
            logevent(lf,tmpstr)
            tmpstr="New sunset = " +str(getsuntime("sunset"))
            logevent(lf,tmpstr)
            time.sleep(60)
        
        #if(openRunOnce and closeRunOnce):
         #   logevent(lf, " new reset day routine\n")
        
        #check for manual current open/close request
        while buttonL.is_pressed:
            time.sleep(.5)
            buttonL.wait_for_release()
            time.sleep(.5)
            print("buttonL released")
            if LcurtainOpen:
                runmotor(LeftMotor,"close",timetoclose)
                curtainOpen=False
                LcurtainOpen=False
                print("left curtain manually closed")

                logevent(lf," user requested manual close left curtain\n")
            else:
                runmotor(LeftMotor,"open",timetoopen)
                curtainOpen=True
                LcurtainOpen=True
                print("left curtain manually opened")

                logevent(lf," user requested manual open left curtain\n")
            time.sleep(.1)

        #check for manual current open/close request
        while buttonR.is_pressed:
            time.sleep(.5)
            buttonR.wait_for_release()
            time.sleep(.5)
            print("buttonL released")
            if RcurtainOpen:
                runmotor(RightMotor,"close",timetoclose)
                curtainOpen=False
                RcurtainOpen=False
                print("Right curtain manually closed")

                logevent(lf," user requested manual close right curtain\n")
            else:
                runmotor(RightMotor,"open",timetoopen)
                curtainOpen=True
                RcurtainOpen=True
                print("Right curtain manually opened")

                logevent(lf," user requested manual open right curtain\n")
            time.sleep(.1)


        #if(not live):
        #    timehour=int(raw_input("new hour: "))
        #    timemin=int(raw_input("new min: "))
        if(not live):
            if(timemin<59):
                timemin=timemin+1
            else:
                timemin=0
                if(timehour<23):
                    timehour=timehour+1
                else:
                    timehour=0
            timetocheck = now.replace(month=12, day=1, hour=timehour, minute=timemin, second=0, microsecond=0)

    
if __name__ == '__main__':
    try:
        curtain_controller()
    except (KeyboardInterrupt, SystemExit) as exErr:
        print("Ending program")
        myMotor.disable()
        logevent(lf," ERROR/EXIT\n*****************************************************\n")
        sys.exit(0)