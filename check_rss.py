import feedparser
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import time
import requests
from urllib.error import URLError, HTTPError
from http.client import RemoteDisconnected
import json
import re

# RSS源列表
RSS_FEEDS = [
    "https://example.com/feed1.xml",
    "https://example.com/feed2.xml",
    # 添加更多RSS源...
]

# 上次检查时间文件
LAST_CHECK_FILE = "check/last_check.txt"

def get_last_check_time():
    if os.path.exists(LAST_CHECK_FILE):
        with open(LAST_CHECK_FILE, "r") as f:
            return float(f.read().strip())
    return 0

def update_last_check_time():
    with open(LAST_CHECK_FILE, "w") as f:
        f.write(str(time.time()))

def parse_feed(url):
    try:
        return feedparser.parse(url)
    except (URLError, HTTPError, RemoteDisconnected):
        print(f"Error fetching feed: {url}")
        return None

def get_subscribers_from_issues():
    repo = os.environ['GITHUB_REPOSITORY']
    token = os.environ['GH_PAT']
    url = f"https://api.github.com/repos/{repo}/issues?labels=subscribe&state=open"
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    response = requests.get(url, headers=headers)
    issues = json.loads(response.text)

    subscribers = []
    for issue in issues:
        if issue['title'].lower().startswith('订阅 rss 更新通知'):
            body = issue['body']
            email_match = re.search(r'邮箱地址:\s*(.+@.+\..+)', body)
            if email_match:
                email = email_match.group(1).strip()
                subscribers.append((email, issue['number']))

    return subscribers

def check_and_notify():
    last_check = get_last_check_time()
    updated = False
    message_content = ""

    for feed_url in RSS_FEEDS:
        feed = parse_feed(feed_url)
        if feed is None:
            continue

        for entry in feed.entries:
            entry_time = time.mktime(entry.published_parsed)
            if entry_time > last_check:
                updated = True
                message_content += f"新文章: {entry.title}\n链接: {entry.link}\n\n"

    if updated:
        subscribers = get_subscribers_from_issues()
        for subscriber, issue_number in subscribers:
            unsubscribe_link = f"https://github.com/{os.environ['GITHUB_REPOSITORY']}/issues/{issue_number}"
            personalized_message = message_content + f"\n\n如果您想取消订阅，请访问此链接并关闭 issue：{unsubscribe_link}"
            send_email("RSS更新提醒", personalized_message, subscriber)
        update_last_check_time()
    else:
        print("没有RSS源更新")

def send_email(subject, message, recipient):
    msg = MIMEMultipart()
    msg['From'] = os.environ['EMAIL_USER']
    msg['To'] = recipient
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    server = smtplib.SMTP(os.environ['SMTP_SERVER'], os.environ['SMTP_PORT'])
    server.starttls()
    server.login(os.environ['EMAIL_USER'], os.environ['EMAIL_PASS'])
    server.send_message(msg)
    server.quit()
    print(f"邮件发送成功到 {recipient}")

if __name__ == "__main__":
    check_and_notify()
