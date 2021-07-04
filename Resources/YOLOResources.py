import requests
import logging
import os

logging.getLogger().setLevel(logging.INFO)

class YOLOResources:

    @staticmethod
    def download_yolo_resources() -> bool:
        os.makedirs('cfg')
        yolo_config = requests.get('https://raw.githubusercontent.com/pjreddie/darknet/master/cfg/yolov3.cfg')
        with open('cfg/yolov3.cfg', 'wb') as f:
            f.write(yolo_config.content)
        os.makedirs('data')
        coco_data = requests.get('https://raw.githubusercontent.com/pjreddie/darknet/master/cfg/coco.data')
        with open('data/coco.data', 'wb') as f:
            f.write(coco_data.content)
        coco_names = requests.get('https://raw.githubusercontent.com/pjreddie/darknet/master/data/coco.names')
        with open('data/coco.names', 'wb') as f:
            f.write(coco_names.content)
        os.makedirs('weights')
        yolo_weights = requests.get('https://pjreddie.com/media/files/yolov3.weights')
        with open('weights/yolov3.weights', 'wb') as f:
            f.write(yolo_weights.content)

        result = coco_data.status_code == yolo_config.status_code == coco_names.status_code == yolo_weights.status_code == 200

        return result


