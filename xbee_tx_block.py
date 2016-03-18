import serial
import xbee
import json
from time import sleep
from nio.signal.base import Signal
from nio.util.discovery import discoverable
from nio.properties import StringProperty, IntProperty
from nio.properties.version import VersionProperty
from nio.util.threading.spawn import spawn
from .xbee_base import XBeeBase


@discoverable
class XBeeTX(XBeeBase):

    """Execute TX Command.

    XBee sends the serialized version of each input signal to thie block. It is
    sent to the configured "Distnation Address" of the XBee. That destination
    XBee will receive that serialized signal. If that block is connected to nio
    then the block will notify the signal.

    Parameters:
        serial_port (str): COM/Serial port the XBee is connected to
    """

    version = VersionProperty(version='0.2.0')

    def process_signals(self, signals):
        for signal in signals:
            data = json.dumps(signal.to_dict()).encode()
            self.logger.debug('Sending data: {}'.format(data))
            # tx: 0x01 "Tx (Transmit) Request: 16-bit address"
            # frame_id: 0x01
            # dest_addr: 0xFFFF appears to make it so that it sends to the
            #    configured "Destination Address" on the XBee
            # data: RF data bytes to be transmitted
            self._xbee.send(
                'tx', frame_id=b'\x01', dest_addr=b'\xFF\xFF', data=data)
