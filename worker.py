#Job automático de monitoramento
#Esse arquivo roda em background no host (Railway/Render) a cada X minutos

import time
from db import get_db
from monitor import check_url

while True:
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM targets")
    targets = cur.fetchall()

    for t in targets:
        result = check_url(t["url"])
        cur.execute(
            "INSERT INTO metrics (target_id, status, response_time) VALUES (%s, %s, %s)",
            (t["id"], result["status"], result["response_time"])
        )
        db.commit()

    time.sleep(300)  # 5 minutos