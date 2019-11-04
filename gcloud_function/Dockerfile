FROM python:3.7

RUN mkdir /usr/application
WORKDIR /usr/application

COPY ./src /usr/application/src
COPY ./run-local.py /usr/application/run-local.py

RUN pip install -r /usr/application/src/requirements.txt

ENV PYTHONPATH "${PYTHONPATH}:/usr/application/src"

CMD ["python", "/usr/application/run-local.py"]