FROM python:3

RUN apt-get update && apt-get install libgl1 -y

WORKDIR /usr/src/app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

ADD lyquid /usr/src/app/lyquid
ADD templates /usr/src/app/templates
COPY main.py .
COPY config.py .
COPY SSD_MobileNet.caffemodel .
COPY SSD_MobileNet_prototxt.txt .

RUN ls
RUN ls src
CMD [ "python", "main.py" ]
