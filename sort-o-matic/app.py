import os

from flask import Flask, render_template, request, redirect
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate

import models
from models import SortOMatic, db

DB_PATH = os.getenv('DATABASE_PATH', '/data/sort-o-matic.sqlite')

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_PATH}"
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Might be interesting to use less memory

db.init_app(app)
migrate = Migrate(app, db)

sortomatic = SortOMatic()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if request.form['action'] == 'add_container':
            container_name = request.form['container_name']
            sortomatic.add_container(container_name)

        elif request.form['action'] == 'add_item':
            container_id = request.form['container_id']
            item_description = request.form['item_description']
            container = models.Container.query.filter_by(id=container_id).first_or_404()
            sortomatic.add_item(container, item_description)

        elif request.form['action'] == 'remove_item':
            container_name = request.form['container_id']
            item_id = request.form['item_id']
            sortomatic.remove_item(container_name, item_id)
        return redirect('/')

    return render_template('index.html', inventory=sortomatic.get_containers())


@app.route('/items', methods=['GET'])
def items():

    return render_template('m2m.html', items=sortomatic.get_items())


if __name__ == '__main__':
    app.run(debug=True, port=8080)
