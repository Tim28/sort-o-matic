import os
from typing import List

from flask import Flask, render_template, request, redirect, abort, flash
from flask_bootstrap import Bootstrap5
from flask_migrate import Migrate

import models
from models import SortOMatic, db

DB_PATH = os.getenv('DATABASE_PATH', '/data/sort-o-matic.sqlite')

app = Flask(__name__)
app.secret_key = b'_5#y2a"F4Q8z\n\xec]/'
app.url_map.strict_slashes = False

bootstrap = Bootstrap5(app)
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_PATH}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

sortomatic = SortOMatic()


@app.route('/')
def index_route():
    return render_template('index.html', containers=sortomatic.get_containers())


@app.route('/items', methods=['GET', 'POST'])
def items_route():
    if request.method == 'POST':
        action = request.form['action']
        if action == "add_item":
            sortomatic.add_item(request.form['item_name'])

    return render_template('items.html', items=sortomatic.get_items())


@app.route('/containers', methods=['GET', 'POST'])
def containers_route():
    if request.method == 'POST':
        if request.form['action'] == 'add_container':
            container_name = request.form['container_name']
            sortomatic.add_container(container_name)

        elif request.form['action'] == 'remove_item':
            container_name = request.form['container_id']
            item_id = request.form['item_id']
            sortomatic.remove_item(container_name, item_id)
        return redirect('/')

    return render_template('containers.html', containers=sortomatic.get_containers())


@app.route('/container/<int:container_id>', methods=['GET', 'POST'])
def container_route(container_id):
    if request.method == "POST":
        if request.form.get('action') != 'add_item':
            return abort(502)

        container = sortomatic.get_container(container_id)
        if not container:
            return abort(404)

        item_id = request.form.get('item_id', type=int)
        item_description = request.form.get('item_description')
        item = sortomatic.get_item(item_id)

        if not item:
            item = sortomatic.add_item(item_description)

        container.add_item(item)

    return render_template('container.html', container=sortomatic.get_container(container_id))


@app.route('/container/<int:container_id>/delete/<int:containeritem_id>', methods=['GET'])
def container_delete_itemid_route(container_id, containeritem_id):
    container_item = models.ContainerItem.query \
        .filter_by(id=containeritem_id, container_id=container_id).first()

    db.session.delete(container_item)
    db.session.commit()

    return redirect(f'/container/{container_id}')


@app.route('/item/<int:item_id>')
def item_route(item_id):
    return render_template('item.html', item=sortomatic.get_item(item_id))


@app.route('/items/delete/<int:item_id>')
def item_delete_route(item_id):
    item = models.Item.query.filter_by(id=item_id).first()
    if item.containers:
        flash(f"Cannot delete Item '{item.description}' because it is still in {len(item.containers)} container(s)!")
        return redirect('/items')

    db.session.delete(item)
    db.session.commit()
    return redirect('/items')


@app.route('/scan')
def scan_route():
    return render_template('scan.html')


@app.route('/scan/<code>')
def scanned_item_route(code):
    found_containers = models.Container.query.filter_by(id=code).all()
    found_items = models.Item.query.filter_by(id=code).all()
    return render_template('scanned.html', containers=found_containers, items=found_items)


@app.route('/search')
def search_route():
    value = request.args.get('value')
    if not value:
        return redirect('/')

    found_containers = models.Container.query.filter(models.Container.description.contains(value)).all()
    found_items = models.Item.query.filter(models.Item.description.contains(value)).all()

    return render_template('search.html', results=found_containers + found_items)


@app.route('/api/lookahead/items')
def lookahead_items_route():
    items_: List[models.Item] = models.Item.query.all()
    return [{
        "title": item_.description,
        "id": item_.id,
    } for item_ in items_]


@app.route('/api/lookahead/containers')
def lookahead_containers_route():
    containers_: List[models.Container] = models.Container.query.all()
    return [{
        "title": container_.description,
        "id": container_.id,
    } for container_ in containers_]


if __name__ == '__main__':
    app.run(debug=True, port=8082)
