XBee Blocks
===========

IMPORTANT: You first need to install the [FTDI drivers](http://www.ftdichip.com/Support/Documents/AppNotes/AN_134_FTDI_Drivers_Installation_Guide_for_MAC_OSX.pdf) to communicate with the XBEE over USB. You will also want a [USB explorer](https://learn.sparkfun.com/tutorials/exploring-xbees-and-xctu/selecting-an-explorer) to hook up the XBee to your computer.

It is recommended that use use [XCTU](http://www.digi.com/products/wireless-wired-embedded-solutions/zigbee-rf-modules/xctu) to configure the XBees before using in n.io.

The XBee needs to be in API Mode. Note: This is NOT the default setting on the XBee.

From the computer terminal, view the serial ports with `ls /dev/tty.*` to discover where your XBee is connected. Ex. /dev/tty.usbserial-DA013Y6Qdev/tty.usbserial

-------------------------------------------------------------------------------

XBee
====

Read/Write XBee over serial.

Input signals are serialized and transmitted to the destination XBee(s).

Destination XBees notify a signal for each received transmission.

Essentially, this block can be used to send signals from one nio instance to another.

Properties
----------

-   **serial_port**: COM/Serial port of XBee. From the computer terminal, view the available ports with `ls /dev/tty.*`. Ex. /dev/tty.usbserial-DA013Y6Q

Dependencies
------------

-   [xbee](https://pypi.python.org/pypi/XBee)

Commands
--------
None

Input
-----
None

Output
------

### default

Notifies a signal for each frame read from XBee. Official Signal response information can be seen in the `api_responses` of the [source code]('https://github.com/nioinnovation/python-xbee/blob/master/xbee/ieee.py').

  - id: The type of response.

#### rx_id_data
  - rssi: RF signal strength
  - source_addr: Which XBee sent the signal
  - samples: A list of readings from each enabled IO pin. Each item of the list is a dictionary of readings for all the enabled IO pins. Keys are of format (adc|dio)-[0-8]
  - options: ???

```
{
  'id': 'rx_io_data',
  'samples': [{'adc-0': 525, 'adc-3': 390, 'adc-1': 472, 'adc-5': 312, 'adc-4': 410, 'adc-2': 437}],
  'options': b'\x00', 
  'rssi': b'2',
  'source_addr': b'\x00\x01'}
}

```

-------------------------------------------------------------------------------

XBeeATCommand
============

Send AT commands to a local XBee.

http://examples.digi.com/wp-content/uploads/2012/07/XBee_ZB_ZigBee_AT_Commands.pdf

Properties
----------

-   **serial_port**: COM/Serial port of XBee. From the computer terminal, view the available ports with `ls /dev/tty.*`. Ex. /dev/tty.usbserial-DA013Y6Q
-   **command**: The command to execute, ex. 'D0', WR'.
-   **parameter**: The command parameter, ex. '05' for 'D0' command to set pin high.

Dependencies
------------

-   [xbee](https://pypi.python.org/pypi/XBee)

Commands
--------
None

Input
-----
Any list of signals.

Output
------

### default

Notifies a signal for each frame read from XBee. Official Signal response information can be seen in the `api_responses` of the [source code]('https://github.com/nioinnovation/python-xbee/blob/master/xbee/ieee.py').

  - id: The type of response.

#### at_response

Each AT Command will notify a response signal.

```
{
  'id': 'at_response',
  'frame_id': b'\x88',
  'status': b'\x00',
  'command': b'D0',
 }
```

-------------------------------------------------------------------------------

XBeeRemoteAT
============

Send Remote AT commands to a destination XBee.

http://examples.digi.com/wp-content/uploads/2012/07/XBee_ZB_ZigBee_AT_Commands.pdf

Properties
----------

-   **serial_port**: COM/Serial port of XBee. From the computer terminal, view the available ports with `ls /dev/tty.*`. Ex. /dev/tty.usbserial-DA013Y6Q
-   **command**: The command to execute, ex. 'D0', WR'.
-   **parameter**: The command parameter, ex. '05' for 'D0' command to set pin high.
-   **dest_addr**: 2 byte address of remote xbee to send AT command too. Default value when left blank is "FF FF" which sends a broadcast.

Dependencies
------------

-   [xbee](https://pypi.python.org/pypi/XBee)

Commands
--------
None

Input
-----
Any list of signals.

Output
------

### default

Notifies a signal for each frame read from XBee. Official Signal response information can be seen in the `api_responses` of the [source code]('https://code.google.com/p/python-xbee/source/browse/xbee/ieee.py').

  - id: The type of response.

#### remote_at_response

Each Remote AT Command will notify a response signal for each remote XBee. This can be many XBees when broadcasting to dest_addr "FF FF".

```
{
  'id': 'remote_at_response',
  'frame_id': b'\x01',
  'source_addr_long': b'\x00\x13\xa2\x00@\xc1S\x05',
  'status': b'\x00',
  'command': b'D0',
  'source_addr': b'\x00\x03',
}
```
