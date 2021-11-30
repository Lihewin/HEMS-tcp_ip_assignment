# save this as app.py
import re
import time
from flask import Flask, render_template, request

app = Flask(__name__)
app.config["ENV"] = "development"
app.config["DEBUG"] = True


@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    print(request)
    return "fdsa", 200


if __name__ == '__main__':
    app.run(port=80, debug=True)
