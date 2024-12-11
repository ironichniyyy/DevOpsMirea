
from flask import Flask, request, jsonify, render_template
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# Database connection settings
DB_CONFIG = {
    "host": "db",  # The service name defined in docker-compose.yml
    "user": "root",
    "password": "example",
    "database": "testdb",
}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/execute", methods=["POST"])
def execute_query():
    query = request.form.get("query")
    if not query:
        return jsonify({"status": "error", "message": "No query provided"}), 400

    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()
        cursor.execute(query)
        if query.lower().startswith("select"):
            results = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            response = {"status": "success", "columns": columns, "results": results}
        else:
            connection.commit()
            response = {"status": "success", "message": "Query executed successfully"}

        cursor.close()
        connection.close()
        return jsonify(response)
    except Error as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

