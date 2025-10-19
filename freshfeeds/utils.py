@'
import time
import requests

DEFAULT_TIMEOUT = 20

def make_session(user_agent: str) -> requests.Session:
    s = requests.Session()
    s.headers.update({"User-Agent": user_agent})
    return s

def politely_wait(seconds: float):
    if seconds and seconds > 0:
        time.sleep(seconds)

def get_json(session: requests.Session, url: str, delay: float = 0.0, timeout: int = DEFAULT_TIMEOUT):
    resp = session.get(url, timeout=timeout)
    resp.raise_for_status()
    politely_wait(delay)
    return resp.json()
'@ | Set-Content .\freshfeeds\utils.py -Encoding UTF8
