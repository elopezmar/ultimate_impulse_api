from copy import deepcopy


class Cache():
    def __init__(self):
        self.info: dict = {}

    def exists(self, key: str) -> bool:
        return self.get(key) != None

    def get(self, key: str) -> dict:
        return self.info.get(key)

    def set(self, key: str, data: dict) -> dict:
        self.info[key] = deepcopy(data)
        return self.info[key]

    def update(self, key: str, data: dict) -> dict:
        if not self.exists(key):
            self.set(key, data)
        self.info[key].update(deepcopy(data))
        return self.info[key]

    def delete(self, key: str) -> dict:
        return self.info.pop(key, None)

    def clear(self):
        self.info.clear()


cache = Cache()