FROM python:3

RUN apt-get update && apt-get install libgl1 -y

WORKDIR /usr/src/app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

ADD templates /usr/src/app/templates
COPY config.py .
COPY main.py .
COPY MobileNetSSD_deploy.caffemodel .
COPY MobileNetSSD_deploy.prototxt .

CMD [ "python", "main.py" ]
