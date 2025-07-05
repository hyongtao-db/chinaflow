from flask import Flask, jsonify
from flask_cors import CORS
import psycopg2

app = Flask(__name__)
CORS(app)  # 全局允许跨域

# PostgreSQL 数据库配置
db_config = {
    "host": "127.0.0.1",
    "port": "5432",
    "user": "postgres",
    "password": "123456",
    "dbname": "postgres"
}

# 查询接口
@app.route("/getMoveData")
def get_move_data():
    try:
        conn = psycopg2.connect(**db_config)
        conn.set_client_encoding('UTF8')  # 或 'GBK' 视库情况
        cursor = conn.cursor()
        cursor.execute("SELECT from_city, to_city, value FROM move_data")
        rows = cursor.fetchall()

        result = []
        for row in rows:
            result.append({
                "from": row[0],
                "to": row[1],
                "value": row[2]
            })

        cursor.close()
        conn.close()
        return jsonify(result)

    except Exception as e:
        print("数据库查询出错:", e)
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
