import radio
import time
from microbit import *

# enable radio (RX)
radio.on()

# enable xn297 compatibility
radio.cx()
radio.config(channel=0)

channel = 0
start = running_time()
radio.config(channel=channel)
channels = []

while True:

  if channel == 0:
    nb_channels = 0

  # Timeout reached ?
  stop = running_time()
  if stop - start > 200:   
    # Jump to next channel
    channel = (channel + 1)%80
    radio.config(channel=channel)
    start = stop

    # Show stats
    if channel == 0:
      print(channels)


  pkt = radio.receive()
  if pkt is not None:
    next_chan = pkt[1]
    print('pkt next chan %02x on channel %02x' % (next_chan, channel))
    if channel not in channels and pkt[0]==0x93:
      channels.append(channel)
  del pkt
