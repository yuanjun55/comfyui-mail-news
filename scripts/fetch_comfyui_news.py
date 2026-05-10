#!/usr/bin/env python3
"""
ComfyUI Daily News - 无邮箱版（直接写入 README.md）
"""
import os
import sys
import pytz
from datetime import datetime, timedelta, timezone
from github import Github

# 配置
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
README_PATH = os.path.join(REPO_ROOT, 'README.md')
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
TZ = pytz.timezone("Asia/Shanghai")
DAYS_BACK = 7  # 抓取最近 7 天更新的插件
MAX_PLUGINS = 15  # 显示前 15 个热门插件

def fetch_comfyui_plugins():
    """抓取 GitHub 上热门 ComfyUI 插件"""
    g = Github(GITHUB_TOKEN)
    one_week_ago = datetime.now(TZ) - timedelta(days=DAYS_BACK)
    one_week_ago_utc = one_week_ago.astimezone(timezone.utc)

    # 搜索 ComfyUI 插件，按收藏数排序
    query = "topic:comfyui-plugin stars:>50"
    repos = g.search_repositories(query=query, sort="stars", order="desc")

    plugins = []
    for repo in repos:
        if len(plugins) >= MAX_PLUGINS:
            break
        # 只保留最近 7 天有更新的插件
        if repo.pushed_at >= one_week_ago_utc:
            plugins.append({
                "name": repo.full_name,
                "url": repo.html_url,
                "stars": repo.stargazers_count,
                "updated": repo.pushed_at.astimezone(TZ).strftime("%Y-%m-%d %H:%M"),
                "description": repo.description or "暂无描述"
            })
    return plugins

def build_readme_content(plugins):
    """生成 README.md 内容"""
    date_str = datetime.now(TZ).strftime("%Y-%m-%d %H:%M:%S")
    content = f"""# ComfyUI 每日资讯 📰

更新时间：{date_str}（北京时间）

以下是最近更新的热门 ComfyUI 插件，按收藏数排序：

---

"""
    for idx, p in enumerate(plugins, 1):
        content += f"""## {idx}. [{p['name']}]({p['url']})
- ⭐ 收藏数：{p['stars']}
- 📅 最近更新：{p['updated']}
- 📝 描述：{p['description']}

---

"""
    return content

def main():
    print("正在抓取 ComfyUI 热门插件...")
    plugins = fetch_comfyui_plugins()
    if not plugins:
        print("⚠️  未找到最近更新的插件，README 不会更新")
        sys.exit(0)
    print(f"✅ 找到 {len(plugins)} 个热门插件，正在写入 README.md...")
    # 写入 README.md
    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(build_readme_content(plugins))
    print("✅ README.md 更新完成！")

if __name__ == "__main__":
    main()
