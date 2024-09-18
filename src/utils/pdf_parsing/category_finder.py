from src.utils.pdf_parsing.config_loader import load_yaml_config


def find_transaction_category(transaction_target):
    if transaction_target:
        target_key = transaction_target.strip().lower()
        for category, targets in _categories.items():
            if targets:
                for target in targets:
                    if target.lower() in target_key:
                        return category
    return None


def _load_payment_categories():
    config = load_yaml_config('config/categories.yaml')
    category_map = {}
    for category, targets in config.get('categories', {}).items():
        category_map[category] = targets
    return category_map


_categories = _load_payment_categories()
