from typing import List

from flask_sqlalchemy import SQLAlchemy

db: SQLAlchemy = SQLAlchemy()


class ContainerItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    container_id = db.Column('container_id', db.Integer, db.ForeignKey('container.id'))
    item_id = db.Column('item_id', db.Integer, db.ForeignKey('item.id'))

    quantity = db.Column(db.Integer)

    container = db.relationship('Container', back_populates='items')
    # container: Mapped['Container'] = db.relationship('Container', back_populates='items')
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

    def get_url(self):
        return f"/container/{self.id}"


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String, nullable=True)
    identifier = db.Column(db.String, nullable=True)

    containers = db.relationship('ContainerItem', back_populates='item')

    def __repr__(self):
        return f"Item ({self.id}): {self.description}"

    def __str__(self):
        return f"Item ({self.id}): {self.description}"

    def get_url(self):
        return f"/item/{self.id}"


class SortOMatic:
    def add_container(self, container_name):
        db.session.add(Container(description=container_name))
        db.session.commit()

    def remove_item(self, container_name, item_id):
        item = Item.query.filter_by(id=item_id).first()
        db.session.delete(item)
        db.session.commit()

    @staticmethod
    def get_containers() -> List[Container]:
        return Container.query.all()

    @staticmethod
    def get_container(container_id: int) -> Container:
        return Container.query.filter_by(id=container_id).first()

    @staticmethod
    def get_items() -> List[Item]:
        return Item.query.all()

    @staticmethod
    def get_item(item_id: int) -> Item:
        return Item.query.filter_by(id=item_id).first()

    @staticmethod
    def add_item(description):
        db.session.add(Item(description=description))
        db.session.commit()
