import re

from src.models.TransactionType import TransactionType
from src.utils.pdf_parsing.category_finder import find_transaction_category
from src.utils.pdf_parsing.numeric_rounder import round_to_half


class Transaction:
    def __init__(self, card=None, card_currency=None, transaction_date=None, transaction_time=None,
                 amount=None, transaction_currency=None, transaction_type=None, transaction_target=None,
                 left_amount=None, source_sms_message=None, is_parsed_fine=True, category=None):
        self.card = card
        self.card_currency = card_currency
        self.transaction_date = transaction_date
        self.transaction_time = transaction_time
        self.amount = amount
        self.transaction_currency = transaction_currency
        self.transaction_type = transaction_type
        self.transaction_target = transaction_target
        self.left_amount = left_amount
        self.source_sms_message = source_sms_message
        self.is_parsed_fine = is_parsed_fine
        self.category = category

    @staticmethod
    def from_sms_message(message):
        patterns = {
            TransactionType.PAYMENT: r"Karta\s+(\S+)\s+(\d{2}-\d{2}-\d{2})\s+(\d{2}:\d{2}):\d{2}\.\s+Oplata\s+(\d+\.\d{2})\s+(\w+)\.\s+(.+)\s+Dostupno:\s+(\d+\.\d{2})\s+(\w+)\.",
            TransactionType.SENT_FROM_ME: r"Karta\s+(\S+)\s+(\d{2}-\d{2}-\d{2})\s+(\d{2}:\d{2}):\d{2}\.\s+Perevod\s+(\d+\.\d{2})\s+(\w+)\.\s+(.+)\s+Dostupno:\s+(\d+\.\d{2})\s+(\w+)\.",
            TransactionType.SENT_TO_ME: r"Karta\s+(\S+)\s+(\d{2}-\d{2}-\d{2})\s+(\d{2}:\d{2}):\d{2}\.\s+Zachislenie\s+perevoda\s+(\d+\.\d{2})\s+(\w+)\.\s+(.+)\s+Dostupno:\s+(\d+\.\d{2})\s+(\w+)\.",
            TransactionType.SENT_FROM_ME_WITH_NO_LEFT_AMOUNT: r"Karta\s+(\S+)\s+(\d{2}-\d{2}-\d{2})\s+(\d{2}:\d{2}):\d{2}\.\s+Perevod\s+(\d+\.\d{2})\s+(\w+)\.\s+(.+)$",
            TransactionType.PAYMENT_WITH_NO_LEFT_AMOUNT: r"Karta\s+(\S+)\s+(\d{2}-\d{2}-\d{2})\s+(\d{2}:\d{2}):\d{2}\.\s+Oplata\s+(\d+\.\d{2})\s+(\w+)\.\s+(.+)$",
            TransactionType.CASH_OUT_IN_ATM: r"Karta\s+(\S+)\s+(\d{2}-\d{2}-\d{2})\s+(\d{2}:\d{2}):\d{2}\.\s+Nalichnye\s+v\s+bankomate\s+(\d+\.\d{2})\s+(\w+)\.\s+(.+)\s+Dostupno:\s+(\d+\.\d{2})\s+(\w+)\.",
            TransactionType.RETURN_TO_ME: r"Na\s+kartu\s+(\S+)\s+proizveden\s+vozvrat\s+v\s+summe\s+(\d+\.\d{2})\s+(\w+)\s+po\s+operacii\s+v\s+(.+?)\.\s+Dostupno:\s+(\d+\.\d{2})\s+(\w+)\."
        }

        for transaction_type, pattern in patterns.items():
            match = re.search(pattern, message, re.DOTALL)
            if match:
                if transaction_type in (TransactionType.SENT_FROM_ME_WITH_NO_LEFT_AMOUNT, TransactionType.PAYMENT_WITH_NO_LEFT_AMOUNT):
                    card, transaction_date, transaction_time, amount, transaction_currency, transaction_target = match.groups()
                    left_amount, card_currency = None, None
                elif transaction_type == TransactionType.RETURN_TO_ME:
                    card, amount, transaction_currency, transaction_target, left_amount, card_currency = match.groups()
                    transaction_date, transaction_time = None, None
                else:
                    card, transaction_date, transaction_time, amount, transaction_currency, transaction_target, left_amount, card_currency = match.groups()

                transaction = Transaction(
                    card=card,
                    card_currency=card_currency,
                    transaction_date=transaction_date,
                    transaction_time=transaction_time,
                    amount=amount,
                    transaction_currency=transaction_currency,
                    transaction_type=transaction_type,
                    transaction_target=transaction_target,
                    left_amount=left_amount,
                    source_sms_message=message,
                    is_parsed_fine=True
                )
                transaction.category = find_transaction_category(transaction.transaction_target)
                return transaction

        return Transaction(source_sms_message=message, is_parsed_fine=False)

    def is_payment_not_categorized(self):
        return self.category is None and self.is_payment()

    def is_payment(self):
        return self.transaction_type in {TransactionType.PAYMENT, TransactionType.PAYMENT_WITH_NO_LEFT_AMOUNT}

    def get_rounded_amount(self):
        return round_to_half(self.amount)

    def get_rounded_left_amount(self):
        if self.left_amount is not None:
            return round_to_half(self.left_amount)
        return None