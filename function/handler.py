import http.client as httplib
import uuid
import os
from pynamodb.exceptions import DoesNotExist, DeleteError, UpdateError
from function.file_storage import FileStorageDatabase
from function.log_cfg import logger
from function.file_adaptor import (
    JsonFileAdaptor,
    TextFileAdaptor,
    FileAdaptor,
    FileAdaptorFactory,
)

BUCKET = os.environ["S3_BUCKET"]
KEY_BASE = os.environ["S3_KEY_BASE"]


def event(event, context):
    """
    Triggered by s3 events, object create and remove
    """
    logger.debug("event: {}".format(event))
    event_name = event["Records"][0]["eventName"]
    bucket = event["Records"][0]["s3"]["bucket"]["name"]
    key = event["Records"][0]["s3"]["object"]["key"]
    source_file_adaptor_factory = FileAdaptorFactory()

    if "ObjectCreated:Put" == event_name:
        try:
            file_adaptor = source_file_adaptor_factory.get_file_hander(
                bucket, key)
            file_storage = FileStorageDatabase()
            file_storage.attach_file(file_adaptor)
            file_storage.save()
            return {"statusCode": httplib.ACCEPTED}
        except UpdateError:
            return {
                "statusCode": httplib.BAD_REQUEST,
                "body": {"error_message": "Unable to update ASSET"},
            }
