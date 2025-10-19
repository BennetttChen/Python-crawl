@'
import argparse, yaml
from . import __app_name__, __version__
from .output import save_json, save_csv, save_markdown
from .sources.bilibili import fetch_bili_timeline, fetch_bili_rank
from .sources.steam_news import fetch_steam_news

def main():
    parser = argparse.ArgumentParser(prog=__app_name__, description="Bilibili anime + Steam news (compliant sources).")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_b = sub.add_parser("bili", help="Bilibili anime sources")
    sb = p_b.add_subparsers(dest="bili_cmd", required=True)

    p_b_t = sb.add_parser("timeline", help="PGC timeline")
    p_b_t.add_argument("--limit", type=int, default=30)
    p_b_t.add_argument("--format", choices=["json","csv","md","all"], default="all")
    p_b_t.add_argument("--outdir", default="output")

    p_b_r = sb.add_parser("rank", help="Ranking (anime/bangumi)")
    p_b_r.add_argument("--category", choices=["anime","bangumi"], default=None)
    p_b_r.add_argument("--limit", type=int, default=20)
    p_b_r.add_argument("--format", choices=["json","csv","md","all"], default="all")
    p_b_r.add_argument("--outdir", default="output")

    p_s = sub.add_parser("steam", help="Steam News API")
    p_s.add_argument("--limit", type=int, default=5)
    p_s.add_argument("--format", choices=["json","csv","md","all"], default="all")
    p_s.add_argument("--outdir", default="output")

    args = parser.parse_args()

    if args.cmd == "bili" and args.bili_cmd == "timeline":
        items = fetch_bili_timeline(limit=args.limit)
        _export(items, args.format, args.outdir, "bili_timeline", "B站番剧时间表（PGC）")
    elif args.cmd == "bili" and args.bili_cmd == "rank":
        category = args.category
        if category is None:
            with open("config.yaml", "r", encoding="utf-8") as f:
                cfg = yaml.safe_load(f) or {}
            category = cfg.get("bilibili_rank_default_category","bangumi")
        items = fetch_bili_rank(category=category, limit=args.limit)
        _export(items, args.format, args.outdir, f"bili_rank_{category}", f"B站排行榜（{category}）")
    elif args.cmd == "steam":
        with open("config.yaml", "r", encoding="utf-8") as f:
            cfg = yaml.safe_load(f) or {}
        appids = cfg.get("steam_appids") or []
        items = fetch_steam_news(appids=appids, limit_per_app=args.limit)
        _export(items, args.format, args.outdir, "steam_news", "Steam 最新公告/更新")

def _export(items, fmt, outdir, name, title):
    paths = []
    if fmt in ("json","all"): paths.append(save_json(items, outdir, name))
    if fmt in ("csv","all"): paths.append(save_csv(items, outdir, name))
    if fmt in ("md","all"): paths.append(save_markdown(items, outdir, name, title))
    for p in paths: print(p)
'@ | Set-Content .\freshfeeds\cli.py -Encoding UTF8
