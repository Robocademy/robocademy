i = None
import time 
import os
import re
from datetime import datetime
import urllib2
import urllib
import sys
import os

domain = 'robocademybackup.rs.af.cm'
domain = 'robocademy.com'

def download(i, device_path):
    
    #global i
    
    
    localFile = open('/home/tim/tmprcc/src/sketch.ino', 'w')
    url = 'http://%s/courses/arduino/get_code/' % (domain)
    # I'm having trouble getting the current version of get_code, cache problems, tried a bunch of things like urllib.urlclean, so now trying
    # wget --cache=off
    os.system('wget --no-cache --user-agent="Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)" --cookies=on --load-cookies=cookies.txt %s' % url)
    f = open('index.html', 'r')
    code = f.read()
    f.close()
    os.system('rm index.html')
    #request = urllib2.Request(url)
    #request.add_header('User-Agent', 'Mozilla/5.0')
    #code = urllib2.build_opener().open(request).read()
    #print code
    print datetime.time(datetime.now()), code.split('\n')[0]
    if code != 'None' and re.match('\d+', code.split('\n')[0]):
        if i is None or int(code.split('\n')[0]) != i:
            print 'Doing'
            f = open('is_serial_ok.txt', 'w')
            f.write('false')
            f.close()
            localFile = open('/home/tim/tmprcc/src/sketch.ino', 'w')
            localFile.write('\n'.join(code.split('\n')[1:]))
            #webFile.close()
            localFile.close()
            #os.system('cd /home/tim/tmprcc/; ino build; ino upload')
            #display out put line by line
            import subprocess
            # 'source', '/home/tim/djangoenv/bin/activate', 
            proc = subprocess.Popen(['cd /home/tim/tmprcc/; ino build; ino upload -p /dev/%s' % (device_path)], stderr=subprocess.STDOUT, stdout = subprocess.PIPE , shell=True)
            
            status = ''
            #print subprocess.PIPE
            #print proc.stdout.read()

            #print response
            #print '=================Start of test===================='
            for line in iter(proc.stdout.readline,''):
                print line
                status += '\n' + line.rstrip()
                data = {'status': status}
                data = urllib.urlencode(data) 
                #print data 
                req = urllib2.Request('http://%s/courses/arduino/set_cmd_status/' % (domain), data) 
                response = urllib2.urlopen(req)
            f = open('is_serial_ok.txt', 'w')
            f.write('true')
            f.close()
            urllib.urlopen('http://robocademy.com/courses/arduino/set_status/').read()
            f = open('current.txt', 'w')
            
            i = code.split('\n')[0]
            f.write(i)
            f.close()            
    
#print sys.argv[1]
download(int(sys.argv[1]), sys.argv[2])