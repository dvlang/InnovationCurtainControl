#!/usr/bin/env python
#-----------------------------------------------------------------------------
# Curtain controller software inclusdes portions of sparkfun autophat exampe code used with following copyright and permission.
# Updated Dan Lang November, 2020
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
# Example 1
#


from __future__ import print_function
import ephem  
import datetime
import sys

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
            openRunOnce=True
            runmotor("open",4)
            position=1
            print("sunrise open")
        
        #run this routine to CLOSE curtain
        if(timetocheck>getsuntime("sunset") and not closeRunOnce and curtainOpen and not timetocheck<getsuntime("sunrise")):
            closeRunOnce=True
            runmotor("close",4)
            position=0
            print("sunset close")
        
        #run this routine to reset time automatic open/close flags
        if(today1am==timetocheck.replace(minute=0, second=0, microsecond=0)):
            openRunOnce = False
            closeRunOnce= False
            print("reset for day")





    
if __name__ == '__main__':
    try:
        curtain_controller()
    except (KeyboardInterrupt, SystemExit) as exErr:
        print("Ending program")
        #myMotor.disable()
        sys.exit(0)