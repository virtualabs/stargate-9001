SG901 RF protocol
=================

Binding process
---------------

Binding is performed on channel 0, the controller send the following packet:

  00 AA 40 07 00 00 00 00 00 00 00 00 00 00 00 00

0x4007 is supposed to be the controller ID.

The drone answers back with its own ID (0x93) in a packet on channel 0:

  00 BB 40 07 93 89 00 00 00 00 00 00 00 00 00 00

Last, the remote controller sends a synchronization packet on channel 0, containing the channel hopping sequence (0x44, 0x4E, 0x4C, 0x45)

  93 00 89 0A 44 4E 4C 45 00 00 40 44 A5 4E 40 07

Once the binding performed, the remote controller keeps sending orders on these channels.


Channel hopping mechanism
-------------------------

The remote controller loops over 4 channels, 6ms/channel (~24ms/cycle), and each packet sent over a channel specifies the next channel
used in the hopping sequence:

```
93 4e 89 0a 80 80 80 08 14 44 60 e0 44 f5 4a 91
   ^
   next channel
```

Data packet format
------------------

The packet contains the following information:

* throttle, roll, pitch and yaw stick positions
* the current selected speed
* the state of various buttons
* a 8-bit CRC
* the controller and drone IDs


| Offset | Example value | Description                                                 |
|--------|---------------|-------------------------------------------------------------|
| +0x00  | 0x93          | drone ID, bits 0-7                                          |
| +0x01  | 0x4e          | Next channel                                                |
| +0x02  | 0x89          | drone ID, bits 8-15                                         |
| +0x03  | 0x0a          | checksum (bits 8-15)                                        |
| +0x04  | 0x01          | throttle (0x00 to 0xff)                                     |
| +0x05  | 0x80          | roll (bit 7 set to 1 indicates a positive value)            |
| +0x06  | 0x80          | pitch (bit 7 set to 1 indicates a positive value)           |
| +0x07  | 0x80          | yaw (bit 7 set to 1 indicates a positive value)             |
| +0x08  | 0x00          | auto take-off/landing, set to 0x40 if enabled               |
| +0x09  | 0x00          | unknown                                                     |
| +0x0A  | 0x40          | unknown                                                     |
| +0x0B  | 0x44          | unknown                                                     |
| +0x0C  | 0x00          | current selected speed (0x00: 40%, 0x01:75%, 0x02:100%)     |
| +0x0D  | 0x55          | 8-bit checksum (see reversed algorithm)                     |
| +0x0E  | 0x40          | controller ID bits 0-7                                      |
| +0x0F  | 0x07          | controller ID bits 8-15                                     |


CRC algorithm
-------------

``` python
def checksum(pkt):
  _pkt = list(pkt)
  _pkt[3] = 0x0
  cs = 0xe6
  for b in _pkt:
    cs = (cs + b)
  return (((cs>>8)<<2)-6, cs&0xff)
```