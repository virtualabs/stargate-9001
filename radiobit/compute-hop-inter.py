import radio
import time
from microbit import *

def tohex(p):
  return ''.join(['%02x'%c for c in p])

# enable radio (RX)
radio.on()

# enable xn297 compatibility
radio.cx()
radio.config(channel=0x45)

n=0
start=0
stop=0
while True:

  pkt = radio.receive()
  if pkt is not None:
    if pkt[0]==0x93:
      if n==0:
        start=running_time()
      n += 1
      if n==50:
        stop=running_time()
        interval = (stop-start)/50
        print('interval: %0.2f' % interval)
        break

print('done')
while True:
  pass