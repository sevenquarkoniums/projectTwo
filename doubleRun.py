#!/usr/bin/env python
'''
'''
outputName = 'appDouble.out'
import time
import subprocess
import os

with open(outputName, 'w') as out:
    out.write('run,thread_Dedup,thread_Swaptions,startTime,end_Dedup,end_Swaptions\n')

FNULL = open(os.devnull, 'w')
app_bin='/home/centos/benchmarks/parsec-3.0/bin/'
unfinished = True
irun = 0
logthread_D = 5# from 5 to 0.
logthread_S = 5# from 5 to 0.
thread_D = 2 ** logthread_D
thread_S = 2 ** logthread_S
obj_D, obj_S = None, None
finish_D, finish_S = False, False

while 1:
    if obj_D == None and obj_S == None:# when nothing is running.
        print 'run %d, thread_Dedup %d, thread_Swaptions %d' % (irun, thread_D, thread_S)
        cmd_D = '{}parsecmgmt -a run -i native -n {} -p {}'.format(app_bin, thread_D, 'dedup')
        obj_D = subprocess.Popen(cmd_D, stdout=FNULL, shell=True)
        cmd_S = '{}parsecmgmt -a run -i native -n {} -p {} -c gcc-tbb'.format(app_bin, thread_S, 'swaptions')
        obj_S = subprocess.Popen(cmd_S, stdout=FNULL, shell=True)
        appStart = time.time()
    if obj_D != None and obj_S != None and obj_D.poll() != None and finish_D == False:# dedup just finished.
        print 'dedup finished.'
        end_D = time.time()
        finish_D = True
    if obj_D != None and obj_S != None and obj_S.poll() != None and finish_S == False:# swaptions just finished.
        print 'swaptions finished.'
        end_S = time.time()
        finish_S = True
    if finish_D and finish_S:# both apps finished.
        line = '%d,%d,%d,%.1f,%.1f,%.1f' % (irun, thread_D, thread_S, appStart, end_D, end_S)
        with open(outputName, 'a') as out:
            out.write('%s\n' % line)
        finish_D, finish_S = False, False
        obj_D, obj_S = None, None
        if logthread_D != 0:# loop through thread_D.
            logthread_D = logthread_D - 1
        if logthread_D == 0 and logthread_S != 0:
            logthread_D = 5
            logthread_S = logthread_S - 1
        if logthread_D == 0 and logthread_S == 0:
            logthread_D = 5
            logthread_S = 5
            irun += 1
        thread_D = 2 ** logthread_D
        thread_S = 2 ** logthread_S
    if irun == 20:
        break
    time.sleep(0.1)

print 'finished, and %s is updated.' % outputName

