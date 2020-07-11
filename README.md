# Sanic with Tracing

### To build
```
docker-compose build
docker-compose up
```

### To test

Create new item
```
curl -XPOST \
    --header 'content-type: application/json' \
    --data '{"name": "product_1","price":"9.9"}' \
    http://localhost:8000/item
```

Create new stock for item 1
```
curl -XPOST \
    --header 'content-type: application/json' \
    --data '{"product_id": "1","stock":"10"}' \
    http://localhost:8001/fill
```   
   
List all items   
```    
curl http:/localhost:8000/list
```

List stocks
```
curl http:/localhost:8001/stocks
```

List items available
```
curl http:/localhost:8000/available
```