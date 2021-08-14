from algoliasearch.search_client import SearchClient

class Algolia():
    def __init__(self, collection_name: str):
        # self.client = SearchClient.create(
        #     'L1A2GEZGAC', # TODO: Agregar a variable de entorno
        #     '2d5dfabc559ee1e1b7850825b263883e'
        # )
        # self.index = self.client.init_index(collection_name)
        pass

    def manage_object_id(self, obj: dict):
        obj['objectID'] = obj.pop('id')
        return obj
        
    def save(self, obj: dict):
        # obj = self.manage_object_id(obj)
        # self.index.save_object(obj)
        pass

    def delete(self, object_id: str):
        # self.index.delete_object(object_id)
        pass