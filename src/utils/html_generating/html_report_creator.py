import os

from src.utils.html_generating.primary_card_finder import get_most_frequent_card_number

small_font = '40px'
attention_color = '#c76e00'

def _create_html_table_header():
    return '''
    <table>
        <tr>
            <th>Amount</th>
            <th>Category</th>
            <th>Card</th>
            <th>Target & Date</th>
            <th>Left</th>
            
        </tr>
    '''

def _create_transaction_row(transaction, most_frequent_card):
    def safe_str(value):
        return value if value is not None else ""

    def color_currency(currency):
        return currency if currency == "BYN" else f"<span style='color: {attention_color};'>{currency}</span>"

    def color_card(card):
        return card if card == most_frequent_card else f"<span style='color: {attention_color};'>{card}</span>"

    category_display = (f"<span style='color: {attention_color}; font-size:{small_font};'>({transaction.transaction_type.get_label()})</span>"
                        if not transaction.is_payment()
                        else "" if transaction.is_payment_not_categorized()
                        else transaction.category)
    return f'''
        <tr>
            <td style="padding-left: 15px;">{transaction.get_rounded_amount()}<br>{color_currency(transaction.transaction_currency)}</td>
            <td>{category_display}</td>
            <td>
                {color_card(transaction.card)}
                <br>
                {color_currency(safe_str(transaction.card_currency))}
            </td>
            <td style="padding-left: 30px; font-size:{small_font}; max-width: 400px">
                {transaction.transaction_target}
                <br>
                <span style='color: #0047AB;'>{safe_str(transaction.transaction_date)}</span>
                <br>
                <span style='color: #0047AB;'>{safe_str(transaction.transaction_time)}</span>
            </td>
            <td>{safe_str(transaction.get_rounded_left_amount())}<br>{color_currency(safe_str(transaction.card_currency))}</td>
        </tr>
    '''

def _create_unparsed_transaction_row(transaction):
    return f'''
        <tr style="background-color: #ffcccc; font-style: italic;">
            <td colspan="6">{transaction.source_sms_message}</td>
        </tr>
    '''

def create_html_report(transactions):
    file_path = 'generated/priorbank-report.html'
    most_frequent_card = get_most_frequent_card_number(transactions)

    html_content = '''
    <html>
    <head>
        <style>
            body {
                font-family: Arial, sans-serif;
            }
            table {
                width: 100%;
                border-collapse: collapse;
                font-size: 60px;
            }
            th, td {
                padding: 90px 10px;
                text-align: left;
            }
            th:last-child, td:last-child {
                padding-right: 15px;
            }
            tr:nth-child(even) {
                background-color: #f2f2f2;
            }
            tr {
                height: 95px;
            }
        </style>
    </head>
    <body>
    ''' + _create_html_table_header()

    for transaction in transactions:
        if transaction.is_parsed_fine:
            html_content += _create_transaction_row(transaction, most_frequent_card)
        else:
            html_content += _create_unparsed_transaction_row(transaction)

    html_content += '''
        </table>
    </body>
    </html>
    '''

    os.makedirs('generated', exist_ok=True)
    with open(file_path, 'w') as file:
        file.write(html_content)