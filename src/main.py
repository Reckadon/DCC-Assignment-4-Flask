from flask import Flask, render_template
from flask_mysqldb import MySQL

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.get("/search_comp")
def search_by_company_individual():
    return render_template("test.html")


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80, debug=True)
