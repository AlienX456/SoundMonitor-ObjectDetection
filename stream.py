import cv2
import logging
import os
import uuid
import numpy as np
from json import dumps
from pydarknet import Detector, Image
from Resources.AwsS3Resource import AwsS3Resource
from Resources.YOLOResources import YOLOResources
from kafka import KafkaConsumer, KafkaProducer

logging.getLogger().setLevel(logging.INFO)
inferencer_identifier = uuid.uuid4().__str__()



consumer = KafkaConsumer(os.environ['DATA_UPLOAD_EVENT'],
                         group_id=os.environ['GROUP_ID'],
                         bootstrap_servers=[os.environ['KAFKA_BOOTSTRAP_SERVER_ONE']],
                         auto_offset_reset='earliest',
                         enable_auto_commit='true',
                         client_id=inferencer_identifier)
producer = KafkaProducer(bootstrap_servers=[os.environ['KAFKA_BOOTSTRAP_SERVER_ONE']],
                         value_serializer=lambda x: dumps(x).encode(os.environ['ENCODE_FORMAT']))

logging.info('Started download of model configuration and weights')

result = YOLOResources.download_yolo_resources()

if (result):

    aws_resorce = AwsS3Resource()

    logging.info('Downloads of model configuration and weights completed!')

    logging.info('Starting detector...')
    net = Detector(bytes("cfg/yolov3.cfg", encoding="utf-8"), bytes("weights/yolov3.weights", encoding="utf-8"), 0,
                   bytes("data/coco.data", encoding="utf-8"))

    for message in consumer:
        fileName = message.value.decode(os.environ['ENCODE_FORMAT'])
        logging.info("New IMG arrived ID %s to consumer %s", fileName, inferencer_identifier)
        try:
            img = aws_resorce.load_image('fileName')
            logging.info(len(img))
            nparray = np.asarray(bytearray(img), dtype="uint8")
            decoded_img = cv2.imdecode(nparray, cv2.IMREAD_COLOR)
            img_darknet = Image(decoded_img)
            results = net.detect(img_darknet)
            dataToSend = {'device_info': {'data_uuid': fileName, 'index_name': os.getenv('ELASTIC_INDEX_NAME')}, 'image_classification': results}
            producer.send(topic=os.getenv['PROCESS_RESULT_EVENT'], value=dataToSend)
        except Exception as e:
            logging.error(e)

else:
    logging.info('There was a problem downloading model configuration and weights')

