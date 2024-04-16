from flask import Flask, render_template, url_for, request
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'testing'
app.config['MYSQL_PASSWORD'] = 'testpassword'
app.config['MYSQL_DB'] = 'electoralbonds'

mysql = MySQL(app)


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "GET":
        return render_template("index.html", searching=False, table=[])
    else:
        col_name = "Bond Number"
        col_value = request.form['bond-number']
        if col_value == "":
            return render_template("index.html", searching=False)

        cursor = mysql.connection.cursor()
        cursor.execute(
            f"SELECT * FROM bonds_encashed_by_parties WHERE `{col_name}` = {col_value}"
        )
        party_data = cursor.fetchall()
        print(party_data)
        cursor.execute(
            f"SELECT * FROM bonds_purchased WHERE `{col_name}` = {col_value}"
        )
        company_data = cursor.fetchall()

        if party_data == ():
            return render_template("index.html", searching=False, no_res=True)
        else:
            return render_template("index.html", searching=True, party_data=party_data, company_data=company_data)


@app.get("/search_comp")
def search_by_company_individual():
    return render_template("test.html")


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80, debug=True)
