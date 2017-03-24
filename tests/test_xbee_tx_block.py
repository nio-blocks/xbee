from unittest import skipUnless
from unittest.mock import patch
from nio.block.terminals import DEFAULT_TERMINAL
from nio.signal.base import Signal
from nio.testing.block_test_case import NIOBlockTestCase


xbee_available = True
try:
    import xbee
    from ..xbee_tx_block import XBeeTX
except:
    xbee_available = False


@skipUnless(xbee_available, 'xbee is not available!!')
class TestXBeeTX(NIOBlockTestCase):

    @patch('xbee.XBee')
    @patch('serial.Serial')
    def test_xbee_read(self, mock_serial, mock_xbee):
        blk = XBeeTX()
        self.configure_block(blk, {})
        blk.start()
        blk._callback({'sample': 'signal'})
        self.assertTrue(len(self.last_notified[DEFAULT_TERMINAL]))
        self.assertEqual(self.last_notified[DEFAULT_TERMINAL][0].sample, 'signal')
        blk.stop()

    @patch('xbee.XBee')
    @patch('serial.Serial')
    def test_bad_response(self, mock_serial, mock_xbee):
        blk = XBeeTX()
        self.configure_block(blk, {})
        blk.start()
        blk._callback('not a dict')
        self.assertFalse(len(self.last_notified[DEFAULT_TERMINAL]))
        blk.stop()

    @patch('xbee.XBee')
    @patch('serial.Serial')
    def test_xbee_send(self, mock_serial, mock_xbee):
        blk = XBeeTX()
        self.configure_block(blk, {})
        blk.start()
        blk.process_signals([Signal({'iama': 'signal'})])
        blk._xbee.send.assert_called_once_with(
            'tx',
            id=b'\x01',
            frame_id=b'\x01',
            dest_addr=b'\xFF\xFF',
            options=b'\x00',
            data=b"{'iama': 'signal'}")
        self.assertFalse(len(self.last_notified[DEFAULT_TERMINAL]))
        blk.stop()

    @patch('xbee.XBee')
    @patch('serial.Serial')
    def test_xbee_send_multiple_signals(self, mock_serial, mock_xbee):
        blk = XBeeTX()
        self.configure_block(blk, {})
        blk.start()
        blk.process_signals([Signal(), Signal()])
        self.assertEqual(2, blk._xbee.send.call_count)
        self.assertFalse(len(self.last_notified[DEFAULT_TERMINAL]))
        blk.stop()

    @patch('xbee.XBee')
    @patch('serial.Serial')
    def test_reconnect(self, mock_serial, mock_xbee):
        blk = XBeeTX()
        mock_xbee.side_effect = Exception
        self.configure_block(blk, {})
        # Wait for one reconnect
        from time import sleep
        sleep(1)
        # Each connect will fail twice, so with one reconnect, we have 4 calls.
        self.assertEqual(4, mock_xbee.call_count)


@skipUnless(xbee_available, 'xbee is not available!!')
class TestDigiMesh(TestXBeeTX):

    @patch('xbee.DigiMesh')
    @patch('serial.Serial')
    def test_xbee_send(self, mock_serial, mock_xbee):
        blk = XBeeTX()
        self.configure_block(blk, {'digimesh': True})
        blk.start()
        blk.process_signals([Signal({'iama': 'signal'})])
        blk._xbee.send.assert_called_once_with(
            'tx',
            id=b'\x10',
            frame_id=b'\x01',
            dest_addr=b'\x00\x00\x00\x00\x00\x00\xFF\xFF',
            reserved=b'\xFF\xFE',
            broadcast_radius=b'\x00',
            options=b'\x00',
            data=b"{'iama': 'signal'}")
        self.assertFalse(len(self.last_notified[DEFAULT_TERMINAL]))
        blk.stop()
