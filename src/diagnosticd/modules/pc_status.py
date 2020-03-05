#! /usr/bin/env python3

import configparser
import sys
import os
import datetime
import time
import subprocess
import re
import psutil 

CONFIG_FILE = "/usr/local/src/diagnostic-tool/conf/diagnosticd.conf"
CPU_USAGE_CMD = "grep cpu /proc/stat | awk '{usage=($2+$4)*100/($2+$4+$5)} END {print usage}'"
DRIVE_CAP_CMD = "df -h | grep 'data'"
PING_CMD = "ping -c 2 google.ca"

def network():
    
    rtt_out = subprocess.Popen(PING_CMD, shell=True, stdout=subprocess.PIPE).communicate()[0].split()
    rtt_ = [x for x in rtt_out if b"time=" in x]
        
    if rtt_out:
        rtt = sum([float(x.split(b'=')[1]) for x in rtt_])/len(rtt_)
    else:
        rtt = 'no connection to network'

    return rtt

def cpu_usage():
    return psutil.cpu_percent()

def drive_capacity():
    return subprocess.run(DRIVE_CAP_CMD)

#def humidity():
#def temperature():

