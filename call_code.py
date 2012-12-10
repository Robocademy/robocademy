import os
import time
import sys
def call_code(device_path, connection_id):
    while True:
        i = 1
        try:
            f = open('current_%s.txt' % (connection_id), 'r')
            
            i = f.read()
        except:
            i = 1
        if not i:
            i = 1
        cmd = 'python get_users_code.py %s %s %s' % (i, device_path, connection_id)
        print cmd
        os.system(cmd)
        time.sleep(1)

call_code(sys.argv[1], sys.argv[2] )