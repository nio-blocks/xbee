from time import sleep
from collections import defaultdict
from unittest import skipUnless
from unittest.mock import MagicMock, patch
from nio.util.support.block_test_case import NIOBlockTestCase
from nio.common.signal.base import Signal

xbee_available = True
try:
    import xbee
    from ..xbee_at_command_block import XBeeATCommand
except:
    xbee_available = False


@skipUnless(xbee_available, 'xbee is not available!!')
class TestXBeeATCommand(NIOBlockTestCase):

    def setUp(self):
        super().setUp()
        self.signals = defaultdict(list)

    def signals_notified(self, signals, output_id):
        self.signals[output_id].extend(signals)

    @patch('xbee.XBee')
    @patch('serial.Serial')
    def test_defaults(self, mock_serial, mock_xbee):
        blk = XBeeATCommand()
        self.configure_block(blk, {})
        blk.start()
        blk.process_signals([Signal({'iama': 'signal'})])
        blk._xbee.send.assert_called_once_with(
            'at',
            frame_id=b'\x08',
            command=b'ID',
            parameter=b'')
        self.assertFalse(len(self.signals['default']))
        blk.stop()

    @patch('xbee.XBee')
    @patch('serial.Serial')
    def test_expression_props(self, mock_serial, mock_xbee):
        blk = XBeeATCommand()
        self.configure_block(blk, {
            "command": "D0",
            "parameter": "05"
        })
        blk.start()
        blk.process_signals([Signal({'iama': 'signal'})])
        blk._xbee.send.assert_called_once_with(
            'at',
            frame_id=b'\x08',
            command=b'D0',
            parameter=b'\x05')
        self.assertFalse(len(self.signals['default']))
        blk.stop()

    @patch('xbee.XBee')
    @patch('serial.Serial')
    def test_invalid_command(self, mock_serial, mock_xbee):
        blk = XBeeATCommand()
        self.configure_block(blk, {
            "command": "{{ 1 }}"
        })
        blk._logger = MagicMock()
        blk.start()
        blk.process_signals([Signal({'iama': 'signal'})])
        # send is never called because of the command not being ascii encodable
        # It needs to be a two ascii characters
        self.assertFalse(blk._xbee.send.called)
        # expected behavior is to log an error
        blk._logger.exception.assert_called_once_with('Failed to execute at command')
        blk.stop()
