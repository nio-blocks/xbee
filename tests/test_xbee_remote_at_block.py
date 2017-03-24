from unittest import skipUnless
from unittest.mock import MagicMock, patch
from nio.block.terminals import DEFAULT_TERMINAL
from nio.signal.base import Signal
from nio.testing.block_test_case import NIOBlockTestCase


xbee_available = True
try:
    import xbee
    from ..xbee_remote_at_block import XBeeRemoteAT
except:
    xbee_available = False


@skipUnless(xbee_available, 'xbee is not available!!')
class TestXBeeRemoteAT(NIOBlockTestCase):

    @patch('xbee.XBee')
    @patch('serial.Serial')
    def test_defaults(self, mock_serial, mock_xbee):
        blk = XBeeRemoteAT()
        self.configure_block(blk, {})
        blk.start()
        blk.process_signals([Signal({'iama': 'signal'})])
        blk._xbee.send.assert_called_once_with(
            'remote_at',
            id=b'\x17',
            frame_id=b'\x01',
            dest_addr_long=b'\x00\x00\x00\x00\x00\x00\x00\x00',
            dest_addr=b'\xFF\xFF',
            options=b'\x02',
            command=b'ID',
            parameter=b'')
        self.assertFalse(len(self.last_notified[DEFAULT_TERMINAL]))
        blk.stop()

    @patch('xbee.XBee')
    @patch('serial.Serial')
    def test_expression_props(self, mock_serial, mock_xbee):
        blk = XBeeRemoteAT()
        self.configure_block(blk, {
            "dest_addr": "00 42",
            "command": "D0",
            "parameter": "05"
        })
        blk.start()
        blk.process_signals([Signal({'iama': 'signal'})])
        blk._xbee.send.assert_called_once_with(
            'remote_at',
            id=b'\x17',
            frame_id=b'\x01',
            dest_addr_long=b'\x00\x00\x00\x00\x00\x00\x00\x00',
            dest_addr=b'\x00\x42',
            options=b'\x02',
            command=b'D0',
            parameter=b'\x05')
        self.assertFalse(len(self.last_notified[DEFAULT_TERMINAL]))
        blk.stop()

    @patch('xbee.XBee')
    @patch('serial.Serial')
    def test_invalid_dest_addr(self, mock_serial, mock_xbee):
        blk = XBeeRemoteAT()
        self.configure_block(blk, {
            "dest_addr": "0"
        })
        blk.logger = MagicMock()
        blk.start()
        blk.process_signals([Signal({'iama': 'signal'})])
        # send is never called because of the odd length dest_addr
        # It needs to be a byte, represented as two ascii chars
        self.assertFalse(blk._xbee.send.called)
        # expected behavior is to log error
        blk.logger.exception.assert_called_once_with('Failed to execute remote at command')
        blk.stop()

    @patch('xbee.XBee')
    @patch('serial.Serial')
    def test_invalid_command(self, mock_serial, mock_xbee):
        blk = XBeeRemoteAT()
        self.configure_block(blk, {
            "command": "{{ 1 }}"
        })
        blk.logger = MagicMock()
        blk.start()
        blk.process_signals([Signal({'iama': 'signal'})])
        # send is never called because of the command not being ascii encodable
        # It needs to be a two ascii characters
        self.assertFalse(blk._xbee.send.called)
        # expected behavior is to log error
        blk.logger.exception.assert_called_once_with('Failed to execute remote at command')
        blk.stop()


@skipUnless(xbee_available, 'xbee is not available!!')
class TestDigiMesh(TestXBeeRemoteAT):

    @patch('xbee.DigiMesh')
    @patch('serial.Serial')
    def test_defaults(self, mock_serial, mock_xbee):
        blk = XBeeRemoteAT()
        self.configure_block(blk, {"digimesh": True})
        blk.start()
        blk.process_signals([Signal({'iama': 'signal'})])
        blk._xbee.send.assert_called_once_with(
            'remote_at',
            id=b'\x17',
            frame_id=b'\x01',
            dest_addr_long=b'\x00\x00\x00\x00\x00\x00\xFF\xFF',
            reserved=b'\xFF\xFE',
            options=b'\x02',
            command=b'ID',
            parameter=b'')
        self.assertFalse(len(self.last_notified[DEFAULT_TERMINAL]))
        blk.stop()

    @patch('xbee.DigiMesh')
    @patch('serial.Serial')
    def test_expression_props(self, mock_serial, mock_xbee):
        blk = XBeeRemoteAT()
        self.configure_block(blk, {
            "digimesh": True,
            "dest_addr": "00 00 00 00 00 00 00 42",
            "command": "D0",
            "parameter": "05"
        })
        blk.start()
        blk.process_signals([Signal({'iama': 'signal'})])
        blk._xbee.send.assert_called_once_with(
            'remote_at',
            id=b'\x17',
            frame_id=b'\x01',
            dest_addr_long=b'\x00\x00\x00\x00\x00\x00\x00\x42',
            reserved=b'\xFF\xFE',
            options=b'\x02',
            command=b'D0',
            parameter=b'\x05')
        self.assertFalse(len(self.last_notified[DEFAULT_TERMINAL]))
        blk.stop()