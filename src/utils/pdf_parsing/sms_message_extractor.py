import re

def extract_sms_messages(full_text):
    pattern = r'Priorbank\.\s(.*?)Spravka:\s\d+'
    all_sms_messages = re.findall(pattern, full_text, re.DOTALL)
    needed_sms_messages = exclude_unneeded_sms_messages(all_sms_messages)
    return needed_sms_messages

def exclude_unneeded_sms_messages(sms_messages):
    return [message for message in sms_messages if not message.strip().startswith('3D-Secure kod')]