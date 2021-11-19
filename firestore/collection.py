from typing import Any, Generator, List

from google.cloud.firestore_v1.base_document import DocumentSnapshot
from google.cloud.firestore_v1.collection import CollectionReference
from google.cloud.firestore_v1.query import Query

from firestore.cache import cache
from firestore.client import client


class Collection():
    def __init__(self, path: str):
        self.path = path

    @property
    def ref(self) -> CollectionReference:
        return client.collection(self.path)

    def to_dict(self, item: DocumentSnapshot) -> dict:
        return cache.set(
            key=f'{self.path}/{item.id}',
            data={'id': item.id, **item.to_dict()}
        )

    def to_list(self, data: Generator[DocumentSnapshot, Any, None]) -> List[dict]:
        return [self.to_dict(item) for item in data]

    def get(self, filters: List[tuple]=None, order_by: List[tuple]=None, limit: int=None) -> List[dict]:
        '''
        filters => [(filter_field, comparison_operator, value), ...]
        order_by => [(order_field, direction: asc | desc )], if there is not direction provided sorting must be ascending
        '''

        ref = self.ref

        if filters:
            for item in filters:
                ref = ref.where(*item)

        if order_by:
            for item in order_by:
                direction = Query.ASCENDING

                if len(item) == 2 and item[1] == 'desc':
                    direction = Query.DESCENDING

                ref = ref.order_by(item[0], direction=direction)

        if limit:
            ref = ref.limit(limit)

        return self.to_list(ref.stream())
