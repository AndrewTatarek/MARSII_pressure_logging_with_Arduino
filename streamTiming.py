'''
this module was done in a hurry, it is aplication specific (pressure logging)
It has not been generalised
I think it would be a good idea to generalise this file but there is not enough
time.
'''

# To reduce the amount of data that is processed I put upper and lower bounds on
# the times to process
analysisStartTime = 0
analysisEndTime = 60

def give_all_readings_a_time(log):
    '''this takes a list of readings grouped by their time of arrival and
    returns a list of readings each with it's own time. This function is
    implimented in a really quick and crappy way using linear intrpolation'''
    firstTime = log[0]['time']
    lastTime = log[-1]['time']
    duration = lastTime - firstTime
    #print(firstTime,lastTime,duration)
    del log[0]
    readings = []
    for pair in log:
        readings.extend(pair['readings'])
    logLen = len(readings)
    readingsWithTimes = []
    for i, pressure in enumerate(readings):
        timeForThisReading = firstTime+duration*i/logLen
        # don't record anything until the start time
        if timeForThisReading<analysisStartTime+firstTime:
            continue
        # don't record anything after the end time
        if timeForThisReading>analysisEndTime+firstTime:
            break
        #assert readings[i]==pressure
        # sometimes the sensors produce bogus readings
        # I want to remove any reading that is more then 1 bar diffrent from
        # the readings immidiately before and after
        try:
            if abs(readings[i-1]-readings[i]) > 1 and abs(readings[i]-readings[i+1]) > 1:
                # set the pressure to a clearly bogus value that is easy to ignore
                pressure = -1
        except IndexError:
            # I don't care about the index errors caused by the first and last elements of the list
            pass
        readingsWithTimes.append((timeForThisReading,pressure))
    return readingsWithTimes

if __name__ == '__main__':
    import json
    fullLogs = json.load(open(r'C:\Users\David\Dropbox\CODE\Python\MARS data\x.json'))
    readingsWithSeperateTimes = [give_all_readings_a_time(fullLog['log']) for fullLog in fullLogs]
    #print(readingsWithSeperateTimes)