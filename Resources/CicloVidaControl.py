from Resources.AwsS3Resource import AwsS3Resource

class CicloVidaControl:

    def __init__(self):
        self.__aws_s3_resource = AwsS3Resource()

    def process_audio(self, nombre_archivo):
        self.__aws_s3_resource.download_object(nombre_archivo)


