import json

from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy.query import Query

db = SQLAlchemy()


class Container(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String, nullable=True)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String, nullable=True)
    container_id = db.Column(db.Integer, db.ForeignKey('container.id'))


class SortOMatic:
    def add_container(self, container_name):
        db.session.add(Container(description=container_name))
        db.session.commit()

    def add_item(self, container_id, item_description):
        db.session.add(Item(description=item_description, container_id=container_id))
        db.session.commit()

    def remove_item(self, container_name, item_id):
        item = Item.query.filter_by(id=item_id).first()
        db.session.delete(item)
        db.session.commit()

    def search(self, keyword):
        results = {}
        return results

    def get_inventory(self):
        Container.query: Query
        Item.query: Query

        return {
            container: Item.query.filter_by(container_id=container.id)
            for container
            in Container.query.all()
        }
