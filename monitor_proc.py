#!/bin/env python
# -*- coding:utf-8 -*-

import os
import json
import time
import socket
import re
import sys
import requests

if len(sys.argv) < 2:
    print("Please input the name of the monitor process, such as:")
    print("python monitor_proc.py chain33")
    exit(1)
else:
    proc_name = sys.argv[1]

def main():
    ip = socket.gethostname()
    timestamp = int(time.time())
    step = 60
    p = []

    monit_keys = [
        ('pid', 'GAUGE'),
        ('args', 'GAUGE'),
        ('rss', 'GAUGE'),
        ('vsz', 'GAUGE'),
        ('pcpu', 'GAUGE'),
    ]

    for key, vtype in monit_keys:
        tags = ""
        cmd = "ps -e -o comm,'%s' | grep %s | grep -v py | grep -v grep" % (key, proc_name)
        res = os.popen(cmd).read()
        value = re.split(r" +", res)[1:]
        value = ' '.join(value)
        if key == "args":
            tags = value
            value = 0
        else:
            value = float(value)

        if key == "pid" and value == []:
            print("Can't find process.")
            break

        i = {
            'Metric': 'proc.%s' % (key),
            'Endpoint': ip,
            'Timestamp': timestamp,
            'Step': step,
            'Value': value,
            'CounterType': vtype,
            'TAGS': tags
        }
        print(i)
        p.append(i)

    #r = requests.post("http://192.168.3.35:1988/v1/push", json.dumps(p))
    print(r)


if __name__ == '__main__':
    main()
