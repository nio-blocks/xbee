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
class TestMongoDB(NIOBlockTestCase):

    def setUp(self):
        super().setUp()
        self.signals = defaultdict(list)

    def signals_notified(self, signals, output_id):
        self.signals[output_id].extend(signals)

    @patch('xbee.XBee')
    @patch('serial.Serial')
    def test_read_xbee(self, mock_ser, mock_xbee):
        blk = XBee()
        self.configure_block(blk, {})
        # Simulate some response from the xbee read
        blk._xbee.wait_read_frame.return_value = {'sample': 'signal'}
        blk.start()
        # Wait a little bit for a read
        sleep(0.1)
        self.assertTrue(len(self.signals['default']))
        self.assertEqual(self.signals['default'][0].sample, 'signal')
        blk.stop()
