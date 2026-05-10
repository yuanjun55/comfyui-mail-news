#!/usr/bin/env python3
import os
import pytz
from datetime import datetime
from github import Github, Auth

# 路径
README_PATH = "README.md"

def get_top_comfyui():
    try:
        auth = Auth.Token(os.getenv("GITHUB_TOKEN"))
        g = Github(auth=auth)
    except:
        g = Github(os.getenv("GITHUB_TOKEN"))

    repos = g.search_repositories("comfyui", sort="stars", order="desc")
    lines = []
    tz = pytz.timezone("Asia/Shanghai")
    now = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")

    lines.append("# 📰 ComfyUI 每日热门插件排行榜")
    lines.append(f"**自动更新时间：{now}（北京时间）**")
    lines.append("---\n")

    count = 0
    for repo in repos:
        if count >= 20:  # 这里改成 20 条
            break
        count += 1
        star = repo.stargazers_count
        name = repo.full_name
        url = repo.html_url
        desc = repo.description or "无描述"
        update = repo.pushed_at.strftime("%Y-%m-%d")

        lines.append(f"## 【第{count}名】⭐ {star} 收藏")
        lines.append(f"- **项目**：[{name}]({url})")
        lines.append(f"- **描述**：{desc}")
        lines.append(f"- **更新时间**：{update}")
        lines.append("---\n")

    return "\n".join(lines)

def write_readme(content):
    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(content)
    print("✅ README.md 已自动更新！")

if __name__ == "__main__":
    content = get_top_comfyui()
    write_readme(content)
