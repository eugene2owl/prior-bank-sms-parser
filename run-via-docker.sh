docker build -t prior-bank-sms-parser-image .

docker run \
  -it \
  --rm \
  --name prior-bank-sms-parser-container \
  -e BANK_SMS_PDF_FILE_PATH=./Priorbank.pdf \
  -v ./generated-from-docker:/app/generated \
  prior-bank-sms-parser-image
