from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy.query import Query
import sqlalchemy as sa

db: SQLAlchemy = SQLAlchemy()


class Container(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String, nullable=True)

    items = db.relationship('Item', secondary='container_item', back_populates='containers')

    def __repr__(self):
        return f"Container ({self.id}): {self.description}"


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String, nullable=True)

    containers = db.relationship('Container', secondary='container_item', back_populates='items')

    def __repr__(self):
        return f"Item ({self.id}): {self.description}"


container_item_m2m = db.Table(
    "container_item",
    db.Column("container_id", sa.ForeignKey(Container.id), primary_key=True),
    db.Column("item_id", sa.ForeignKey(Item.id), primary_key=True)
)


# class OneClass(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String, nullable=True)
#
#     twos = db.relationship('TwoClass', secondary='one_two', back_populates='ones')
#
#
# class TwoClass(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String, nullable=True)
#
#     ones = db.relationship('OneClass', secondary='one_two', back_populates='twos')
#
#
# one_two_m2m = db.Table(
#     "one_two",
#     db.Column("one_id", sa.ForeignKey(OneClass.id), primary_key=True),
#     db.Column("two_id", sa.ForeignKey(TwoClass.id), primary_key=True)
# )


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

        return {
            container
            for container
            in Container.query.all()
        }

    def get_items(self):
        Item.query: Query

        return [
            item
            for item
            in Item.query.all()
        ]
