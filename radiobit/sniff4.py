import radio
import time
from microbit import *

def tohex(p):
  return ''.join(['%02x'%c for c in p])

# enable radio (RX)
radio.on()

# enable xn297 compatibility
radio.cx()
radio.config(channel=0)

channel = 0
radio.config(channel=0x45)

while True:

  pkt = radio.receive()
  if pkt is not None:
    if pkt[0]==0x93:
      print('%d - %s' % (running_time(), tohex(pkt[:16])))
  del pkt
