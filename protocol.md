# Reset XN297L
FC 00: CE_FSPI_OFF
53 5A: RST_FSPI_HOLD 
53 A5: RST_FSPI_RELS

# Configuration
22 01: Enable data pipe 0 (EN_RXADDR)
23 03: Set address length to 5 bytes (SETUP_AW)
31 10: Set RX payload size to 16 bytes (RX_PW_P0)
30 CC CC CC CC CC: Set Transmit Address to CC:CC:CC:CC:CC (TX_ADDR)
2A CC CC CC CC CC: Set PIPE0 RX Address to CC:CC:CC:CC:CC (RX_ADDR_P0)
3C 00: Set static packet length (DYNPD)
26 3F: Set bitrate to 1Mbps (RF_SETUP)
24 00: Disable retransmit (SETUP_RETR)
21 00: Set no auto-ack (EN_AA)

# Calibration data
3F 0A 6D 67 9C 46: Set BB_CAL (calibration)
3E F6 37 5D:  Set RF_CAL  (calibration)
3A 45 21 EF 2C 5A 5C: Set RF_CAL2 (calibration)
39 01: Set DEMOD_CAL  (calibration)
3B 0B DF 02: Set DEM_CAL2 (calibration)

FC 00: CE_FSPI_OFF
20 0E: Enable CRC, 2-byte CRC, PTX mode ON (transmit)
00 0E: Read CONFIG register (0x0E returned)
27 70: Clear RX_DR, TX_DS, MAX_RT (STATUS)
25 00: Set RF_CH to 0 (Channel: 0)
FC 00: CE_FSPI_OFF
20 8E: Enter STB3 (Standby-III mode)
FD 00: CE_FSPI_ON
A0 00 AA 40 07 00 00 00 00 00 00 00 00 00 00 00 00: Transmit payload 00 AA 40 07 00 ... 00 <16 bytes>
FD 00: CE_FSPI_ON

# Wait 1s

FC 00: CE_FSPI_OFF


FC 00: CE_FSPI_OFF
20 0E: Enable CRC, 2-byte CRC, PTX mode ON (transmit)
00 0E: Read CONFIG register (0x0E returned)
27 70: Clear RX_DR, TX_DS, MAX_RT (STATUS)
25 00: Set RF_CH to 0 (Channel: 0)
FC 00: CE_FSPI_OFF
20 8E: Enter STB3 (Standby-III mode)
FD 00: CE_FSPI_ON
A0 00 AA 40 07 00 00 00 00 00 00 00 00 00 00 00 00: Transmit payload 00 AA 40 07 00 ... 00 <16 bytes>
FD 00: CE_FSPI_ON

FC 00:


....


# Binding process (channel 0)

First, the remote controller sends an advertising packet on channel 0:

  00 AA 40 07 00 00 00 00 00 00 00 00 00 00 00 00

The drone answers back with its own ID (0x93) in a packet on channel 0:

  00 BB 40 07 93 89 00 00 00 00 00 00 00 00 00 00

Last, the remote controller sends a synchronization packet on channel 0, containing the channel hopping sequence (0x44, 0x4E, 0x4C, 0x45)

  93 00 89 0A 44 4E 4C 45 00 00 40 44 A5 4E 40 07

Once the binding performed, the remote controller keeps sending orders on these channels.


# Channel hopping mechanism

The remote controller loops over 4 channels, 6ms/channel (~24ms/cycle), and each packet sent over a channel specifies the next channel
used in the hopping sequence:

```
93 4e 89 0a 80 80 80 08 14 44 60 e0 44 f5 4a 91
   ^
   next channel
```



