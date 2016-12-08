import binascii
from nio.util.discovery import discoverable
from nio.properties import Property
from nio.properties.version import VersionProperty
from .xbee_base import XBeeBase


@discoverable
class XBeeRemoteAT(XBeeBase):

    """Execute Remote AT commands.

    Parameters:
        command: The command to execute, ex. 'D0', WR'
        parameter: The command parameter, ex. '05' for 'D0' command
           to set pin high
        dest_addr: 2 byte address of remote xbee to send AT command too.
            Default value when left blank is "FF FF" which sends a broadcast.
    """

    version = VersionProperty(version='0.1.0')
    command = Property(title='AT Command (ascii)', default='ID')
    parameter = Property(title='Command Parameter (hex, ex: "05")', default='')
    dest_addr = Property(
        title='Destination Address (2 byte hex, ex: "00 05")', default='')

    def process_signals(self, signals):
        for signal in signals:
            try:
                command = self.command(signal)
                parameter = self.parameter(signal).replace(" ", "")
                dest_addr = self.dest_addr(signal).replace(" ", "")
                self._remote_at(command, parameter, dest_addr)
            except:
                self.logger.exception("Failed to execute remote at command")

    def _remote_at(self, command, parameter, dest_addr):
        command = command.encode('ascii')
        parameter = binascii.unhexlify(parameter)
        dest_addr = binascii.unhexlify(dest_addr) if dest_addr else b'\xFF\xFF'
        self.logger.debug(
            "Executing Remote AT command: {}, with parameter: {}".format(
                command, parameter))
        # remote_at: 0x17 "Remote AT Command"
        # frame_id: 0x01
        # dest_addr: 0xFFFF broadcasts to all XBees
        # data: RF data bytes to be transmitted
        # command: The command to execute, ex. 'D0', WR'
        # parameter: The command parameter, ex. b'\x05' for 'D0' command
        #    to set pin high
        #
        # frame_id is an arbitrary value, 1 hex byte, used to associate sent 
        # packets with their responses. If set to 0 no response will be sent.
        # Could be a block property.
        self._xbee.send(
            'remote_at', frame_id=b'\x01', dest_addr=dest_addr,
            command=command, parameter=parameter)
