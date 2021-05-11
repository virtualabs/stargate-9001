import radio
import time
from microbit import *

def checksum(pkt):
  _pkt = list(pkt)
  _pkt[3] = 0x0
  cs = 0xe6
  for b in _pkt:
    cs = (cs + b)
  return (((cs>>8)<<2)-6, cs&0xff)

def disp_pkt2(p):
  print(''.join(['%02x' % c for c in p]))

def craft_packet(throttle=0x80, roll=0x80, pitch=0x80, yaw=0x80, next_channel=0x44):
  pkt = [
    0x93, # drone id (part 1)
    next_channel,
    0x89, # drone id (part 2)
    0x00, # checksum (part 1)
    throttle,
    roll,
    pitch,
    yaw,
    0x00, # auto takeoff/landing
    0x00, # unk
    0x40, # unk
    0x44, # unk
    0x00, # speed
    0x00, # checksum (part 2)
    0x40,
    0x07
  ]

  # add checksum
  b0,b1 = checksum(pkt[:13])
  pkt[3] = b0
  pkt[13] = b1

  return bytes(pkt)


# enable radio (RX)
radio.on()

# enable xn297 compatibility
radio.cx()
radio.config(channel=0x44)


while True:
  p = craft_packet(next_channel=0x13)
  radio.send(p)





