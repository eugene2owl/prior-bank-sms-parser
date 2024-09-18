import os

from src.models.Transaction import Transaction
from src.utils.html_generating.html_report_creator import create_html_report
from src.utils.pdf_parsing.pdf_reader import extract_text_from_pdf
from src.utils.pdf_parsing.sms_message_extractor import extract_sms_messages

full_text = extract_text_from_pdf(os.getenv('BANK_SMS_PDF_FILE_PATH', './Priorbank.pdf'))
sms_messages = extract_sms_messages(full_text)
transactions = [Transaction.from_sms_message(message) for message in sms_messages]
create_html_report(transactions)