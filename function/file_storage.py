from abc import ABC, abstractmethod
import os
import uuid
from datetime import datetime

from pynamodb.attributes import UnicodeAttribute, UTCDateTimeAttribute
from pynamodb.models import Model

from function.log_cfg import logger
from function.file_adaptor import FileAdaptor


class FileStorage():

    @abstractmethod
    def attach_file(self, file_handler: FileAdaptor):
        pass


# TODO - Could use factory is multiple storage types, but potentially pre-mature optimisation
class FileStorageDatabase(Model, FileStorage):
    class Meta:
        table_name = os.environ["DYNAMODB_TABLE"]
        if "ENV" in os.environ:
            host = "http://localhost:8000"
        else:
            region = os.environ["REGION"]
            host = os.environ["DYNAMODB_HOST"]

    id = UnicodeAttribute(hash_key=True)
    contents = UnicodeAttribute(null=True, default="")
    createdAt = UTCDateTimeAttribute(
        null=False, default=datetime.now().astimezone())
    updatedAt = UTCDateTimeAttribute(
        null=False, default=datetime.now().astimezone())

    def attach_file(self, file_handler: FileAdaptor):
        self.contents = file_handler.get_content()

    def save(self, conditional_operator=None, **expected_values):
        try:
            self.updatedAt = datetime.now().astimezone()
            if not self.id:
                self.id = uuid.uuid1().__str__()
            logger.debug("saving: {}".format(self))
            super(FileStorageDatabase, self).save()
        except Exception as e:
            logger.error("save {} failed: {}".format(
                self.id, e), exc_info=True)
            raise e
