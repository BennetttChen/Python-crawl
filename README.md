# FreshFeeds Bili + Steam

合规采集 **B 站番剧时间表 / 排行榜** 与 **Steam 官方新闻** 的 Python 小工具。
- 仅使用公开 JSON / 官方 API；不抓视频流或受限内容
- 导出 JSON / CSV / Markdown
- 自带 GitHub Actions 工作流，支持每日自动刷新输出

## 快速开始
```bash
python -m venv .venv
# Windows PowerShell:
# Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
# .\.venv\\Scripts\\Activate.ps1
pip install -r requirements.txt

# B站番剧时间表
python -m freshfeeds bili timeline --limit 15 --format all --outdir output

# B站排行榜（番剧区/bangumi 或 动画区/anime）
python -m freshfeeds bili rank --category bangumi --limit 20 --format md --outdir output

# Steam 新闻（在 config.yaml 里改 appid）
python -m freshfeeds steam --limit 8 --format all --outdir output
```

## GitHub Actions 自动刷新
工作流文件：`.github/workflows/refresh.yml`（已内置）  
默认每天北京时间 10:00 运行，也可在 Actions 页面手动点击 **Run workflow**。  
如需把 `output/` 提交到仓库，请保证 `.gitignore` 未忽略它（此包已允许提交全部 output）。
