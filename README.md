<p align="center">
  <a href="https://github.com/BennetttChen/Python-crawl/actions/workflows/refresh.yml">
    <img src="https://github.com/BennetttChen/Python-crawl/actions/workflows/refresh.yml/badge.svg" alt="Refresh feeds">
  </a>
  <a href="https://github.com/BennetttChen/Python-crawl/releases">
    <img src="https://img.shields.io/github/v/release/BennetttChen/Python-crawl?display_name=tag" alt="Latest Release">
  </a>
  <a href="https://bennetttchen.github.io/Python-crawl/">
    <img src="https://img.shields.io/badge/Pages-live-blue" alt="GitHub Pages">
  </a>
</p>

## Features
- Bilibili PGC 时间表、番剧/动漫排行榜（合规、尊重 robots）
- Steam 官方新闻（ISteamNews API）
- 输出 **JSON / CSV / Markdown**
- GitHub Actions 每日自动刷新；自动 **Release + GitHub Pages**

## Quick Start (Local)
```bash
python -m venv .venv
# Windows PowerShell:
# Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
# .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Bilibili timeline
python -m freshfeeds bili timeline --limit 15 --format all --outdir output

# Bilibili rank
python -m freshfeeds bili rank --category bangumi --limit 20 --format md --outdir output

# Steam news (appids in config.yaml)
python -m freshfeeds steam --limit 8 --format all --outdir output
