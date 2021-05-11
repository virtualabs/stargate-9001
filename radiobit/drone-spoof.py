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

def disp_pkt(p):
  crc1 = pkt[3]
  crc2 = pkt[13]
  crc1_,crc2_ = checksum(pkt[:13])
  crc_valid = ((crc1==crc1_) and (crc2==crc2_))
  t,r,p,y = p[4:8]
  if r&0x80:
    r = r&0x7f
  else:
    r = -(r&0x7f)
  if p&0x80:
    p = p&0x7f
  else:
    p = -(p&0x7f)
  if y&0x80:
    y = y&0x7f
  else:
    y = -(y&0x7f)
  print('throt: %03d roll: %03d pitch: %03d yaw: %03d (crc: %s)' % (t,r,p,y,crc_valid))

# enable radio (RX)
radio.on()

# enable xn297 compatibility
radio.cx()
radio.config(channel=0)

# State
state = 0
channel = 0
bound = False
channels = []
print('> Wait for binding ...')
while not bound:
  pkt = radio.receive()
  if pkt is not None:
    #disp_pkt(pkt, True)
    if pkt[0] == 0x00 and pkt[1] == 0xAA:
      while not bound:
        binding_resp = bytes([0x00, 0xBB, 0x40, 0x07, 0x93, 0x89, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
        radio.send(binding_resp)
        pkt = radio.receive()
        if pkt is not None:
          #disp_pkt(pkt, True)
          if pkt[0] == 0x93:
            channels = list(pkt[4:8])
            channel = channels[0]
            radio.config(channel=channel)
            print('> Tx OK (%02x)' % channel)
            bound = True

# channel hopping
print('> Ready for RX')
while True:
  pkt = radio.receive()
  if pkt is not None:
    if pkt[0] == 0x93 and pkt[1]>0x00:
      disp_pkt(pkt)
      next_channel = pkt[1]
      del pkt
      channel = next_channel
      radio.config(channel=channel)















