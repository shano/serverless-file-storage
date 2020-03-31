import os
import json
import boto3

from function.log_cfg import logger


class FileAdaptor():
    def __init__(self, bucket, key):
        self.bucket = bucket
        self.key = key
        s3 = boto3.resource("s3")
        self.obj = s3.Object(bucket, key)

    def get_unparsed_body(self):
        return self.obj.get()


class GenericFileAdaptor(FileAdaptor):

    # Where it's an unknown type, default to storing the url
    def get_content(self):
        return "https://%s.s3.amazonaws.com/%s" % (self.bucket, self.key)


class TextFileAdaptor(FileAdaptor):
    def get_content(self):
        return self.get_unparsed_body()["Body"].read().decode("utf-8")


class JsonFileAdaptor(FileAdaptor):
    def get_content(self):
        # TODO: An example to show the concept, but just storing as text, could do something clever
        return self.get_unparsed_body()["Body"].read().decode("utf-8")


class FileAdaptorFactory:
    def get_file_hander(self, bucket, key):
        self.bucket = bucket
        self.key = key
        filename, file_extension = os.path.splitext(key)
        logger.debug(file_extension)

        method = getattr(self, file_extension[1:], lambda: self.generic())
        return method()

    def generic(self):
        return GenericFileAdaptor(self.bucket, self.key)

    def txt(self):
        return TextFileAdaptor(self.bucket, self.key)

    def json(self):
        return JsonFileAdaptor(self.bucket, self.key)
