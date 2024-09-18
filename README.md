# prior-bank-sms-parser
1) Parse PDF file with sms messages from bank.
2) Generate HTML report with categories of expenses.

<img src="https://raw.githubusercontent.com/eugene2owl/prior-bank-sms-parser/main/assets/images/readme/bank_sms_parser.png" alt="schema" width="1000"/>

## How to run
* Using Docker container [run-via-docker.sh](run-via-docker.sh)
* Right on a local machine [run-locally.sh](run-locally.sh)
```
(!) Python 3.10 and Poetry installation is pre-requisite to run locally.
```

## Environment variables
* `BANK_SMS_PDF_FILE_PATH` - path to PDF file with SMS messages from bank
