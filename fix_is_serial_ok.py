while True:
    import time
    time.sleep(5 * 60)
    f = open('is_serial_ok.txt', 'w')
    f.write('true')
    f.close()
