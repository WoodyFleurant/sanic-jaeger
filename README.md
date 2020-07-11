# sanic-jaeger
Sanic &amp; Open Tracing with Jaeger


ab -n 10000 -c 100 localhost:8000/example-api

docker build -t empty-sanic -f empty/Dockerfile empty/
docker run -p 8000:8000 empty-sanic


curl -XPOST \
    --header 'content-type: application/json' \
    --data '{"name": "product_1","price":"9.9"}' \
    http://localhost:8000/item
    
#ab -n 10000 -c 100 -T application/json -p post.json http://localhost:8000/item

#ab -n 10000 -c 100 -p catalog/post.json -T application/json http://localhost:8000/item

curl -XPOST \
    --header 'content-type: application/json' \
    --data '{"product_id": "1","stock":"10"}' \
    http://localhost:8001/fill
    
curl -XPOST --header 'content-type: application/json' --data '{"product_id": "2","stock":"10"}' http://localhost:8001/fill

curl http:/localhost:8000/list

curl http:/localhost:8001/stocks


#curl -XPOST --header 'content-type: application/json' --data '{"product_id": "2"}' http://localhost:8001/reserve