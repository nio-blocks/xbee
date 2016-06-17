import binascii
from nio.common.discovery import Discoverable, DiscoverableType
from nio.metadata.properties import ExpressionProperty
from nio.metadata.properties.version import VersionProperty
from .xbee_base import XBeeBase


@Discoverable(DiscoverableType.block)
class XBeeATCommand(XBeeBase):

    """ Execute AT commands

    Parameters:
        command: The command to execute, ex. 'D0', WR'
        parameter: The command parameter, ex. '05' for 'D0' command
           to set pin high
        dest_addr: 2 byte address of xbee to send AT command too.
            """

    version = VersionProperty(version='0.1.0')
    command = ExpressionProperty(title='AT Command (ascii)',
                                 default='ID')
    parameter = ExpressionProperty(title='Command Parameter (hex, ex: "05")')

    def process_signals(self, signals):
        for signal in signals:
            try:
                command = self.command(signal)
                parameter = self.parameter(signal).replace(" ", "")
                self._at(command, parameter)
            except:
                self._logger.exception("Failed to execute at command")

    def _at(self, command, parameter):
        command = command.encode('ascii')
        parameter = binascii.unhexlify(parameter)
        self._logger.debug(
            "Executing AT command: {}, with parameter: {}".format(
                command, parameter))
        # remote_at: 0x17 "Remote AT Command"
        # frame_id: 0x01
        # dest_addr: 0xFFFF broadcasts to all XBees
        # data: RF data bytes to be transmitted
        # command: The command to execute, ex. 'D0', WR'
        # parameter: The command parameter, ex. b'\x05' for 'D0' command
        #    to set pin high
        self._xbee.send('at', frame_id=b'\x08', command=command, parameter=parameter)
