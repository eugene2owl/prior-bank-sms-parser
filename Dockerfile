FROM python:3.10-slim
RUN pip install poetry
WORKDIR /app
ENV PYTHONPATH /app
COPY pyproject.toml poetry.lock* /app/
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi
COPY . /app
ENV BANK_SMS_PDF_FILE_PATH=./Priorbank.pdf
CMD ["python", "src/main.py", "${BANK_SMS_PDF_FILE_PATH}"]
