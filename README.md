# XBee Blocks

IMPORTANT: If you are using a USB connection to your XBee(s) rather than TTL serial, you first need to install the [FTDI drivers](http://www.ftdichip.com/Support/Documents/AppNotes/AN_134_FTDI_Drivers_Installation_Guide_for_MAC_OSX.pdf) to communicate with the XBEE over USB. You will also want a [USB explorer](https://learn.sparkfun.com/tutorials/exploring-xbees-and-xctu/selecting-an-explorer) to hook up the XBee to your computer.

It is recommended that you use [XCTU](http://www.digi.com/products/wireless-wired-embedded-solutions/zigbee-rf-modules/xctu) to configure the XBees via USB or serial before using in n.io. At the minimum it is necessary to enable API mode to accept AT commands and further configuration settings.

XBee modules need to be configured with AP=2, API w/ PPP, which automatically escapes special characters in transmission. Note: This is NOT the default setting on the XBee.

From the computer terminal, view the serial ports with `ls /dev/tty.*` to discover where your XBee is connected. Ex. `/dev/tty.usbserial-DA013Y6Qdev/tty.usbserial`

## Output

Notifies a signal for each frame read from XBee. Each block in this repository will notify a signal for each api response received at that XBee. For example, XBeeRemoteAT notifies a `remote_at_response` containing the status of the Remote AT command.


XBeeTX
======

Transmit signal through XBee over serial.

Input signals are serialized and transmitted to the destination XBee(s).

Destination XBees notify a signal for each received transmission.

Essentially, this block can be used to send signals from one nio instance to another.

Properties
----------

-   **serial_port**: COM/Serial port of XBee. From the computer terminal, view the available ports with `ls /dev/tty.*`. Ex. `/dev/tty.usbserial-DA013Y6Q`

Dependencies
------------

-   [XBee](https://pypi.python.org/pypi/XBee)

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

  - **id**: The type of response.

#### rx\_id\_data
  - **rssi**: RF signal strength
  - **source_addr**: Which XBee sent the signal
  - **samples**: A list of readings from each enabled IO pin. Each item of the list is a dictionary of readings for all the enabled IO pins. Keys are of format (adc|dio)-[0-8]
  - **options**: ???

```
{
  'id': 'rx_io_data',
  'samples': [{'adc-0': 525, 'adc-3': 390, 'adc-1': 472, 'adc-5': 312, 'adc-4': 410, 'adc-2': 437}],
  'options': b'\x00', 
  'rssi': b'2',
  'source_addr': b'\x00\x01'}
}

```

***

XBeeATCommand
=============

Send [AT commands](http://examples.digi.com/wp-content/uploads/2012/07/XBee_ZB_ZigBee_AT_Commands.pdf) to a local XBee.

Properties
----------

-   **serial_port**: COM/Serial port of XBee. From the computer terminal, view the available ports with `ls /dev/tty.*`. Ex. `/dev/tty.usbserial-DA013Y6Q`
-   **command**: The command to execute, ex. `D0`, `WR`.
-   **parameter**: The command parameter, ex. `05` for `D0` command to set pin high.

Dependencies
------------

-   [XBee](https://pypi.python.org/pypi/XBee)

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

  - **id**: The type of response.

#### at_response

Each AT Command will notify a response signal.

```
{
  'id': 'at_response',
  'frame_id': b'\x88',
  'status': b'\x00',
  'command': b'D0'
 }
```

Each response includes a status, with the following possible values:
- `00 OK`
- `01 Error`
- `02 Invalid Command`
- `03 Invalid Parameter`
- `04 No Response`

***

XBeeRemoteAT
============

Send [Remote AT commands](http://examples.digi.com/wp-content/uploads/2012/07/XBee_ZB_ZigBee_AT_Commands.pdf) to a destination XBee.

Properties
----------

-   **serial_port**: COM/Serial port of XBee. From the computer terminal, view the available ports with `ls /dev/tty.\*`. Ex. `/dev/tty.usbserial-DA013Y6Q`
-   **command**: The command to execute, ex. `D0`, `WR`.
-   **parameter**: The command parameter, ex. `05` for `D0` command to set pin high.
-   **dest_addr**: 2 byte address of remote XBee to send AT command too. Default value when left blank is `FF FF` which sends a broadcast.

Dependencies
------------

-   [XBee](https://pypi.python.org/pypi/XBee)

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

  - **id**: The type of response.

#### remote\_at\_response

Each Remote AT Command will notify a response signal for each remote XBee. This can be many XBees when broadcasting to `dest_addr` `FF FF`.

```
{
  'id': 'remote_at_response',
  'frame_id': b'\x01',
  'source_addr_long': b'\x00\x13\xa2\x00@\xc1S\x05',
  'status': b'\x00',
  'command': b'D0',
  'source_addr': b'\x00\x03'
}
```

Each response includes a status, with the following possible values:
- `00 OK`
- `01 Error`
- `02 Invalid Command`
- `03 Invalid Parameter`
- `04 No Response`
