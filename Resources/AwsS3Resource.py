import os
import boto3
import logging
import io

class AwsS3Resource:

    def __init__(self):
        session = boto3.Session(region_name='us-east-1')
        self.bucket = session.resource('s3').Bucket(os.environ['BUCKET_NAME'])

    def load_image(self, file_name):
        try:
            logging.info('Trying to download %s', file_name)
            return self.bucket.Object(file_name).get()["Body"].read()
        except Exception as e:
            logging.error('Error: while downloading the file %s exception %s', file_name, str(e))
            raise
