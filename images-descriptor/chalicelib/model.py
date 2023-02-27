import os

from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, UTCDateTimeAttribute, ListAttribute, MapAttribute, NumberAttribute


class ConceptMap(MapAttribute):
    name = UnicodeAttribute(null=False)
    value = NumberAttribute(null=False)


class ImageModel(Model):
    class Meta:
        table_name = os.environ['TABLE_NAME']

    id = UnicodeAttribute(hash_key=True)
    created_at = UTCDateTimeAttribute(null=False)
    extension = UnicodeAttribute(null=False)
    concepts = ListAttribute(of=ConceptMap, null=True)

    def get_file_name(self):
        return f'{self.id}.{self.extension}'
