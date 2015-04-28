import serial
import xbee
from nio.common.block.base import Block
from nio.common.signal.base import Signal
from nio.common.discovery import Discoverable, DiscoverableType
from nio.metadata.properties import StringProperty
from nio.metadata.properties.version import VersionProperty
from nio.modules.threading import spawn


@Discoverable(DiscoverableType.block)
class XBee(Block):

    """ Read XBee over serial.

    Parameters:
        serial_port (str): COM/Serial port the XBee is connected to
    """

    version = VersionProperty(version='0.1.0')
    serial_port = StringProperty(name='COM/Serial Port',
                                 default='/dev/ttyAMA0')

    BAUDRATE = 9600

    def __init__(self):
        super().__init__()
        self.xbee = None
        self.ser = None

    def configure(self, context):
        super().configure(context)
        self.ser = serial.Serial(self.serial_port, self.BAUDRATE)
        self.xbee = xbee.XBee(self.ser)

    def start(self):
        super().start()
        spawn(self._read)

    def stop(self):
        try:
            self.ser.close()
        except:
            self._logger.exception('Exception while closing serial connection')
        super().stop()

    def _read(self):
        while True:
            try:
                response = self.xbee.wait_read_frame()
                self.notify_signals([Signal(response)])
            except:
                break
