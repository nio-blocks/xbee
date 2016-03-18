import serial
import xbee
import json
from time import sleep
from nio.block.base import Block
from nio.signal.base import Signal
from nio.properties import StringProperty, IntProperty
from nio.properties.version import VersionProperty
from nio.util.threading.spawn import spawn


class XBeeBase(Block):

    """ Read XBee over serial.

    Parameters:
        serial_port (str): COM/Serial port the XBee is connected to
    """

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
            pass

    def stop(self):
        try:
            self.logger.debug('Halting XBee callback thread')
            self._xbee.halt()
            self.logger.debug('XBee halted')
        except:
            self.logger.exception('Exception while halting xbee')
        try:
            self._serial.close()
        except:
            self.logger.exception('Exception while closing serial connection')
        super().stop()

    def _connect(self):
        ''' Establish XBee serial connection '''
        try:
            self._serial = serial.Serial(self.serial_port(), self.baud_rate())
            self.logger.debug(
                'Establish serial connection with XBee'
                ': {}'.format(self.serial_port()))
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
                self.logger.exception(
                    'XBee connection established but the xbee library on pypi'
                    ' does not have error_callback. For improved performance,'
                    ' try using http://github.com:neutralio/python-xbee.git')
            self._reconnect_delay = 1
        except:
            self.logger.exception('Failed to establish XBee connection')
            self._reconnect()

    def _callback(self, response):
        try:
            self.notify_signals([Signal(response)])
        except:
            self.logger.exception(
                'Response is not valid: {}'.format(response))

    def _error_callback(self, e):
        self.logger.error('XBee thread unexpectedly ended: {}'.format(e))
        self._reconnect()

    def _reconnect(self):
        self.logger.debug(
            'Attempting reconnect in {} seconds'.format(self._reconnect_delay))
        sleep(self._reconnect_delay)
        self._reconnect_delay *= 2
        spawn(self._connect)
