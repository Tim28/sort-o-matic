import os
from typing import List

from flask import Flask, render_template, request, redirect, abort
from flask_bootstrap import Bootstrap5
from flask_migrate import Migrate

import models
from models import SortOMatic, db

DB_PATH = os.getenv('DATABASE_PATH', '/data/sort-o-matic.sqlite')

app = Flask(__name__)
app.url_map.strict_slashes = False

bootstrap = Bootstrap5(app)
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_PATH}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

sortomatic = SortOMatic()


@app.route('/', methods=['GET', 'POST'])
def index_route():
    if request.method == 'POST':
        if request.form['action'] == 'add_container':
            container_name = request.form['container_name']
            sortomatic.add_container(container_name)

        # elif request.form['action'] == 'add_item':
        #     container_id = request.form['container_id']
        #     item_description = request.form['item_description']
        #     container_obj = models.Container.query.filter_by(id=container_id).first_or_404()
        #     sortomatic.add_item(container_obj, item_description)

        elif request.form['action'] == 'remove_item':
            container_name = request.form['container_id']
            item_id = request.form['item_id']
            sortomatic.remove_item(container_name, item_id)
        return redirect('/')

    return render_template('containers.html', containers=sortomatic.get_containers())


@app.route('/items', methods=['GET', 'POST'])
def items_route():
    if request.method == 'POST':
        action = request.form['action']
        if action == "add_item":
            sortomatic.add_item(request.form['item_name'])

    return render_template('items.html', items=sortomatic.get_items())


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

        # return request.values
    return render_template('container.html', container=sortomatic.get_container(container_id))


@app.route('/item/<int:item_id>')
def item_route(item_id):
    return render_template('item.html', item=sortomatic.get_item(item_id))


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


@app.route('/api/lookahead')
def lookahead_route():
    items_: List[models.Item] = models.Item.query.all()
    return [{
        "title": item_.description,
        "id": item_.id,
    } for item_ in items_]


if __name__ == '__main__':
    app.run(debug=True, port=8080)
