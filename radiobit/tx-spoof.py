import radio
import time
from microbit import *

channel_id = 0
channels = [0x44, 0x4E, 0x4C, 0x45]

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
radio.config(channel=0)

adv = bytes([0x00, 0xAA, 0x40, 0x07, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
bind = bytes([0x93, 0x00, 0x89, 0x0A, 0x44, 0x4E, 0x4C, 0x45, 0x00, 0x00, 0x40, 0x44, 0xA5, 0x4E, 0x40, 0x07])

bound = False
while not bound:
  # Tx advertisement
  
  radio.send(adv)
  pkt = radio.receive()
  if pkt is not None:
    if pkt[0]==0x00 and pkt[1]==0xBB:
      #disp_pkt2(pkt[:16])
      time.sleep(0.01)
      for i in range(37):
        time.sleep(0.006)
        radio.send(bind)
      bound = True
 
while True:
  radio.config(channel=channels[channel_id])
  time.sleep(0.006)
  #p = craft_packet(throttle=0xff, next_channel=channels[(channel_id+1)%4])
  p = craft_packet(throttle=0xff,next_channel=channels[channel_id])
  radio.send(p)
  #disp_pkt2(p)
  #channel_id = (channel_id + 1)%4





