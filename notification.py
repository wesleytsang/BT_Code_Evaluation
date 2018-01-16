class Notification:
    """Class of notification"""
    def __init__(self, received, sent, sent_from, action, subject=None):
        self.received = int(received)
        self.sent = int(sent)
        self.sent_from = sent_from
        self.action = action
        self.subject = subject

    def __str__(self):
        if self.subject is not None:
            return ' '.join([str(self.received), self.sent_from,
                             self.action, self.subject])
        else:
            return ' '.join([str(self.received), self.sent_from, self.action])