from time import sleep
from collections import defaultdict
from unittest import skipUnless
from unittest.mock import MagicMock, patch
from nio.util.support.block_test_case import NIOBlockTestCase


xbee_available = True
try:
    import xbee
    from ..xbee_block import XBee
except:
    xbee_available = False


@skipUnless(xbee_available, 'xbee is not available!!')
class TestXBee(NIOBlockTestCase):

    def setUp(self):
        super().setUp()
        self.signals = defaultdict(list)

    def signals_notified(self, signals, output_id):
        self.signals[output_id].extend(signals)

    @patch('xbee.XBee')
    @patch('serial.Serial')
    def test_xbee_read(self, mock_serial, mock_xbee):
        blk = XBee()
        self.configure_block(blk, {})
        blk.start()
        blk._callback({'sample': 'signal'})
        self.assertTrue(len(self.signals['default']))
        self.assertEqual(self.signals['default'][0].sample, 'signal')
        blk.stop()

    @patch('xbee.XBee')
    @patch('serial.Serial')
    def test_bad_response(self, mock_serial, mock_xbee):
        blk = XBee()
        self.configure_block(blk, {})
        blk.start()
        blk._callback('not a dict')
        self.assertFalse(len(self.signals['default']))
        blk.stop()
