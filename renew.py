#!/usr/bin/env python3
"""
NeoHeberg 免费 VPS 自动续期脚本
- 每月运行一次（到期前 3 天）
- 通过浏览器自动登录面板点击续期
- 成功/失败都通过 Telegram bot 通知用户
"""
import os
import sys
import json
import urllib.request
import urllib.parse
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TOKEN_FILE = os.path.join(BASE_DIR, ".bot-token")
CHAT_ID_FILE = os.path.join(BASE_DIR, ".chat-id")
LOG_FILE = os.path.join(BASE_DIR, "renew.log")


def log(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line, flush=True)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")


def send_tg(text):
    """通过续期通知 bot 发送 Telegram 消息"""
    try:
        with open(TOKEN_FILE) as f:
            token = f.read().strip()
        with open(CHAT_ID_FILE) as f:
            chat_id = f.read().strip()
        data = urllib.parse.urlencode(
            {"chat_id": chat_id, "text": text}
        ).encode()
        req = urllib.request.Request(
            f"https://api.telegram.org/bot{token}/sendMessage", data=data
        )
        with urllib.request.urlopen(req, timeout=30) as r:
            result = json.load(r)
            return result.get("ok", False)
    except Exception as e:
        log(f"TG 发送失败: {e}")
        return False


def main():
    log("=== NeoHeberg VPS 续期任务开始 ===")
    # 续期操作由 cron 的 agent 通过浏览器任务执行
    # 本脚本负责 TG 通知的发送端点
    # 实际调用时传入 --success 或 --failure 参数
    if len(sys.argv) > 1:
        if sys.argv[1] == "--success":
            msg = "✅ NeoHeberg 免费 VPS 续期成功\n延后 31 天，节点继续运行"
            log("续期成功，发送通知")
            send_tg(msg)
        elif sys.argv[1] == "--failure":
            reason = sys.argv[2] if len(sys.argv) > 2 else "未知原因"
            msg = f"❌ NeoHeberg 免费 VPS 续期失败\n原因: {reason}\n请手动检查面板"
            log(f"续期失败，发送通知: {reason}")
            send_tg(msg)
        elif sys.argv[1] == "--test":
            msg = "🔄 NeoHeberg 续期通知测试：bot 工作正常"
            log("发送测试通知")
            ok = send_tg(msg)
            log(f"测试通知发送{'成功' if ok else '失败'}")
        else:
            log(f"未知参数: {sys.argv[1]}")
    else:
        log("用法: renew.py --success | --failure [原因] | --test")
    log("=== 续期任务结束 ===")


if __name__ == "__main__":
    main()
