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
count = 0
nb_channels = 0

while True:

  if channel == 0:
    nb_channels = 0

  # Timeout reached ?
  stop = running_time()
  if stop - start > 5000:
    # Show stats
    if count>0:
      print('channel %d: %d' % (channel, count))
      nb_channels += 1

    # Jump to next channel
    channel = (channel + 1)%80
    radio.config(channel=channel)
    start = stop
    count = 0

    if channel == 0:
      print('Nb channels: %d' % nb_channels)

  pkt = radio.receive()
  if pkt is not None:
    count += 1
  del pkt
