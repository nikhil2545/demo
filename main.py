import flask
import pandas as pd
import sqlite3
import json


app = flask.Flask(__name__)
@app.route('/data',methods=['GET'])
def get_data():
    well = flask.request.args.get('well')
    df = pd.read_excel(r'doubt.xls')
    conn = sqlite3.connect('database.db')
    df.to_sql('table_name', conn, if_exists='replace', index=False)
    cursor = conn.cursor()
    cursor.execute('SELECT *  FROM table_name')
    rows = cursor.fetchall()
    result = []
    for row in rows:
        result.append(dict(zip([column[0] for column in cursor.description], row)))
    json_data = json.dumps(result)
    dict_data = json.loads(json_data)
    index_Of_api = []
    oil_total = 0
    gas_total = 0
    brine_total = 0
    for d in dict_data:
        if d['API WELL  NUMBER'] == int(well):
            index_Of_api.append(d)
            for i in index_Of_api:
                if d['QUARTER 1,2,3,4']:
                    oil_total = oil_total + i['OIL']
            for i in index_Of_api:
                 if d['QUARTER 1,2,3,4']:
                     gas_total = gas_total + i['GAS']
            for i in index_Of_api:
                if d['QUARTER 1,2,3,4']:
                    brine_total = brine_total + i['BRINE']

    return flask.jsonify({"oil":oil_total},
                         {"gas":gas_total},
                         {"brine":brine_total})

if __name__ == '__main__':
    app.run(debug=True,port=8080)