from flask import Flask, request, jsonify
import os
import psycopg2

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.route('/AddData', methods=["POST"])
def register():
    payload = request.get_json(force=True)
    temp = payload['temp']
    humid = payload['humid']
    DATABASE_URL = os.environ['DATABASE_URL']
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    # conn = sqlite3.connect('example.db')
    c = conn.cursor()
    # inset row of data
    c.execute('INSERT INTO records(temp,humid) VALUES(%s,%s)', (temp,humid))
    conn.commit()
    conn.close()
    resp = {'status':'OK'}
    return jsonify(resp)

@app.route('/summary', methods=["GET"])
def summary():
    temp = request.args.get('temp')
    humid = request.args.get('humid')
    DATABASE_URL = os.environ['DATABASE_URL']
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    #conn = sqlite3.connect('example.db')
    c = conn.cursor()
    # if name != None and name != '':
    #     c.execute('SELECT * FROM records WHERE name=?', (name,))
    # else:
    c.execute('SELECT * FROM records')
    records = c.fetchall()
    results = []
    for r in records:
        results.append({'timestamp':r[1], 'temp':r[2] , 'humid':r[3]})
    conn.commit()
    conn.close()
    resp = {'status':'OK', 'results':results}
    return jsonify(resp)

if __name__ == '__main__':

    DATABASE_URL = os.environ['DATABASE_URL']
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    #conn = sqlite3.connect('example.db') # connect to database
    c = conn.cursor()   
    # create table 
    c.execute('''CREATE TABLE IF NOT EXISTS records
             (_id SERIAL PRIMARY KEY,
             TIMESTAMP timestamp without time zone DEFAULT now(),
             temp INTEGER NOT NULL,
             humid INTEGER NOT NULL)''')
    conn.commit() # commit change
    conn.close() # close connection
    app.run(debug=True)
