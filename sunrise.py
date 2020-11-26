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
    tsunrise= sunrise.replace(month=11, day=25) #make it today
    tsunset= sunset.replace(month=11, day=25) #make it today


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



now = datetime.datetime.now()       
today1am = now.replace(hour=1, minute=0, second=0, microsecond=0)
timetocheck = now.replace(month=11, day=25, hour=int(sys.argv[1]), minute=0, second=0, microsecond=0)
    
openRunOnce = False
closeRunOnce= False

if(timetocheck>getsuntime("sunrise")):    #replace timetocheck with now for not testcase>
    openRunOnce=True
    runmotor("open",4)
    position=1
    print("sunrise open")
    
if(timetocheck>getsuntime("sunset")):
    closeRunOnce=True
    runmotor("close",4)
    position=0
    print("sunset close")

if(today1am==timetocheck.replace(minute=0, second=0, microsecond=0)):
    openRunOnce = False
    closeRunOnce= False
    print("reset for day")
    
