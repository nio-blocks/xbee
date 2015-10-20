import serial
import xbee
import json
from time import sleep
from nio.common.signal.base import Signal
from nio.common.discovery import Discoverable, DiscoverableType
from nio.metadata.properties import StringProperty, IntProperty
from nio.metadata.properties.version import VersionProperty
from nio.modules.threading import spawn
from .xbee_base import XBeeBase


@Discoverable(DiscoverableType.block)
class XBee(XBeeBase):

    """ Read XBee over serial.

    Parameters:
        serial_port (str): COM/Serial port the XBee is connected to
    """

    version = VersionProperty(version='0.2.0')

    def process_signals(self, signals):
        for signal in signals:
            data = json.dumps(signal.to_dict()).encode()
            self._logger.debug('Sending data: {}'.format(data))
            # tx: 0x01 "Tx (Transmit) Request: 16-bit address"
            # frame_id: 0x01
            # dest_addr: 0xFFFF appears to make it so that it sends to the
            #    configured "Destination Address" on the XBee
            # data: RF data bytes to be transmitted
            self._xbee.send(
                'tx', frame_id=b'\x01', dest_addr=b'\xFF\xFF', data=data)
