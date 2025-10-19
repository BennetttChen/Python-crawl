from typing import List, Dict
from dateutil import parser as dtp
from .steam_util import get_news_for_app

def fetch_steam_news(appids: List[int], limit_per_app: int = 5) -> List[Dict]:
    all_items: List[Dict] = []
    for appid in appids:
        data = get_news_for_app(appid=appid, count=limit_per_app)
        if not data: continue
        appnews = data.get("appnews", {})
        newsitems = appnews.get("newsitems", []) or []
        appid_value = appnews.get("appid") or appid
        for n in newsitems:
            dt = n.get("date")
            published = ""
            if dt:
                try: published = dtp.parse(str(dt), fuzzy=True).strftime("%Y-%m-%d %H:%M")
                except Exception: published = str(dt)
            all_items.append({
                "appid": appid_value,
                "title": n.get("title"),
                "link": n.get("url"),
                "author": n.get("author"),
                "published": published,
                "summary": (n.get("contents") or "").replace("\\r"," ").replace("\\n"," ").strip()[:400],
                "source": "Steam News API"
            })
    return all_items
'@ | Set-Content .\freshfeeds\sources\steam_news.py -Encoding UTF8
