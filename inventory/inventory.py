from sanic import Sanic
from sanic import response
import pymysql
import opentracing
from opentracing.ext import tags
from jaeger_client import Config
from opentracing.scope_managers.contextvars import ContextVarsScopeManager
from opentracing.propagation import Format
from db import init_db, _get_all_stocks, _put_in_stocks

app = Sanic(__name__)

db = pymysql.connect("db-inventory", "inventory-user", "inventorypwd", "INVENTORY_DB")

init_db(db)


@app.listener('after_server_start')
async def notify_server_started(app, loop):
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


@app.route("/stocks", methods={"GET"})
async def get_stocks(request):
    tracer = opentracing.global_tracer()
    span_ctx = tracer.extract(format=Format.HTTP_HEADERS, carrier=request.headers)
    with tracer.start_span("get_stocks", child_of=span_ctx) as span:
        try:
            items = await _get_all_stocks(db)
            return response.json(status=200, body=items)
        except Exception as e:
            span.set_tag('response', e)
            span.set_tag(tags.ERROR, True)
            return response.json(status=500, body="KO")


@app.route("/fill", methods={"POST"})
async def put_in_stock(request):
    with opentracing.tracer.start_span('/fill') as span:
        product_id = int(request.json['product_id'])
        stock = int(request.json['stock'])
        try:
            await _put_in_stocks(db, product_id, stock)
            span.set_tag('response', "OK")
            return response.json(status=200, body="OK")
        except Exception as e:
            span.set_tag('response', e)
            span.set_tag(tags.ERROR, True)
            db.rollback()
            return response.json(status=500, body="KO")


if __name__ == "__main__":
    app.run(port=8001, host="0.0.0.0", workers=2, access_log=False)
