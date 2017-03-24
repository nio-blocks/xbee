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
        dest_addr: address of remote xbee to send AT command too.
            Default value when left blank is "FF FF" which sends a broadcast
            or the "Destination Address" configured in the XBee
    """

    version = VersionProperty(version='0.2.1')
    data = Property(title="Data", default="{{ $.to_dict() }}")
    # todo: make dest_addr a block property

    def process_signals(self, signals):
        for signal in signals:
            data_encoded = "{}".format(self.data(signal)).encode()
            self.logger.debug('Sending data: {}'.format(data_encoded))
            if self.digimesh():
                self._xbee.send('tx',
                                id=b'\x10',
                                frame_id=b'\x01',
                                dest_addr=b'\x00\x00\x00\x00\x00\x00\xFF\xFF',
                                reserved=b'\xFF\xFE',
                                broadcast_radius=b'\x00',
                                options=b'\x00',
                                data=data_encoded)
            else:
                self._xbee.send('tx',
                                id=b'\x01',
                                frame_id=b'\x01',
                                dest_addr=b'\xFF\xFF',
                                options=b'\x00',
                                data=data_encoded)
