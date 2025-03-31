#!/bin/bash

DEST=~/Masaüstü/flask_rus
mkdir -p $DEST/templates

# app.py
cat > $DEST/app.py << EOF
from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def get_messages():
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    c.execute(\"""
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
    \""")
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
EOF

# requirements.txt
echo "Flask==2.3.2" > $DEST/requirements.txt

# index.html
cat > $DEST/templates/index.html << EOF
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>Flask Telegram Etiketleme</title>
    <style>
        table { width: 100%; border-collapse: collapse; }
        th, td { border: 1px solid #ddd; padding: 8px; vertical-align: top; }
        input[type="text"], textarea { width: 100%; }
    </style>
</head>
<body>
    <h2>Telegram Mesaj Etiketleme (Flask)</h2>
    <form method="POST">
        <table>
            <tr>
                <th>ID</th>
                <th>Kanal</th>
                <th>Tarih</th>
                <th>Mesaj</th>
                <th>Çeviri</th>
                <th>Tema</th>
                <th>Yer1</th>
                <th>Yer2</th>
                <th>Yer3</th>
                <th>Not</th>
            </tr>
            {% for row in messages %}
            <tr>
                <td>{{ row[0] }}</td>
                <td>{{ row[1] }}</td>
                <td>{{ row[2] }}</td>
                <td>{{ row[3] }}</td>
                <td>{{ row[4] }}</td>
                <td><input type="text" name="tema_{{ row[0] }}" value="{{ row[5] or '' }}"></td>
                <td><input type="text" name="yer1_{{ row[0] }}" value="{{ row[6] or '' }}"></td>
                <td><input type="text" name="yer2_{{ row[0] }}" value="{{ row[7] or '' }}"></td>
                <td><input type="text" name="yer3_{{ row[0] }}" value="{{ row[8] or '' }}"></td>
                <td><textarea name="not_{{ row[0] }}">{{ row[9] or '' }}</textarea></td>
            </tr>
            {% endfor %}
        </table>
        <button type="submit">Kaydet</button>
    </form>
</body>
</html>
EOF

echo "✅ Flask klasörü ve dosyaları oluşturuldu: $DEST"
