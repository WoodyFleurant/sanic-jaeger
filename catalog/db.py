def _init_db(db):
    cursor = db.cursor()
    sql = """CREATE TABLE IF NOT EXISTS ITEM (ID int NOT NULL AUTO_INCREMENT, NAME CHAR(20) NOT NULL, PRICE FLOAT, PRIMARY KEY (ID))"""
    cursor.execute(sql)


def _fetch_all_items(db):
    items = []
    cursor = db.cursor()
    sql = "SELECT * FROM ITEM"
    cursor.execute(sql)
    results = cursor.fetchall()
    for row in results:
        item = {
            "id": row[0],
            "name": row[1],
            "price": row[2]
        }
        items.append(item)
    return items


def _create_new_item(db, name, price):
    cursor = db.cursor()
    sql = "INSERT INTO ITEM(NAME, PRICE) \
           VALUES ('%s', '%d')" % (name, price)
    try:
        cursor.execute(sql)
        db.commit()
    except Exception as e:
        print(e)
        db.rollback()
        raise Exception("failed to insert item in db")