#Checagem de URLs/APIs

import requests
import time

def check_url(url):
    start = time.time()
    try:
        r = requests.get(url, timeout=10)
        status = r.status_code
        ok = True
    except Exception:
        status = 0
        ok = False
    response_time = round(time.time() - start, 3)

    return {
        "status": status,
        "response_time": response_time,
        "ok": ok
    }