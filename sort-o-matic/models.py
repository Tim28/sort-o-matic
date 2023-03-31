from typing import List, Optional

from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy.query import Query
from sqlalchemy.ext.associationproxy import association_proxy

db: SQLAlchemy = SQLAlchemy()


class ContainerItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    container_id = db.Column('container_id', db.Integer, db.ForeignKey('container.id'))
    item_id = db.Column('item_id', db.Integer, db.ForeignKey('item.id'))

    quantity = db.Column(db.Integer)

    # container = db.relationship('Container', back_populates='items_assoc')
    container = db.relationship('Container', back_populates='items')
    item = db.relationship('Item', back_populates='containers')


class Container(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String, nullable=True)
    identifier = db.Column(db.String, nullable=True)

    items = db.relationship('ContainerItem', back_populates='container')

    def __repr__(self):
        return f"Container ({self.id}): {self.description}"

    def __str__(self):
        return f"Container ({self.id}): {self.description}"


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String, nullable=True)
    identifier = db.Column(db.String, nullable=True)

    containers = db.relationship('ContainerItem', back_populates='item')

    def __repr__(self):
        return f"Item ({self.id}): {self.description}"

    def __str__(self):
        return f"Item ({self.id}): {self.description}"


class SortOMatic:
    def add_container(self, container_name):
        db.session.add(Container(description=container_name))
        db.session.commit()

    def add_item(self, container: Container, item_description: str):
        item = Item(description=item_description)
        item.containers.append(container)
        db.session.add(item)
        db.session.commit()

    def remove_item(self, container_name, item_id):
        item = Item.query.filter_by(id=item_id).first()
        db.session.delete(item)
        db.session.commit()

    def search(self, keyword):
        results = {}
        return results

    def get_containers(self):
        Container.query: Query

        return [
            container
            for container
            in Container.query.all()
        ]

    @staticmethod
    def get_container(container_id: int):
        return Container.query.filter_by(id=container_id).first()

    def get_items(self):
        Item.query: Query

        return [
            item
            for item
            in Item.query.all()
        ]
