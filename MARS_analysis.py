import os
import json
import itertools
import time
import sys
sys.path.append(r'C:\Users\David\Dropbox\CODE\Reusable')
sys.path.append(r'X:\CODE\Reusable')
import streamTiming

def analyse(fileName):
    assert fileName[-5:] == '.json'
    'this loads json from the given file, processes it and outputs it'
    print('loading logs')
    fullLogs = json.load(open(fileName))
    print('calculating times on a per sensor basis')
    readingsWithSeperateTimes = [streamTiming.give_all_readings_a_time(fullLog['log']) for fullLog in fullLogs]
    # rescale the output pressure to look better on the graphs
    for i, dataFromASensor in enumerate(readingsWithSeperateTimes):
        if fullLogs[i]['purpose'] == 'output pressure (upstream of the Alicat)':
            for i in range(len(dataFromASensor)):
                calculatedTime,pressure = dataFromASensor[i]
                dataFromASensor[i] = calculatedTime, pressure*65
    for fullLog in fullLogs:
        del fullLog['log']
    print('syncing data from each sensor')
    readingsWithCombinedTimes = sync(readingsWithSeperateTimes)
    # I want the results to be labled .txt
    outputFileName = fileName[:-5]+'.txt'
    print('writing to file')
    with open(outputFileName,'w') as outputFile:
        testDescription = fileName.split('\\')[-1].split('.')[0]+'\n'
        outputFile.write(testDescription)
        fileOrigin = 'This data was taken from: ' + fileName+'\n'
        outputFile.write(fileOrigin)
        timeAtTestStart = time.localtime(fullLogs[0]["initial unix time"])
        outputFile.write(time.strftime("The data was recorded on: %A, %d %b %Y %H:%M:%S\n\n",timeAtTestStart))
        headers = 'Time (seconds)\t'+'\t'.join([str(fullLog['purpose']) for fullLog in fullLogs])+'\n'
        outputFile.write(headers)
        fileBody = '\n'.join('\t'.join(str(value) for value in reading) for reading in readingsWithCombinedTimes)
        outputFile.write(fileBody)
        # the blank lines make it easier to paste new data over old data in excel
        #blankLines = (('\t'*(len(readingsWithCombinedTimes[0])-1))+'\n')*100
        #outputFile.write(blankLines)
    print('analysis done')

def sync(logs):
    '''up to this point the data from each sensor has been processed
    independently. I now want to sample the data at a fixed rate with times
    starting from 0. This will also synchronize the data'''
    Hz = 800
    # I want to start at the latest start point of all the input streams
    startTime = max([log[0][0] for log in logs])
    syncedLog = []
    # I initalise all the indexes to point at the begining of the logs
    indexes = [0 for log in logs]
    # I will create a combined log with unified times
    for generatedTime in itertools.count(startTime,1/Hz):
        # each synced reading starts with the time and the times start from 0
        syncedReading = [generatedTime-startTime]
        # I then add the pressures to the synced readings
        # to find the pressure at the right time I migrate the indexes along the logs
        #
        try:
            for i,log in enumerate(logs):
                while logs[i][indexes[i]+1][0]<=generatedTime:
                    indexes[i]+=1
                firstTime      = logs[i][indexes[i]  ][0]
                secondTime     = logs[i][indexes[i]+1][0]
                firstPressure  = logs[i][indexes[i]  ][1]
                secondPressure = logs[i][indexes[i]+1][1]
                deltaTime = secondTime - firstTime
                deltaPressure = secondPressure - firstPressure
                # the index should now be pointing at the right point in the log
                assert firstTime<=generatedTime<secondTime 
                fraction = (generatedTime-firstTime)/deltaTime
                interpolatedPressure = firstPressure + fraction*deltaPressure
                assert (firstPressure<=interpolatedPressure<=secondPressure or
                        firstPressure>=interpolatedPressure>=secondPressure)
                syncedReading.append(interpolatedPressure)
        except IndexError:
            # assert that the full syncedLog has been created
            break
        syncedLog.append(syncedReading)
    return syncedLog

    
if __name__ == '__main__':
    print(__file__)
    #for reading in analyse('MARS data/x'):
    #    print(*reading)
    filePath = r'C:\Users\David\Dropbox\CODE\Python\mars data'
    #filePath = r'X:\CODE\Python\mars data'
    
    fileNames = [filePath+'\\'+f for f in os.listdir(filePath) if f[-5:]=='.json']
    #fileNames = [filePath+'\\'+'Unit B with 40 shore disks after 1 day.json']
    for fileName in fileNames:
        print('now processing: '+fileName)
        analyse(fileName)
    print('it worked')




    
