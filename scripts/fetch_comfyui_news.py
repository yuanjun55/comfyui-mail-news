#!/usr/bin/env python3
"""
ComfyUI Daily News Fetcher (163 邮箱版)
- 抓取热门插件更新，按收藏/更新时间排序
- 通过 163 邮箱发送每日邮件
"""
import os
import sys
import pytz
import smtplib
from datetime import datetime, timedelta, timezone
from github import Github
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ========= 配置信息 =========
# 从 GitHub Secrets 读取
SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", "465"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")
EMAIL_TO = os.getenv("EMAIL_TO")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# 抓取最近 7 天更新的插件，按收藏排序
TZ = pytz.timezone("Asia/Shanghai")
DAYS_BACK = 7
MAX_PLUGINS = 10  # 邮件里显示前 10 个热门插件

def fetch_comfyui_plugins():
    """抓取 GitHub 上 ComfyUI 相关热门插件"""
    g = Github(GITHUB_TOKEN)
    one_week_ago = datetime.now(TZ) - timedelta(days=DAYS_BACK)
    one_week_ago_utc = one_week_ago.astimezone(timezone.utc)

    # 搜索 ComfyUI 插件，按 stars 降序排序
    query = "topic:comfyui-plugin stars:>100"
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

def build_email_html(plugins):
    """生成邮件 HTML 内容"""
    date_str = datetime.now(TZ).strftime("%Y-%m-%d")
    html = f"""
    <h1>ComfyUI 每日资讯 - {date_str}</h1>
    <p>以下是最近更新的热门插件，按收藏数排序：</p>
    <hr>
    """
    for idx, p in enumerate(plugins, 1):
        html += f"""
        <h3>{idx}. <a href="{p['url']}">{p['name']}</a></h3>
        <p>⭐ 收藏数：{p['stars']} | 📅 最近更新：{p['updated']}</p>
        <p>📝 描述：{p['description']}</p>
        <hr>
        """
    return html

def send_email(html_content):
    """通过 163 SMTP 发送邮件"""
    msg = MIMEMultipart('alternative')
    msg['Subject'] = f"[ComfyUI 资讯] 每日更新 - {datetime.now(TZ).strftime('%Y-%m-%d')}"
    msg['From'] = SMTP_USER
    msg['To'] = EMAIL_TO

    part = MIMEText(html_content, 'html', 'utf-8')
    msg.attach(part)

    try:
        # 用 SSL 连接 163 邮箱
        server = smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT)
        server.login(SMTP_USER, SMTP_PASS)
        server.sendmail(SMTP_USER, [EMAIL_TO], msg.as_string())
        server.quit()
        print("✅ 邮件发送成功！")
    except Exception as e:
        print(f"❌ 邮件发送失败：{str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    print("正在抓取 ComfyUI 热门插件...")
    plugins = fetch_comfyui_plugins()
    if not plugins:
        print("⚠️  未找到最近更新的插件，邮件将不会发送")
        sys.exit(0)
    print(f"✅ 找到 {len(plugins)} 个热门插件")
    html = build_email_html(plugins)
    send_email(html)
