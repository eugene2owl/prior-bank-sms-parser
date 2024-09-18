#!/bin/bash

export BANK_SMS_PDF_FILE_PATH=./Priorbank.pdf
export PYTHONPATH=$PWD:$PYTHONPATH
poetry run python src/main.py
