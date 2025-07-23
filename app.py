from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import pyodbc
import os
from io import BytesIO

app = Flask(__name__)
CORS(app)

# SQL Server connection
server = '192.168.1.59,1500'    
database = 'ImageDB'
username = 'mkbairwa942'
password = 'vaa2829m'
driver = 'SQL Server Native Client 11.0'

conn_str = f"""
    DRIVER={driver};
    SERVER={server};
    DATABASE={database};
    UID={username};
    PWD={password};
"""
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

@app.route('/search', methods=['GET'])
def search_images():
    query = request.args.get('q', '')
    cursor.execute("SELECT Name FROM Images WHERE Name LIKE ?", ('%' + query + '%',))
    rows = cursor.fetchall()
    names = [row[0] for row in rows]
    return jsonify({'results': names})

@app.route('/image/<name>', methods=['GET'])
def get_image(name):
    cursor.execute("SELECT Image_Data FROM Images WHERE Name=?", (name,))
    row = cursor.fetchone()
    if row:
        return send_file(BytesIO(row[0]), mimetype='image/jpeg')
    return "Not found", 404

if __name__ == '__main__':
    #app.run(debug=True)
    #app.run(host="0.0.0.0", port=5000, debug=True)
    app.run(host='0.0.0.0', port=5000)
    #app.run(host="0.0.0.0", port=8080)



