from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def get_messages():
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            message_id INTEGER PRIMARY KEY,
            channel_name TEXT,
            send_date TEXT,
            message TEXT,
            translated TEXT,
            tema TEXT,
            yer1 TEXT,
            yer2 TEXT,
            yer3 TEXT,
            notlar TEXT
        )
    """)
    c.execute("SELECT COUNT(*) FROM messages")
    if c.fetchone()[0] == 0:
        c.execute("INSERT INTO messages (message_id, channel_name, send_date, message, translated) VALUES (?, ?, ?, ?, ?)",
                  (101, 'Мерсин 🍋', '2025-03-28', 'Orijinal mesaj örneği', 'Çevrilmiş mesaj örneği'))
    conn.commit()
    c.execute("SELECT * FROM messages ORDER BY send_date DESC")
    rows = c.fetchall()
    conn.close()
    return rows

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        conn = sqlite3.connect("data.db")
        c = conn.cursor()
        for key in request.form:
            if key.startswith("tema_"):
                msg_id = key.split("_")[1]
                tema = request.form.get(f"tema_{msg_id}")
                yer1 = request.form.get(f"yer1_{msg_id}")
                yer2 = request.form.get(f"yer2_{msg_id}")
                yer3 = request.form.get(f"yer3_{msg_id}")
                notlar = request.form.get(f"not_{msg_id}")
                c.execute("UPDATE messages SET tema=?, yer1=?, yer2=?, yer3=?, notlar=? WHERE message_id=?", 
                          (tema, yer1, yer2, yer3, notlar, msg_id))
        conn.commit()
        conn.close()
        return redirect("/")
    messages = get_messages()
    return render_template("index.html", messages=messages)

if __name__ == "__main__":
    app.run(debug=True)
