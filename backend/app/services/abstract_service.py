
from flask import jsonify


class AbstractService():

    def delete(self, entity):
        self.repository().delete(entity)

    def find_all(self):
        return self.repository().find_all()

    def find_by_id(self, id):
        return self.repository().find_by_id(id)

    def get(self, id):
        return self.repository().get(id)

    def repository(self):
        raise NotImplementedError("Inherited Service should implement repository()")

    def save(self, entity):
        return self.repository().save(entity)

    def create_json(self, entities, show=[]):
        arr = []
        for entity in entities:
            arr.append(entity.to_dict(show=show))
        return jsonify(arr)
