#!/usr/bin/env python3
"""
ComfyUI Daily News - 极简测试版（只打印结果）
"""
import os
import sys
import pytz
from datetime import datetime, timedelta, timezone
from github import Github

# 配置
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
TZ = pytz.timezone("Asia/Shanghai")
DAYS_BACK = 7
MAX_PLUGINS = 5

def fetch_comfyui_plugins():
    g = Github(GITHUB_TOKEN)
    one_week_ago = datetime.now(TZ) - timedelta(days=DAYS_BACK)
    one_week_ago_utc = one_week_ago.astimezone(timezone.utc)

    query = "topic:comfyui-plugin stars:>50"
    repos = g.search_repositories(query=query, sort="stars", order="desc")

    plugins = []
    for repo in repos:
        if len(plugins) >= MAX_PLUGINS:
            break
        if repo.pushed_at >= one_week_ago_utc:
            plugins.append({
                "name": repo.full_name,
                "url": repo.html_url,
                "stars": repo.stargazers_count,
                "updated": repo.pushed_at.astimezone(TZ).strftime("%Y-%m-%d %H:%M"),
                "description": repo.description or "暂无描述"
            })
    return plugins

def main():
    print("=== ComfyUI Daily News ===")
    print(f"更新时间：{datetime.now(TZ).strftime('%Y-%m-%d %H:%M:%S')}")
    print("正在抓取插件...")

    plugins = fetch_comfyui_plugins()
    if not plugins:
        print("⚠️  未找到最近更新的插件")
        sys.exit(0)

    print(f"\n✅ 找到 {len(plugins)} 个热门插件：")
    for idx, p in enumerate(plugins, 1):
        print(f"\n{idx}. {p['name']}")
        print(f"   链接：{p['url']}")
        print(f"   收藏数：{p['stars']}")
        print(f"   更新时间：{p['updated']}")
        print(f"   描述：{p['description']}")

if __name__ == "__main__":
    main()
