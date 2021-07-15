import cv2
import logging
import os
import uuid
import numpy as np
from json import dumps
from pydarknet import Detector, Image
from Resources.AwsS3Resource import AwsS3Resource
from kafka import KafkaConsumer, KafkaProducer
from datetime import datetime

logging.getLogger().setLevel(logging.INFO)
identifier = uuid.uuid4().__str__()

try:

    aws_resorce = AwsS3Resource()

    logging.info('Starting detector...')
    net = Detector(bytes("./cfg/yolov3.cfg", encoding="utf-8"), bytes("./weights/yolov3.weights", encoding="utf-8"), 0,
                   bytes("./data/coco.data", encoding="utf-8"))

    consumer = KafkaConsumer(os.environ['DATA_UPLOAD_EVENT'],
                             group_id=os.environ['GROUP_ID'],
                             bootstrap_servers=[os.environ['KAFKA_BOOTSTRAP_SERVER_ONE']],
                             auto_offset_reset='earliest',
                             enable_auto_commit='true',
                             session_timeout_ms=30000)
    producer = KafkaProducer(bootstrap_servers=[os.environ['KAFKA_BOOTSTRAP_SERVER_ONE']],
                             value_serializer=lambda x: dumps(x).encode(os.environ['ENCODE_FORMAT']))


    for message in consumer:
        fileName = message.value.decode(os.environ['ENCODE_FORMAT'])
        logging.info("New IMG arrived ID %s to consumer %s", fileName, identifier)
        try:
            startTime = datetime.now()
            img = aws_resorce.load_image(fileName)
            logging.info(len(img))
            nparray = np.asarray(bytearray(img), dtype="uint8")
            decoded_img = cv2.imdecode(nparray, cv2.IMREAD_COLOR)
            img_darknet = Image(decoded_img)
            results = net.detect(img_darknet)
            dataToSend = {'device_info': {'data_uuid': fileName, 'index_name': os.getenv('ELASTIC_INDEX_NAME'),
                                          'location-lat': 0.00000, 'location-lon': 0.00000},
                          'image_classification': results}
            finishTime = datetime.now()
            duration = finishTime - startTime
            logging.info("data send %s", dataToSend)
            logging.info("Processing Finished for %s with inference time of %s", fileName, duration.total_seconds())
            producer.send(os.getenv('PROCESS_RESULT_EVENT'), value=dataToSend)
        except Exception as e:
            logging.error(e)

except Exception as e:
    logging.error('There was an error while Connecting: %s', str(e))
