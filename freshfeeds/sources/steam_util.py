from typing import Dict, Any
from ..utils import make_session, get_json
import yaml

STEAM_NEWS_API = "https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid={appid}&count={count}"

def load_config_user_agent_delay():
    with open("config.yaml", "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f) or {}
    ua = cfg.get("user_agent") or "freshfeeds/1.0"
    delay = float(cfg.get("request_delay_seconds") or 0.8)
    return ua, delay

def get_news_for_app(appid: int, count: int = 5) -> Dict[str, Any]:
    user_agent, delay = load_config_user_agent_delay()
    sess = make_session(user_agent)
    url = STEAM_NEWS_API.format(appid=appid, count=count)
    data = get_json(sess, url, delay=delay)
    return data
