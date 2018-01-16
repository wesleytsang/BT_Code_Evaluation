import unittest
from notification import Notification


class TestNotification(unittest.TestCase):

    def setUp(self):
        self.noti_1 = Notification('1508405807242', '1508405807141', 'vader', 'HELLO')
        self.noti_2 = Notification('1508405807378', '1508405807387', 'luke', 'LOST', 'vader')
    

    def test_received(self):
        self.assertEqual(self.noti_1.received, 1508405807242)
        self.assertEqual(self.noti_2.received, 1508405807378)


    def test_sent(self):
        self.assertEqual(self.noti_1.sent, 1508405807141)
        self.assertEqual(self.noti_2.sent, 1508405807387)


    def test_sent_from(self):
        self.assertEqual(self.noti_1.sent_from, 'vader')
        self.assertEqual(self.noti_2.sent_from, 'luke')


    def test_action(self):
        self.assertEqual(self.noti_1.action, 'HELLO')
        self.assertEqual(self.noti_2.action, 'LOST')


    def test_subject(self):
        self.assertEqual(self.noti_1.subject, None)
        self.assertEqual(self.noti_2.subject, 'vader')


    def test_str(self):
        self.assertEqual(str(self.noti_1), '1508405807242 vader HELLO')
        self.assertEqual(str(self.noti_2), '1508405807378 luke LOST vader')


if __name__ == '__main__':
    unittest.main()
