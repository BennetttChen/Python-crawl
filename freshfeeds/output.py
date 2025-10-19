import csv, json
from pathlib import Path
from typing import List, Dict

def ensure_outdir(outdir: str) -> Path:
    p = Path(outdir)
    p.mkdir(parents=True, exist_ok=True)
    return p

def save_json(items: List[Dict], outdir: str, name: str) -> str:
    out = ensure_outdir(outdir) / f"{name}.json"
    out.write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")
    return str(out)

def save_csv(items: List[Dict], outdir: str, name: str) -> str:
    out = ensure_outdir(outdir) / f"{name}.csv"
    if not items:
        out.touch()
        return str(out)
    keys = sorted({k for it in items for k in it.keys()})
    with out.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=keys)
        w.writeheader()
        for it in items:
            w.writerow(it)
    return str(out)

def save_markdown(items: List[Dict], outdir: str, name: str, title: str) -> str:
    out = ensure_outdir(outdir) / f"{name}.md"
    lines: List[str] = ["# " + title, ""]
    for it in items:
        t = it.get("title") or it.get("name") or "Untitled"
        link = it.get("link") or it.get("url") or ""
        pub = it.get("published") or it.get("date") or ""
        summary = it.get("summary") or it.get("desc") or ""
        src = it.get("source") or ""

        lines.append(f"- **{t}**  ")
        if pub:
            lines.append(f"  发布: {pub}  ")
        if src:
            lines.append(f"  来源: {src}  ")
        if link:
            lines.append(f"  链接: {link}  ")

        if summary:
            s = summary.replace("\n", " ").strip()
            snippet = s[:280]
            if len(s) > 280:
                snippet += "…"
            lines.append("  摘要: " + snippet)
            lines.append("")  # 空行分隔

    out.write_text("\n".join(lines).strip() + "\n", encoding="utf-8")
    return str(out)
