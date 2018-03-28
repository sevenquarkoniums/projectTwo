#!/usr/bin/env python
'''
'''
outputName = 'monitorDouble.out'
import time
import subprocess

with open(outputName, 'w') as out:
    out.write('time,cpu-clock,context-switches,cpu-migrations,page-faults,user,nice,system,idle,iowait,irq,softirq,steal\n')

while 1:
    perf = subprocess.check_output('sudo perf stat -a sleep 1 2>&1', shell=True)
    perfsplit = perf.split()
    m1 = float(perfsplit[6].replace(',', ''))
    m2 = int(perfsplit[13].replace(',', ''))
    m3 = int(perfsplit[18].replace(',', ''))
    m4 = int(perfsplit[23].replace(',', ''))
    procstat = subprocess.check_output('cat /proc/stat 2>&1', shell=True)
    procstatsplit = procstat.split()
    user = int(procstatsplit[1])
    nice = int(procstatsplit[2])
    system = int(procstatsplit[3])
    idle = int(procstatsplit[4])
    iowait = int(procstatsplit[5])
    irq = int(procstatsplit[6])
    softirq = int(procstatsplit[7])
    steal = int(procstatsplit[8])
    t = time.time()
    data = '%.1f,%.1f,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d' % (t, m1, m2, m3, m4, user, nice, system, idle, iowait, irq, softirq, steal)
    print data
    with open(outputName, 'a') as out:
        out.write('%s\n' % data)

