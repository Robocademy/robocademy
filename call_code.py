import os
import time
import sys
def call_code(device_path, connection_id):
    while True:
        f = open('current.txt', 'r')
        
        i = f.read()
        if not i:
            i = 0
        os.system('python get_users_code.py %s %s %s' % (i, device_path, connection_id))
        time.sleep(1)

call_code(sys.argv[1], sys.argv[2] )