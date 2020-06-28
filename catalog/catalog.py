from sanic import Sanic
from sanic import response
import pymysql


app = Sanic(__name__)

db = pymysql.connect("db-catalog", "catalog-user", "catalogpwd", "CATALOG_DB")

cursor = db.cursor()
sql = """CREATE TABLE IF NOT EXISTS ITEM (ID int NOT NULL AUTO_INCREMENT, NAME CHAR(20) NOT NULL, PRICE FLOAT, SERIES int, PRIMARY KEY (ID))"""
cursor.execute(sql)


@app.route("/item", methods={"POST"})
async def add_item(request):
    name = request.json['name']
    price = float(request.json['price'])
    series = int(request.json['series'])
    cursor = db.cursor()
    sql = "INSERT INTO ITEM(NAME, PRICE, SERIES) \
       VALUES ('%s', '%d', %d )" % (name, price, series)
    try:
        cursor.execute(sql)
        db.commit()
        return response.json(status=200, body="OK")
    except Exception as e:
        print(e)
        db.rollback()
        return response.json(status=500, body="KO")


@app.route("/list")
async def get_items(request):
    items = []
    cursor = db.cursor()
    sql = "SELECT * FROM ITEM"
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            item = {
                "id": row[0],
                "name": row[1],
                "price": row[2],
                "series": row[3]
            }
            items.append(item)
        return response.json(status=200, body=items)
    except Exception as e:
        print(e)
        return response.json(status=500, body="KO")


if __name__ == "__main__":
    app.run(port=8000, host="0.0.0.0", workers=1, access_log=False)
