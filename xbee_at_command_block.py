import binascii
from nio.util.discovery import discoverable
from nio.properties import Property
from nio.properties.version import VersionProperty
from .xbee_base import XBeeBase


@discoverable
class XBeeATCommand(XBeeBase):

    """ Execute AT commands
    Parameters:
        command: The command to execute, ex. 'D0', WR'
        parameter: The command parameter, ex. '05' for 'D0' command
           to set pin high
    """

    version = VersionProperty(version='0.1.0')
    command = Property(title='AT Command (ascii)',
                       default='ID')
    parameter = Property(title='Command Parameter (hex, ex: "05")',
						 default='')

    def process_signals(self, signals):
        for signal in signals:
            try:
                command = self.command(signal)
                parameter = self.parameter(signal).replace(" ", "")
                self._at(command, parameter)
            except:
                self.logger.exception("Failed to execute at command")

    def _at(self, command, parameter):
        command = command.encode('ascii')
        parameter = binascii.unhexlify(parameter)
        self.logger.debug(
            "Executing AT command: {}, with parameter: {}".format(
                command, parameter))
        # at: 0x08 "AT Command"
        # frame_id: 0x08
        # data: RF data bytes to be transmitted
        # command: The command to execute, ex. 'D0', WR'
        # parameter: The command parameter, ex. b'\x05' for 'D0' command
        #    to set pin high
        #
        # frame_id is an arbitrary value, 1 hex byte, used to associate sent
        # packets with their responses. If set to 0 no response will be sent.
        # Could be a block property.
        self._xbee.send('at', frame_id=b'\x01', command=command,
                        parameter=parameter)
