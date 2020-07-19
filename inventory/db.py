

def init_db(db):
    cursor = db.cursor()
    sql = """CREATE TABLE IF NOT EXISTS STOCK (ITEM_ID int, STOCK int, PRIMARY KEY (ITEM_ID))"""
    cursor.execute(sql)


async def _get_all_stocks(db):
    items = []
    cursor = db.cursor()
    sql = "SELECT * FROM STOCK"
    cursor.execute(sql)
    results = cursor.fetchall()
    for row in results:
        item = {
            "item_id": row[0],
            "stock": row[1],
        }
        items.append(item)
    return items


async def _put_in_stocks(db, product_id, stock):
    cursor = db.cursor()
    sql = "INSERT INTO STOCK(ITEM_ID, STOCK) VALUES ('%d', %d )" % (product_id, stock)
    cursor.execute(sql)
    db.commit()