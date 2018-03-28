#!/usr/bin/env python
'''
'''
outputName = 'appSingle.out'
import time
import subprocess

with open(outputName, 'w') as out:
    out.write('run,thread,app,startTime,endTime\n')

app_bin='/home/centos/benchmarks/parsec-3.0/bin/'
for irun in range(10):
    print 'run number: %d' % irun
    for thread in [32,16,8,4,2,1]:
        print 'thread number: %d' % thread
        for app in ['dedup', 'swaptions']:
            print 'Starting job ' + app
            appStart = time.time()
            if app == 'dedup':
                cmd = '{}parsecmgmt -a run -i native -n {} -p {}'.format(app_bin, thread, app)
            elif app == 'swaptions':
                cmd = '{}parsecmgmt -a run -i native -n {} -p {} -c gcc-tbb'.format(app_bin, thread, app)
            subprocess.call(cmd, shell=True)
            appEnd = time.time()
            with open(outputName, 'a') as out:
                out.write('%d,%d,%s,%.1f,%.1f\n' % (irun, thread, app, appStart, appEnd))

print 'finished, and %s is updated.' % outputName
