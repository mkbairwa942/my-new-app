from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import mysql.connector
from io import BytesIO

app = Flask(__name__)
CORS(app)

# ✅ MySQL connection setup
conn = mysql.connector.connect(
    host='192.168.1.59',
    port=3306,
    user='mkbairwa942',
    password='vaa2829m',
    database='ImageDB'
)

cursor = conn.cursor()

@app.route('/search', methods=['GET'])
def search_images():
    query = request.args.get('q', '')
    cursor.execute("SELECT Name FROM Images WHERE Name LIKE %s", ('%' + query + '%',))
    rows = cursor.fetchall()
    print("Query:", query, "Rows:", rows)  # 🔍 Print for debugging
    names = [row[0] for row in rows]
    return jsonify({'results': names})

@app.route('/image/<name>', methods=['GET'])
def get_image(name):
    cursor.execute("SELECT Image_Data FROM Images WHERE Name = %s", (name,))
    row = cursor.fetchone()
    if row:
        return send_file(BytesIO(row[0]), mimetype='image/jpeg')
    return "Not found", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
