import os
import time
import sys
def call_code(device_path):
    while True:
        f = open('current.txt', 'r')
        
        i = f.read()
        if not i:
            i = 59
        os.system('python get_users_code.py %s %s' % (i, device_path))
        time.sleep(1)

call_code(sys.argv[1])