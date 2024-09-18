from collections import Counter


def get_most_frequent_card_number(transactions):
    card_numbers = [transaction.card for transaction in transactions if transaction.card is not None]

    if not card_numbers:
        return None

    card_number_counts = Counter(card_numbers)
    most_common_card, _ = card_number_counts.most_common(1)[0]

    return most_common_card
