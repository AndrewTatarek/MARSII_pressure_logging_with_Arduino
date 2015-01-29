''' this file logs data from a set of pressure sensors into an intermediate
JSON file'''

import time
import sys
import json
#sys.path.append(r'C:\Users\David\Dropbox\CODE\Reusable')
sys.path.append(r'X:\CODE\Reusable')
import autoSetup
from arduinoPressureSensor import PressureSensor
import MARS_analysis

# I want to record what job each sensor is doing
purposes = ['green (on time)',None,'output pressure (upstream of the Alicat)','orange (off time)','red (supply)']

# I want a sorted list of pressure sensors
pSensors = autoSetup.setup_list_of(PressureSensor)
print(len(pSensors),'sensors detected')
assert pSensors # there should be at least one 
pSensors.sort(key=lambda x:x.serialNumber)
for sensor in pSensors:
    sensor.fullLog['purpose'] = purposes[sensor.serialNumber]
    
# nice to know info
for pSensor in pSensors:
    print(pSensor.serialNumber,pSensor.comHandle.port+1,pSensor.pressure())
    
timeToRunFor = float(input('How many seconds should data be recorded for?\n'))
fileName = 'MARS data\\'+input('What should the results file be called?\n')

# start the timer
startTime = time.perf_counter()
# clear the existing data
for pSensor in pSensors:
    pSensor.comHandle.read_all()
    pSensor.log = []
    pSensor.fullLog['log'] = pSensor.log
# log some new data
while time.perf_counter() < startTime+timeToRunFor:
    # note that the pressure() method also retrieves data from the COM port and puts it in the log
    timeAndPresssures = [time.perf_counter()-startTime]+[sensor.pressure() for sensor in pSensors]
    print(' \t'.join('{:.4}'.format(double)for double in timeAndPresssures))

with open(fileName+'.json','w') as fileHandle:
    tmp1 = pSensors[0].fullLog
    tmp2 = tmp1['log']
    tmp3 = len(tmp2)
    json.dump([sensor.fullLog for sensor in pSensors],fileHandle)
print('json file finished')
# currently I pass the file name, it would be more efficent to pass the data
# structure before it got converted to JSON
#MARS_analysis.analyse(fileName)
#print('analysis finished')
