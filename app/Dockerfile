FROM python:3.12-slim

RUN apt-get update

RUN pip install poetry==1.8.0

WORKDIR /app/

COPY . /app/

ENV PYTHONPATH "${PYTHONPATH}:/app/"

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes
RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]