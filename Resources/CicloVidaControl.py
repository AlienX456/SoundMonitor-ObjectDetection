import cv2
import logging
import numpy as np
from Resources.AwsS3Resource import AwsS3Resource
from pydarknet import Detector, Image

logging.getLogger().setLevel(logging.INFO)
class CicloVidaControl:

    def __init__(self):
        self.__aws_s3_resource = AwsS3Resource()
        self.__net = Detector(bytes("./cfg/yolov3-custom.cfg", encoding="utf-8"), bytes("./weights/yolov3.weights", encoding="utf-8"),
                       0,
                       bytes("./data/obj.data", encoding="utf-8"))

    def process_img(self, nombre_archivo):
        img = self.__aws_s3_resource.load_image(nombre_archivo)
        nparray = np.asarray(bytearray(img), dtype="uint8")
        decoded_img = cv2.imdecode(nparray, cv2.IMREAD_COLOR)
        img_darknet = Image(decoded_img)
        detections = self.__net.detect(img_darknet)
        return self.remove_box_on_detections(detections)

    @staticmethod
    def remove_box_on_detections(detections) -> dict:
        detections_filtered = []
        for detection in detections:
            detections_filtered.append({"class": detection[0], "score": detection[1]})
        return detections_filtered



