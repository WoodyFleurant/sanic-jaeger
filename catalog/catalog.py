from sanic import Sanic
from sanic import response
import requests
import pymysql
import opentracing
from opentracing.ext import tags
from jaeger_client import Config
from opentracing.scope_managers.contextvars import ContextVarsScopeManager
from logic import _retain_only_items_in_stock
from db import _fetch_all_items, _create_new_item, _init_db

app = Sanic(__name__)

db = pymysql.connect("db-catalog", "catalog-user", "catalogpwd", "CATALOG_DB")

_init_db(db)

@app.listener('after_server_start')
async def notify_server_started(app, loop):
    print("--- after server start ---")
    config = Config(
        config={
            'sampler': {
                'type': 'const',
                'param': 1,
            },
            'logging': True,
        },
        service_name="inventory",
        validate=True,
        scope_manager=ContextVarsScopeManager()
    )
    config.initialize_tracer()


@app.route("/item", methods={"POST"})
async def add_item(request):
    name = request.json['name']
    price = float(request.json['price'])
    try:
        _create_new_item(db, name, price)
        return response.json(status=200, body="OK")
    except Exception as e:
        print(e)
        return response.json(status=500, body=e)


@app.route("/list")
async def get_items(request):
    try:
        items = _fetch_all_items(db)
        return response.json(status=200, body=items)
    except Exception as e:
        print(e)
        return response.json(status=500, body=e)


@app.route("/available")
async def get_available_items(request):
    try:
        items = _fetch_all_items(db)
        inventory = await _fetch_all_inventory()
        available_items = _retain_only_items_in_stock(items, inventory)
        return response.json(status=200, body=available_items)
    except Exception as e:
        print(e)
        return response.json(status=500, body=e)


async def _fetch_all_inventory():
    response = requests.get("http://inventory:8001/stocks")
    return response.json()


if __name__ == "__main__":
    app.run(port=8000, host="0.0.0.0", workers=2, access_log=False)
