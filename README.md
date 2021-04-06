StarGate 9001 (Goolsky SG901 hardware/software reverse-engineering Project)
===========================================================================

## Hardware reverse-engineering

The Goolsky SG901 is composed of:
* a 2.4GHz remote controller
* a quadcopter including a 2.4GHz receiver + a WiFi IP camera

### Remote controller

The remote controller is based on an unknown MCU that exposes 5 test points named *G* (ground), *3.3V* (Vcc), *D* (Data ?), *C* (Clock) and *E* (Enable?).
These test points are directly accessible on the single-layer PCB.

This unknown MCU communicates with a XN297 2.4GHz transceiver chip over SPI (to be confirmed). Datasheet is included in the *datasheets* folder.


### Quadcopter Flight Contoller

The Quadcopter Flight Controller is based on PAN159CY (datasheet included in the *datasheets* folder), and uses a 3-axis accelerometer and 2x2 ESCs.


### On-board Camera

The on-board is a WiFi IP camera based on an Intellichip A7 SoC and a XR819 WiFi modem.
The Intellichip A7 uses an external flash memory.


