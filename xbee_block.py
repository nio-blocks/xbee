import serial
import xbee
from nio.common.block.base import Block
from nio.common.signal.base import Signal
from nio.common.discovery import Discoverable, DiscoverableType
from nio.metadata.properties import StringProperty, IntProperty
from nio.metadata.properties.version import VersionProperty


@Discoverable(DiscoverableType.block)
class XBee(Block):

    """ Read XBee over serial.

    Parameters:
        serial_port (str): COM/Serial port the XBee is connected to
    """

    version = VersionProperty(version='0.1.1')
    serial_port = StringProperty(name='COM/Serial Port',
                                 default='/dev/ttyAMA0')
    baud_rate = IntProperty(name='Baud Rate', default=9600, hidden=True)

    def __init__(self):
        super().__init__()
        self._xbee = None
        self._serial = None

    def configure(self, context):
        super().configure(context)
        self._serial = serial.Serial(self.serial_port, self.baud_rate)
        self._xbee = xbee.XBee(self._serial,
                               callback=self._callback,
                               escaped=True)

    def stop(self):
        try:
            self._logger.debug('Halting XBee callback thread')
            self._xbee.halt()
            self._logger.debug('XBee halted')
        except:
            self._logger.exception('Exception while halting xbee')
        try:
            self._serial.close()
        except:
            self._logger.exception('Exception while closing serial connection')
        super().stop()

    def _callback(self, response):
        try:
            self.notify_signals([Signal(response)])
        except:
            self._logger.exception(
                'Response is not valid: {}'.format(response))
