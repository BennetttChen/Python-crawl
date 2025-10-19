from typing import List, Dict, Tuple
from dateutil import parser as dtp
from ..utils import make_session, get_json
import yaml

TIMELINE_API = "https://api.bilibili.com/pgc/web/timeline/v2?season_type=1&day_before=2&day_after=4"
RANK_API_V2 = "https://api.bilibili.com/x/web-interface/ranking/v2?rid={rid}&type=all"
FALLBACK_TIMELINE_API = "https://bangumi.bilibili.com/web_api/timeline_global"

def load_common():
    with open("config.yaml", "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f) or {}
    ua = cfg.get("user_agent") or "freshfeeds/1.0"
    delay = float(cfg.get("request_delay_seconds") or 0.8)
    rank_default = (cfg.get("bilibili_rank_default_category") or "bangumi").lower()
    return ua, delay, rank_default

def fetch_bili_timeline(limit: int = 30) -> List[Dict]:
    ua, delay, _ = load_common()
    s = make_session(ua)
    items: List[Dict] = []
    # New API
    try:
        data = get_json(s, TIMELINE_API, delay=delay)
        result = data.get("result") or data.get("data") or {}
        for day in result.get("timeline", []):
            for ep in day.get("episodes", []):
                title = f"{ep.get('pub_index','')} {ep.get('title','')}".strip()
                ts = ep.get("pub_ts") or ep.get("pub_time") or ""
                pub = str(ts)
                try:
                    if ts: pub = dtp.parse(str(ts)).strftime("%Y-%m-%d %H:%M")
                except Exception: pass
                season_id = ep.get("season_id") or ep.get("season_id_str") or ""
                ep_id = ep.get("ep_id") or ep.get("episode_id") or ""
                link = f"https://www.bilibili.com/bangumi/play/ss{season_id}" if season_id else \
                       (f"https://www.bilibili.com/bangumi/play/ep{ep_id}" if ep_id else "")
                items.append({
                    "title": title or ep.get("long_title") or ep.get("share_copy") or "",
                    "link": link,
                    "published": pub,
                    "summary": ep.get("share_copy") or ep.get("subtitle") or "",
                    "source": "Bilibili PGC Timeline"
                })
                if len(items) >= limit: return items
    except Exception:
        pass
    # Fallback
    try:
        data = get_json(s, FALLBACK_TIMELINE_API, delay=delay)
        for day in data.get("result", []):
            for ep in day.get("seasons", []):
                items.append({
                    "title": ep.get("title") or ep.get("pub_index") or "",
                    "link": ep.get("url") or "",
                    "published": str(ep.get("pub_date") or ep.get("pub_time") or ""),
                    "summary": ep.get("pub_time") or "",
                    "source": "Bilibili Timeline (legacy)"
                })
                if len(items) >= limit: return items
    except Exception:
        pass
    return items[:limit]

def _rid_for_category(category: str) -> Tuple[int, str]:
    c = (category or "bangumi").lower()
    if c in ("anime","animation","donghua","鍔ㄧ敾","dongman"):
        return 1, "anime"
    return 13, "bangumi"

def fetch_bili_rank(category: str = "bangumi", limit: int = 20) -> List[Dict]:
    ua, delay, _ = load_common()
    s = make_session(ua)
    rid, cname = _rid_for_category(category)
    url = RANK_API_V2.format(rid=rid)
    items: List[Dict] = []
    try:
        data = get_json(s, url, delay=delay)
        lst = (data.get("data") or {}).get("list") or []
        for it in lst[:limit]:
            stat = it.get("stat") or {}
            owner = it.get("owner") or {}
            title = it.get("title") or it.get("name") or it.get("short_title") or ""
            bvid = it.get("bvid") or ""
            season_id = it.get("season_id") or it.get("season_id_str") or ""
            link = f"https://www.bilibili.com/video/{bvid}" if bvid else \
                   (f"https://www.bilibili.com/bangumi/play/ss{season_id}" if season_id else "")
            items.append({
                "title": title,
                "link": link,
                "published": str(it.get("pubdate") or it.get("ctime") or it.get("publish_time") or ""),
                "summary": it.get("desc") or it.get("evaluate") or "",
                "view": stat.get("view") or it.get("play") or None,
                "like": stat.get("like") or None,
                "author": owner.get("name") or it.get("subtitle") or "",
                "source": f"Bilibili Ranking ({cname})"
            })
    except Exception:
        pass
    return items[:limit]
'@ | Set-Content .\freshfeeds\sources\bilibili.py -Encoding UTF8
