from sanic import Sanic
from sanic import response
import random

app = Sanic(__name__)

@app.route("/example-api")
async def example(request):
    random_value = random.randint(0, 100000)
    return response.json(random_value)

if __name__ == "__main__":
    app.run(port=8000, host="0.0.0.0", workers=2, access_log=False)