from enum import Enum

class TransactionType(Enum):
    PAYMENT = ('PAYMENT', 'payment')
    SENT_FROM_ME = ('SENT_FROM_ME', 'sent from me')
    SENT_TO_ME = ('SENT_TO_ME', 'sent to me')
    SENT_FROM_ME_WITH_NO_LEFT_AMOUNT = ('SENT_FROM_ME_WITH_NO_LEFT_AMOUNT', 'sent from me')
    PAYMENT_WITH_NO_LEFT_AMOUNT = ('PAYMENT_WITH_NO_LEFT_AMOUNT', 'payment')
    CASH_OUT_IN_ATM = ('CASH_OUT_IN_ATM', 'cash out in ATM')
    RETURN_TO_ME = ('RETURN_TO_ME', 'returned to me')

    def __init__(self, code, label):
        self.code = code
        self.label = label

    def get_label(self):
        return self.label