import serial
import time
domain = 'robocademy.com'
sm = ''
import urllib
import urllib2

import sys
import signal
 
class TimeoutException(Exception): 
    pass 
    
def get_serial():
    global sm
    def timeout_handler(signum, frame):
        raise TimeoutException()
 
    old_handler = signal.signal(signal.SIGALRM, timeout_handler) 
    signal.alarm(1) # triger alarm in 3 seconds
 
    try: 
        arduino = serial.Serial('/dev/ttyS0', 9600)
        if arduino.readline():
            sm += '\n' + arduino.readline()
            data = {'content': sm}
            data = urllib.urlencode(data) 
            #print data 
            req = urllib2.Request('http://%s/courses/arduino/set_serial_monitor/' % (domain), data) 
            try:
                resp = urllib2.urlopen(req)
                contents = resp.read()
            except urllib2.HTTPError, error:
                g = open('error.html', 'w')
                
                contents = error.read()
                g.write(contents)
                g.close()
            print contents
            #response = urllib2.urlopen(req)
        del arduino
    except TimeoutException:
        return "default value"
    finally:
        signal.signal(signal.SIGALRM, old_handler) 
 
    signal.alarm(0)
while True:
    time.sleep(1)
    f = open('is_serial_ok.txt', 'r')
    v = f.read().strip()
    print v
    f.close()
    if v == 'true':
        get_serial()
        
    else:
        sm = ''
        data = urllib.urlencode({'content': ''}) 
        #print data 
        req = urllib2.Request('http://%s/courses/arduino/set_serial_monitor/' % (domain), data) 
        resp = urllib2.urlopen(req)
        contents = resp.read()