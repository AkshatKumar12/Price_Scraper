import time
from collections import defaultdict
from config import Config

requests_log = defaultdict(list)

def check_rate_limit(ip):
    now = time.time()
    window = 60

    requests_log[ip] = [t for t in requests_log[ip] if now - t < window]

    if len(requests_log[ip]) >= Config.RATE_LIMIT:
        return False

    requests_log[ip].append(now)
    return True
