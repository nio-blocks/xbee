import serial
import xbee
from nio.common.block.base import Block
from nio.common.signal.base import Signal
from nio.common.signal.status import BlockStatusSignal
from nio.common.block.controller import BlockStatus
from nio.common.discovery import Discoverable, DiscoverableType
from nio.metadata.properties import StringProperty, IntProperty
from nio.metadata.properties.version import VersionProperty
from nio.modules.threading import spawn, Event


@Discoverable(DiscoverableType.block)
class XBee(Block):

    """ Read XBee over serial.

    Parameters:
        serial_port (str): COM/Serial port the XBee is connected to
    """

    version = VersionProperty(version='0.1.0')
    serial_port = StringProperty(name='COM/Serial Port',
                                 default='/dev/ttyAMA0')
    baud_rate = IntProperty(name='Baud Rate', default=9600, hidden=True)

    def __init__(self):
        super().__init__()
        self._xbee = None
        self._ser = None
        self._stop_event = Event()

    def configure(self, context):
        super().configure(context)
        self._ser = serial.Serial(self.serial_port, self.baud_rate)
        self._xbee = xbee.XBee(self._ser)

    def start(self):
        super().start()
        spawn(self._read)

    def stop(self):
        self._stop_event.set()
        try:
            self._ser.close()
        except:
            self._logger.exception('Exception while closing serial connection')
        super().stop()

    def _read(self):
        while True:
            if self._stop_event.is_set():
                # Stop reading on block stop
                break
            try:
                response = self._xbee.wait_read_frame()
                self.notify_signals([Signal(response)])
            except:
                self._logger.exception('Failed reading from Xbee. Aborting...')
                self.notify_management_signal(BlockStatusSignal(
                    BlockStatus.error, 'Failed to read Xbee'))
                break
