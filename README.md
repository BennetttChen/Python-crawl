# FreshFeeds: Bilibili + Steam (Compliant)

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
# FreshFeeds Bili + Steam 🕷️

这是一个基于 **Python** 的信息采集项目，用于自动获取 **B 站番剧时间表** 与 **Steam 官方游戏公告**。

## ✨ 功能
- 获取 B 站番剧时间表（timeline）
- 抓取 Steam 官方新闻（news）
- 导出为 JSON / CSV / Markdown
- 支持 GitHub Actions 自动每日更新

- Bilibili PGC 时间表、番剧/动漫排行榜（合规、尊重 robots）
- Steam 官方新闻（ISteamNews API）
- 输出 **JSON / CSV / Markdown**
- GitHub Actions 每日自动刷新；自动 **Release + GitHub Pages**
  
合规采集 **B 站番剧时间表/排行榜** 与 **Steam 官方新闻**；输出 **JSON / CSV / Markdown**。  
遵守 robots，使用公开 API；每日自动刷新、自动 Release、自动发布 GitHub Pages。

## 本地运行
```bash
python -m venv .venv
# Windows PowerShell:
# Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
# .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# B 站番剧时间表
python -m freshfeeds bili timeline --limit 15 --format all --outdir output

# B 站排行榜：番剧区 / 或 --category anime
python -m freshfeeds bili rank --category bangumi --limit 20 --format md --outdir output

# Steam 新闻（appids 在 config.yaml）
python -m freshfeeds steam --limit 8 --format all --outdir output
