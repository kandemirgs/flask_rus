from flask import Flask, render_template, request, redirect
import mysql.connector
from datetime import datetime
import os

app = Flask(__name__)

# MariaDB bağlantı ayarları
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "1959",
    "database": "rus",
    "charset": "utf8mb4"
}

# Çevrilmiş mesajları getir
def get_translated_messages():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT message_id, channel_name, send_date, translated_message,
               tema1, tema2, yer1, yer2, yer3, extra, notlar
        FROM telegram_messages
        WHERE translated_message IS NOT NULL
        ORDER BY send_date DESC
        LIMIT 500
    """)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        for key in request.form:
            if key.startswith("tema1_"):
                msg_id = key.split("_")[1]
                tema1 = request.form.get(f"tema1_{msg_id}")
                tema2 = request.form.get(f"tema2_{msg_id}")
                yer1 = request.form.get(f"yer1_{msg_id}")
                yer2 = request.form.get(f"yer2_{msg_id}")
                yer3 = request.form.get(f"yer3_{msg_id}")
                extra = request.form.get(f"extra_{msg_id}")
                notlar = request.form.get(f"notlar_{msg_id}")
                cursor.execute("""
                    UPDATE telegram_messages
                    SET tema1=%s, tema2=%s, yer1=%s, yer2=%s, yer3=%s,
                        extra=%s, notlar=%s, tagged_at=%s
                    WHERE message_id=%s
                """, (tema1, tema2, yer1, yer2, yer3, extra, notlar, now, msg_id))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect("/")

    messages = get_translated_messages()
    return render_template("index.html", messages=messages)

# Render için uygun Flask başlatma komutu
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
# trigger rebuild
