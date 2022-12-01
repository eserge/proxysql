FROM --platform=arm64 python:3.9.6

WORKDIR /app

COPY requirements.txt /
RUN pip install -r /requirements.txt

COPY src/ /app/

CMD [ "python", "ping.py" ]