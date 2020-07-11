from sanic import Sanic
from sanic import response
import pymysql
import opentracing
from opentracing.ext import tags
from jaeger_client import Config
from opentracing.scope_managers.contextvars import ContextVarsScopeManager

app = Sanic(__name__)

db = pymysql.connect("db-inventory", "inventory-user", "inventorypwd", "INVENTORY_DB")

cursor = db.cursor()
sql = """CREATE TABLE IF NOT EXISTS STOCK (ITEM_ID int, STOCK int, PRIMARY KEY (ITEM_ID))"""
cursor.execute(sql)


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


@app.route("/stocks", methods={"GET"})
async def get_stocks(request):
    items = []
    cursor = db.cursor()
    sql = "SELECT * FROM STOCK"
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            item = {
                "item_id": row[0],
                "stock": row[1],
            }
            items.append(item)
        return response.json(status=200, body=items)
    except Exception as e:
        print(e)
        return response.json(status=500, body="KO")

@app.route("/fill", methods={"POST"})
async def put_in_stock(request):
    with opentracing.tracer.start_span('/fill') as span:
        product_id = int(request.json['product_id'])
        stock = int(request.json['stock'])
        cursor = db.cursor()
        sql = "INSERT INTO STOCK(ITEM_ID, STOCK) VALUES ('%d', %d )" % (product_id, stock)
        try:
            cursor.execute(sql)
            db.commit()
            span.set_tag('response', "OK")
            return response.json(status=200, body="OK")
        except Exception as e:
            span.set_tag('response', e)
            span.set_tag(tags.ERROR, True)
            db.rollback()
            return response.json(status=500, body="KO")


if __name__ == "__main__":
    app.run(port=8001, host="0.0.0.0", workers=2, access_log=False)
