# Development stage

WORK IN PROGRESS
This addon has not been completed, do not use.

# sort-o-matic

Sort-O-Matic - Home Assistant Add-on for sorting and finding items in physical containers

# Home Assistant Add-on: Sort-O-Matic

Sort-O-Matic is a powerful [HomeAssistant][homeassistant] addon designed to help you easily index and locate items that you have stored in physical containers around your house. With this addon, you can easily create a comprehensive catalog of all your belongings and their locations, making it easy to find what you need when you need it.

Sort-O-Matic works by allowing you to assign a unique identifier to each of your physical containers, such as boxes, bins, or shelves. You can then use the addon to create an inventory list of all the items you have stored in each container, including a detailed description of each item, its location, and any other relevant information.

The addon comes with an intuitive user interface that makes it easy to add new items to your inventory, update existing entries, or search for specific items using keywords or other criteria. You can also create custom categories and tags to help you organize your inventory and make it easier to find what you're looking for.

In addition to its powerful indexing and search capabilities, Sort-O-Matic also comes with a range of useful features to help you manage your inventory more efficiently. For example, you can set reminders to alert you when items are due for maintenance or replacement, or you can create reports to track usage patterns and identify items that may need to be replaced or restocked.

Overall, Sort-O-Matic is an invaluable tool for anyone who wants to keep track of their belongings and ensure that everything is organized and easy to find. Whether you're a busy professional, a homemaker, or simply someone who wants to stay on top of their household inventory, this addon is a must-have for any HomeAssistant user.

## Authors

The original setup of this repository is by [Mikki Weesenaar][mweesenaar] and [Tim Wijers][tim28].

## Database migrations
To create a new migration file, first add or update the models.  
Then run `flask db migrate -m 'My migration description'`  
Finally run `flask db upgrade`

## Local testing

```bash
docker build \
 --build-arg BUILD_FROM="homeassistant/aarch64-base:latest" \
 -t local/my-test-addon .
```

```bash
docker run --rm \
 -e DATABASE_PATH="sort-o-matic.sqlite3" \
 -v /tmp/my_test_data:/data \
 -p 8099:8099 \
 local/my-test-addon
```

## License

MIT License 2023

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

[homeassistant]: https://www.home-assistant.io/
[mweesenaar]: http://github.com/mweesenaar
[tim28]: http://github.com/tim28
