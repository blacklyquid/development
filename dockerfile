FROM python:3

RUN apt-get update && apt-get install libgl1 -y

WORKDIR /usr/src/app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

ADD src /usr/src/app/src
ADD templates /usr/src/app/templates
COPY main.py .
COPY config.py .
COPY SSD_MobileNet.caffemodel .
COPY SSD_MobileNet_prototxt.txt .

CMD [ "python", "./main.py" ]
