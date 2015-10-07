import binascii
from nio.common.discovery import Discoverable, DiscoverableType
from nio.metadata.properties import ExpressionProperty
from nio.metadata.properties.version import VersionProperty
from .xbee_base import XBeeBase


@Discoverable(DiscoverableType.block)
class XBeeRemoteAT(XBeeBase):

    """ Execute Remote AT commands

    Parameters:
        command: The command to execute, ex. 'D0', WR'
        parameter: The command parameter, ex. '05' for 'D0' command
           to set pin high
    """

    version = VersionProperty(version='0.1.0')
    command = ExpressionProperty(title='AT Command (ascii)',
                                 default='ID')
    parameter = ExpressionProperty(title='Command Parameter (hex, ex: "05")')

    def process_signals(self, signals):
        for signal in signals:
            try:
                command = self.command(signal)
                parameter = self.parameter(signal)
                self._remote_at(command, parameter)
            except:
                self._logger.exception("Failed to execute remote at command")

    def _remote_at(self, command, parameter=None):
        command = command.encode('ascii')
        parameter = binascii.unhexlify(parameter)
        self._logger.debug(
            "Executing Remote AT command: {}, with parameter: {}".format(
                command, parameter))
        # remote_at: 0x17 "Remote AT Command"
        # frame_id: 0x01
        # dest_addr: 0xFFFF appears to make it so that it sends to the
        #    configured "Destination Address" on the XBee
        # data: RF data bytes to be transmitted
        # command: The command to execute, ex. 'D0', WR'
        # parameter: The command parameter, ex. b'\x05' for 'D0' command
        #    to set pin high
        self._xbee.send(
            'remote_at', frame_id=b'\x01', dest_addr=b'\xFF\xFF',
            command=command, parameter=parameter)
