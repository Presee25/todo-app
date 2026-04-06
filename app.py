from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)


# function to connect database
def get_db():
    conn = sqlite3.connect("tasks.db")
    return conn


# create table
conn = get_db()
conn.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task TEXT
)
""")
conn.close()


@app.route("/", methods=["GET", "POST"])
def home():
    conn = get_db()
    cursor = conn.cursor()

    if request.method == "POST":
        task = request.form.get("task")
        if task:
            cursor.execute("INSERT INTO tasks (task) VALUES (?)", (task,))
            conn.commit()

    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()

    conn.close()

    return render_template("index.html", tasks=tasks)


@app.route("/delete/<int:id>")
def delete(id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM tasks WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)