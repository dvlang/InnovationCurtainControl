#!/usr/bin/env python
#-----------------------------------------------------------------------------
# A simple test to speed up and slow down 1 motor.
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
import time
import sys
import math
import qwiic_scmd
import qwiic_dual_encoder_reader

verion=0.5

myMotor = qwiic_scmd.QwiicScmd()
myEncoders = qwiic_dual_encoder_reader.QwiicDualEncoderReader()

NumRotations = 0
exact_revolutions=0
direction='null'

def curtainControl():
    print("Verion: ",verion)
    if len(sys.argv) != 3:
        raise ValueError('ERROR: INSUFFICIENT INPUT PARAMETERS')
    print("passed arg ", sys.argv[1])
    
    direction=sys.argv[1]
    print("direction= ", direction)
    
    NumRotations=int(sys.argv[2])
    print("number of rotations haha1", NumRotations)
    
    
    print("Motor Test.")
    R_MTR = 0
    L_MTR = 1
  
    #get direction from user
    if direction=="-open":
        DIR=1
    elif direction=="-close":
        DIR=0
    else:
        print("ERROR: INVALID DIRECTION")
        return


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
    myMotor.set_drive(1,0,0)

    myMotor.enable()
    print("Motor enabled")
    time.sleep(.250)

    myEncoders.count1=0
    myEncoders.get_diff(True)

    time.sleep(.250)
    print("initial count: ",myEncoders.count1)
	
	#Main Loop

    loopcount=0
    totalRotations=0
    i=0
    print("NumRotations is ",NumRotations)
    

    while i<NumRotations:
        print("i= ", i)
        myEncoders.count1=0
        
        while abs(myEncoders.count1)<5462:
            speed = 255
            myMotor.set_drive(R_MTR,DIR,speed)
            time.sleep(.15)

            myMotor.set_drive(0,0,0)

            time.sleep(.15)

            
            print("rotation_count: ",myEncoders.count1)
            print("in loop ",loopcount)
            loopcount=loopcount+1
            if myEncoders.count1>=5462:
                totalRotations=totalRotations+myEncoders.count1
        print("Rotations ",(i+1))
        i=i+1
		
    myMotor.set_drive(0,0,0)
    myMotor.disable()
    
    exact_revolutions=totalRotations/5462.22
    print("Revolutions: ",exact_revolutions)
	
if __name__ == '__main__':
    try:
        curtainControl()
    except (KeyboardInterrupt, SystemExit) as exErr:
        print("Ending example.")
        myMotor.disable()
        sys.exit(0)
