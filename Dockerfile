FROM ubuntu:bionic

RUN apt update &&\
    apt install -y software-properties-common &&\
    add-apt-repository ppa:deadsnakes/ppa &&\
    apt -y install python3.8

RUN apt-get -y install python3-pip &&\
    python3.8 -m pip install pip

COPY requirements.txt /Yolo/

RUN python3.8 -m pip install -r /Yolo/requirements.txt

COPY ./ /Yolo/

WORKDIR /Yolo/

CMD ["python3.8","stream.py"]
