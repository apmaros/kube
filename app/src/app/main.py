from flask import Flask, render_template
import os
import time;

app = Flask(__name__)


@app.route('/')
def home():
    return {"message": f"Hello World, it is {time.asctime(time.localtime(time.time()))}"}


if __name__ == "__main__":
    print('Starting App')
    port = int(os.environ.get('PORT', 5050))
    app.run(debug=True, host='0.0.0.0', port=port)

