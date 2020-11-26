from __future__ import print_function
import ephem  
import datetime
import sys


o=ephem.Observer()  
o.lat='41.99'  
o.long='-87.98'  
s=ephem.Sun()  
s.compute()  
#print ephem.localtime(o.next_rising(s))  
#print ephem.localtime(o.next_setting(s))  


def runmotor(direction,rotations):
    print("running motor in direction ", direction, " and for rotations= ", rotations)

now = datetime.datetime.now()
sunrise = ephem.localtime(o.next_rising(s))  
sunset=ephem.localtime(o.next_setting(s))  

#print(sunrise)
#print(sunset)
#print(now)

#set up test times
tsunrise= sunrise.replace(month=11, day=25) #make it today
tsunset= sunset.replace(month=11, day=25) #make it today
timetocheck = now.replace(month=11, day=25, hour=int(sys.argv[1]), minute=0, second=0, microsecond=0)

print(tsunrise)
print(tsunset)
print(timetocheck)

today1am = now.replace(hour=1, minute=0, second=0, microsecond=0)

openRunOnce = False
closeRunOnce= False

if(timetocheck>tsunrise):    #replace timetocheck with now for normal>
    openRunOnce=True
    runmotor("open",4)
    position=1
    print("sunrise open")
    
if(timetocheck>tsunset):
    closeRunOnce=True
    runmotor("close",4)
    position=0
    print("sunset close")

if(today1am==timetocheck.replace(minute=0, second=0, microsecond=0)):
    openRunOnce = False
    closeRunOnce= False
    print("reset for day")
    

    


#if(sunrisetime < timetocheck):
 #   print("<true")
#if(sunrisetime == timetocheck):
 #   print("=true")
#if(sunrisetime > timetocheck):
 #   print(">true")