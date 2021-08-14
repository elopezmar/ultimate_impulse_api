from typing import Any, Generator, List

from google.cloud.firestore_v1.base_document import DocumentSnapshot
from google.cloud.firestore_v1.collection import CollectionReference

from firestore.client import client


class Collection():
    def __init__(self, path: str):
        self.__client = client
        self.__path = path

    @staticmethod
    def __to_list(data: Generator[DocumentSnapshot, Any, None]) -> List[dict]:
        return [{'id': item.id, **item.to_dict()} for item in data]

    def __get_ref(self) -> CollectionReference:
        return self.__client.collection(self.__path)

    def get(self, filters: list=None) -> List[dict]:
        ref = self.__get_ref()

        if filters:
            for filter in filters:
                ref = ref.where(*filter)

        return self.__to_list(ref.stream())

        

