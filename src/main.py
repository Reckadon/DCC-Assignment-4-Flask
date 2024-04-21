from flask import Flask, render_template, request
from flask_mysqldb import MySQL
import locale

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'testing'
app.config['MYSQL_PASSWORD'] = 'testpassword'
app.config['MYSQL_DB'] = 'electoralbonds'

mysql = MySQL(app)


def number_format(n):
    s, *d = str(n).partition(".")
    r = ",".join([s[x - 2:x] for x in range(-3, -len(s), -2)][::-1] + [s[-3:]])
    return "".join([r] + d)


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

        cursor.execute(
            f"SELECT * FROM bonds_purchased WHERE `{col_name}` = {col_value}"
        )
        company_data = cursor.fetchall()

        if party_data == ():
            return render_template("index.html", searching=False, no_res=True)
        else:
            return render_template("index.html", searching=True, party_data=party_data, company_data=company_data)


@app.route("/search_comp", methods=["GET", "POST"])
def search_by_company_individual():
    cursor = mysql.connection.cursor()
    cursor.execute(
        f"SELECT DISTINCT `Name of the Purchaser` FROM bonds_purchased"
    )
    company_names = cursor.fetchall()
    if request.method == "GET":
        return render_template("company.html", searching=False, names=company_names)
    elif request.method == "POST":
        company_name = request.form['company-name']
        # for year wise data
        query = f"SELECT `Date of Purchase`, `Denominations` FROM bonds_purchased WHERE `Name of the Purchaser` = '{company_name}'"
        cursor.execute(query)
        raw_data = cursor.fetchall()
        bonds_number_denom_data = {}
        bonds_total_denom_data = {}
        for row in raw_data:
            date = row[0]
            year = date.split('/')[-1]
            locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
            denom = locale.atoi(row[1])
            bonds_number_denom_data[year] = bonds_number_denom_data.get(year, 0) + 1
            bonds_total_denom_data[year] = bonds_total_denom_data.get(year, 0) + denom

        per_year_data = [[year, bonds_number_denom_data[year], bonds_total_denom_data[year]] for year in
                         list(bonds_total_denom_data.keys())]
        total = 0
        for year in per_year_data:
            total += year[2]
        f_per_year_data = [[year[0], year[1], number_format(year[2])] for year in per_year_data]
        total = number_format(total)
        years = [str(year[0]) for year in per_year_data]
        bond_values = [year[2] for year in per_year_data]

        # for party wise data
        query = f"SELECT `Name of the Political Party`, bp.Denominations FROM bonds_encashed_by_parties be JOIN bonds_purchased bp ON be.`Bond Number` = bp.`Bond Number` AND be.Prefix = bp.Prefix WHERE `Name of the Purchaser` = '{company_name}'"
        cursor.execute(query)
        raw_data = cursor.fetchall()
        party_total_denom_data = {}
        for row in raw_data:
            party_name = row[0]
            locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
            denom = locale.atoi(row[1])
            party_total_denom_data[party_name] = party_total_denom_data.get(party_name, 0) + denom

        party_data = [[party, party_total_denom_data.get(party)] for party in list(party_total_denom_data.keys())]
        f_party_data = [[party[0], number_format(party[1])] for party in party_data]
        parties = [str(party[0]) for party in party_data]
        party_bond_values = [party[1] for party in party_data]
        return render_template("company.html", searching=True, names=company_names, selected_name=company_name,
                               total=total,
                               year_data=f_per_year_data, years=years, year_data_values=bond_values,
                               party_data=f_party_data, parties=parties, party_data_values=party_bond_values)


@app.route("/search_party", methods=["GET", "POST"])
def search_by_party():
    return render_template("party.html")


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80, debug=True)
