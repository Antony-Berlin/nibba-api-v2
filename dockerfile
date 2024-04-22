FROM python:3.10

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

COPY ./functions.py /code/functions.py

COPY ./main.py /code/main.py

COPY ./vector_DB /code/vector_DB

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

CMD [ "uvicorn", "main:api", "--host", "0.0.0.0", "--port", "80" ]
