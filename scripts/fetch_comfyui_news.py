#!/usr/bin/env python3
import os
import sys
import pytz
from datetime import datetime, timedelta, timezone
from github import Github, Auth

def main():
    print("=== 📰 ComfyUI 热门插件（必出结果版）===")
    print(f"时间：{datetime.now(pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M')}\n")

    try:
        auth = Auth.Token(os.getenv("GITHUB_TOKEN"))
        g = Github(auth=auth)
    except:
        g = Github(os.getenv("GITHUB_TOKEN"))

    # 宽松搜索：只要 ComfyUI 相关，按收藏排序
    repos = g.search_repositories("comfyui", sort="stars", order="desc")

    count = 0
    for repo in repos:
        if count >= 10:
            break
        count += 1
        print(f"【第{count}名】⭐ {repo.stargazers_count} 收藏")
        print(f"名称：{repo.full_name}")
        print(f"链接：{repo.html_url}")
        print(f"描述：{repo.description or '无'}")
        print(f"更新：{repo.pushed_at.strftime('%Y-%m-%d')}\n")

    print("✅ 抓取完成！上面就是最新热门插件排行榜")

if __name__ == "__main__":
    main()
