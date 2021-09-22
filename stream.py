import logging
import os
import uuid
from json import dumps
from kafka import KafkaConsumer, KafkaProducer
from Resources.CicloVidaControl import  CicloVidaControl
from datetime import datetime

logging.getLogger().setLevel(logging.INFO)
identifier = uuid.uuid4().__str__()

try:


    logging.info('Starting detector...')

    data_cycle = CicloVidaControl()

    consumer = KafkaConsumer(os.environ['DATA_UPLOAD_EVENT'],
                             group_id=os.environ['GROUP_ID'],
                             bootstrap_servers=[os.environ['KAFKA_BOOTSTRAP_SERVER_ONE']],
                             auto_offset_reset='earliest',
                             enable_auto_commit='true',
                             session_timeout_ms=50000)
    producer = KafkaProducer(bootstrap_servers=[os.environ['KAFKA_BOOTSTRAP_SERVER_ONE']],
                             value_serializer=lambda x: dumps(x).encode(os.environ['ENCODE_FORMAT']))


    for message in consumer:
        fileName = message.value.decode(os.environ['ENCODE_FORMAT'])
        logging.info("New IMG arrived ID %s to consumer %s", fileName, identifier)
        try:
            startTime = datetime.now()
            results = data_cycle.process_img(fileName)
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
