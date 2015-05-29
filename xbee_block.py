import serial
import xbee
import json
from time import sleep
from nio.common.block.base import Block
from nio.common.signal.base import Signal
from nio.common.discovery import Discoverable, DiscoverableType
from nio.metadata.properties import StringProperty, IntProperty
from nio.metadata.properties.version import VersionProperty
from nio.modules.threading import spawn


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
        self._reconnect_delay = 1

    def configure(self, context):
        super().configure(context)
        self._connect()

    def process_signals(self, signals):
        for signal in signals:
            data = json.dumps(signal.to_dict()).encode()
            self._logger.debug('Sending data: {}'.format(data))
            self._xbee.send(
                'tx', frame_id=b'\x01', dest_addr=b'\xFF\xFF', data=data)

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

    def _connect(self):
        ''' Establish XBee serial connection '''
        try:
            self._serial = serial.Serial(self.serial_port, self.baud_rate)
            self._logger.debug(
                'Establish serial connection with XBee'
                ': {}'.format(self.serial_port))
            try:
                self._xbee = xbee.XBee(self._serial,
                                       callback=self._callback,
                                       escaped=True,
                                       error_callback=self._error_callback)
            except:
                # xbee on pypi does not have error_callback
                self._xbee = xbee.XBee(self._serial,
                                       callback=self._callback,
                                       escaped=True)
                self._logger.exception(
                    'XBee conenctecion established but the xbee library on pypi'
                    ' does not have error_callback. For improved performance,'
                    ' try using http://github.com:neutralio/python-xbee.git')
            self._reconnect_delay = 1
        except:
            self._logger.exception('Failed to establish XBee connection')
            self._reconnect()

    def _callback(self, response):
        try:
            self.notify_signals([Signal(response)])
        except:
            self._logger.exception(
                'Response is not valid: {}'.format(response))

    def _error_callback(self, e):
        self._logger.error('XBee thread unexpectedly ended: {}'.format(e))
        self._reconnect()

    def _reconnect(self):
        self._logger.debug(
            'Attempting reconnect in {} seconds'.format(self._reconnect_delay))
        sleep(self._reconnect_delay)
        self._reconnect_delay *= 2
        spawn(self._connect)
