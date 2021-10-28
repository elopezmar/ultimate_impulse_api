from algoliasearch.search_client import SearchClient
from algoliasearch.search_index import SearchIndex


class Index():
    def __init__(self, id: str, url: str, title: str, type: str, **fields):
        self.id = id
        self.url = url
        self.title = title
        self.type = type
        self.fields = fields

    @property
    def index(self) -> SearchIndex:
        #TODO: Agregar a variables de entorno
        api_id = 'L1A2GEZGAC'
        api_key = '2d5dfabc559ee1e1b7850825b263883e'
        name = 'ui-index'
        return SearchClient.create(api_id, api_key).init_index(name)

    @property
    def data(self) -> dict:
        return {
            'objectID': self.id,
            'url': self.url,
            'title': self.title,
            'type': self.type,
            'fields': {k: v for k, v in self.fields.items() if v != None}
        }

    def save(self):
        self.index.save_object(self.data)

    def delete(self):
        self.index.delete_object(self.id)