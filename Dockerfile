FROM python:3.6

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY . /usr/src/app
RUN pip install -r package.txt


ENTRYPOINT ["python3", "/usr/src/app/stellar_main.py"]
