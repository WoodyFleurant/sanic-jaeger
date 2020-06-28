from sanic import Sanic
from sanic import response
import pymysql
import opentracing
from jaeger_util import init_tracer
from opentracing.ext import tags


app = Sanic(__name__)

db = pymysql.connect("db-inventory", "inventory-user", "inventorypwd", "INVENTORY_DB")

cursor = db.cursor()
sql = """CREATE TABLE IF NOT EXISTS STOCK (ITEM_ID int, STOCK int, PRIMARY KEY (ITEM_ID))"""
cursor.execute(sql)


@app.listener('after_server_start')
async def notify_server_started(app, loop):
    print("--- after server start ---")
    init_tracer("inventory")


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


@app.route("/reserve", methods={"POST"})
async def reserve(request):
    product_id = request.json['product_id']
    db.begin()
    cursor = db.cursor()
    sql = "SELECT * FROM STOCK WHERE ITEM_ID = ('%d')" % (int(product_id))
    sql_update = "UPDATE STOCK SET STOCK = STOCK - 1 WHERE ITEM_ID = ('%d')" % (int(product_id))
    try:
        cursor.execute(sql)
        result = cursor.fetchone()
        if len(result) == 0 or result is None:
            return response.json(status=404, body="Not Found")
        stock = int(result[1])
        if stock == 0:
            return response.json(status=410, body="Not available")
        cursor.execute(sql_update)
        db.commit()
        return response.json(status=200, body="OK")
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
