FROM python:3.11.6-alpine3.17 as builder

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=./

ENV WORKDIR=/server
WORKDIR $WORKDIR
RUN pip install --upgrade pip
RUN pip install poetry==1.7.1

COPY pyproject.toml ./

RUN poetry config virtualenvs.create false \
    && poetry install

RUN poetry lock


COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]