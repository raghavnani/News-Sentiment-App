from app import db


class AbstractRepository():

    def delete(self, entity):
        db.session.delete(entity)
        db.session.commit()
        return entity

    def entity(self):
        raise NotImplementedError("Inherited repository should implement entity()")

    def find_all(self):
        result = db.session.query(self.entity()).order_by(self.entity().id.desc()).all()
        return result

    def find_by_id(self, id):
        result = db.session.query(self.entity()).filter_by(id=id).first()
        return result

    def get(self, id):
        return db.session.query(self.entity()).get(id)

    def save(self, entity):
        db.session.add(entity)
        db.session.commit()
        result = entity

        return result
