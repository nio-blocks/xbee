from nio.properties import Property
from nio.properties.version import VersionProperty
from .xbee_base import XBeeBase


class XBeeTX(XBeeBase):

    """Execute TX Command.

    XBee sends the serialized version of each input signal to thie block. It is
    sent to the configured "Distnation Address" of the XBee. That destination
    XBee will receive that serialized signal. If that block is connected to nio
    then the block will notify the signal.

    Parameters:
        dest_addr: 2 byte address of remote xbee to send AT command too.
            Default value when left blank is "FF FF" which sends a broadcast.
    """

    version = VersionProperty(version='0.2.1')
    data = Property(title="Data", default="{{ $.to_dict() }}")

    def process_signals(self, signals):
        for signal in signals:
            data_encoded = "{}".format(self.data(signal)).encode()
            self.logger.debug('Sending data: {}'.format(data_encoded))
            # tx: 0x01 "Tx (Transmit) Request: 16-bit address"
            # frame_id: 0x01
            # dest_addr: 0xFFFF appears to make it so that it sends to the
            #    configured "Destination Address" on the XBee
            # data: RF data bytes to be transmitted
            self._xbee.send('tx',
                            frame_id=b'\x01',
                            dest_addr=b'\xFF\xFF',
                            data=data_encoded)