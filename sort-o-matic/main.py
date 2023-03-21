import os

from flask import Flask, render_template, request, redirect
from flask_bootstrap import Bootstrap

from models import SortOMatic

app = Flask(__name__)
bootstrap = Bootstrap(app)

DATABASE_LOCATION = os.getenv('DATABASE_LOCATION', './database.json')

sortomatic = SortOMatic()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if request.form['action'] == 'add_container':
            container_id = request.form['container_id']
            sortomatic.add_container(container_id)
        elif request.form['action'] == 'add_item':
            container_id = request.form['container_id']
            item_description = request.form['item_description']
            sortomatic.add_item(container_id, {'description': item_description})
        elif request.form['action'] == 'remove_item':
            container_id = request.form['container_id']
            item_index = int(request.form['item_index'])
            sortomatic.remove_item(container_id, sortomatic.inventory[container_id][item_index])

    return render_template('index.html', inventory=sortomatic.inventory)


@app.route('/save')
def save():
    sortomatic.save_inventory(DATABASE_LOCATION)
    return redirect('/')


@app.route('/load')
def load():
    sortomatic.load_inventory(DATABASE_LOCATION)
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
