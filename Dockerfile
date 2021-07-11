FROM ubuntu:bionic

RUN apt update &&\
    apt install -y software-properties-common &&\
    apt-get -y install libgl1-mesa-dev &&\
    add-apt-repository ppa:deadsnakes/ppa &&\
    apt -y install python3.8 &&\
    apt-get install -y wget

RUN apt-get -y install python3-pip &&\
    python3.8 -m pip install pip &&\
    python3.8 -m pip install --upgrade pip

COPY requirements.txt /Yolo/

RUN python3.8 -m pip install numpy==1.20.3
RUN python3.8 -m pip install -r /Yolo/requirements.txt

RUN wget https://raw.githubusercontent.com/pjreddie/darknet/master/cfg/yolov3.cfg -P /Yolo/cfg &&\
    wget https://raw.githubusercontent.com/pjreddie/darknet/master/cfg/coco.data -P /Yolo/data &&\
    wget https://raw.githubusercontent.com/pjreddie/darknet/master/data/coco.names -P /Yolo/data &&\
    wget https://pjreddie.com/media/files/yolov3.weights -P /Yolo/weights

COPY ./ /Yolo/

WORKDIR /Yolo/

CMD ["python3.8","stream.py"]
