# NeoHeberg 免费 VPS 自动续期脚本

每月自动续期 NeoHeberg 免费 VPS，成功/失败都通过 Telegram Bot 通知。

## 原理

- NeoHeberg 免费 VPS 每 31 天需手动续期一次（免费，0 coins）
- 本脚本配合定时任务，每月到期前 3 天自动登录面板点击续期
- 续期结果通过 Telegram Bot 推送通知

## 使用方法

1. 克隆本仓库
2. 创建 Telegram Bot（找 @BotFather），拿到 token
3. 给 Bot 发任意消息，然后通过 `https://api.telegram.org/bot<TOKEN>/getUpdates` 获取你的 chat ID
4. 在脚本目录创建两个文件：
   - `.bot-token`：写入 Bot token（仅一行）
   - `.chat-id`：写入你的 chat ID（仅一行）
5. 设置定时任务，每月运行一次：
   ```bash
   python3 renew.py  # 配合浏览器自动化完成续期后调用
   python3 renew.py --success      # 续期成功时发送通知
   python3 renew.py --failure "原因"  # 续期失败时发送通知
   python3 renew.py --test         # 测试通知通道
   ```

## 文件说明

- `renew.py`：主脚本，负责发送 Telegram 通知
- `.bot-token`（需自建，不在仓库中）：Telegram Bot token
- `.chat-id`（需自建，不在仓库中）：接收通知的 Telegram chat ID

## 注意

- `.bot-token` 和 `.chat-id` 包含敏感信息，切勿提交到公开仓库
- 续期本身需通过浏览器自动化登录 NeoHeberg 面板完成，本仓库仅提供通知模块
