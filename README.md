<div align="center">

# 🦉 OWO AUTO TOOL v2.0

**An advanced, multi-threaded, Discord-themed GUI automation tool for the OwO Discord Bot.**

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![GUI](https://img.shields.io/badge/GUI-Tkinter-4B8BBE?style=for-the-badge&logo=python&logoColor=white)](https://docs.python.org/3/library/tkinter.html)
[![Author](https://img.shields.io/badge/author-Haribo-7289da.svg?style=for-the-badge)](https://github.com/)
[![Version](https://img.shields.io/badge/version-2.0-brightgreen.svg?style=for-the-badge)](https://github.com/)
[![License](https://img.shields.io/badge/license-MIT-green.svg?style=for-the-badge)](LICENSE)

[Features](#-features) • [Installation](#-installation) • [Configuration](#-configuration) • [Usage](#-usage) • [Safety & Anti-Ban](#-safety--anti-ban) • [Disclaimer](#-disclaimer)

</div>

---

## ✨ Features

### ⚔️ Automated Actions
- **Auto Hunt & Battle:** Periodically sends `owo h` and `owo b` with randomized intervals.
- **Auto Pray / Curse:** Regularly performs `owo pray` or `owo curse` to boost streak and economy.
- **Auto Daily:** Automatically claims your `owo daily` rewards.
- **Auto Sell:** Sells inventory clutter with `owo sell all`.
- **Casino Games:**
  - **Auto Slots:** Automated `owo s <amount>` with configurable bet sizes.
  - **Auto CoinFlip:** Automated `owo cf <amount>` gambling.
- **Inventory & Buffs:**
  - **Auto Gems:** Automatically equips gems (`owo use <gem_ids>`) before hunting/battling.
  - **Auto Lootbox:** Opens lootboxes automatically (`owo lb all`).
  - **Auto Cookie:** Sends `owo cookie <user>` to friends or alts.
  - **HuntBot:** Automates claim and upgrade cycles for OwO HuntBot.

### 🛡️ Safety & Anti-Detection
- **Automated Captcha Detection:** Continuously scans incoming messages for bot check triggers (captcha, verify, human, suspended, etc.).
- **Emergency Auto-Pause:** Instantly pauses all operations across all channels if a captcha is suspected.
- **Human-like Delays:** Customizable randomized intervals (`delay_min` to `delay_max`) to simulate natural human typing speeds.
- **Multi-Channel Rotation:** Distributes commands across multiple channels with independent timers to reduce channel spam.

### 🔔 Webhook Alerts & Logging
- **Discord Webhook Integration:** Sends immediate rich embeds to your private Discord server for:
  - 🚨 **Captcha Detection Alert** (instant ping so you can solve it manually)
  - 💰 **Daily Claim Notification**
  - 🤖 **HuntBot Status**
  - 💸 **Low Balance Warning**
- **Live GUI Logger & File Logs:** Displays timestamped, categorized actions in real-time within the UI and persists daily logs to `/logs`.

---

## 📸 Interface Preview

```text
+-----------------------------------------------------------------------------------+
|  OWO AUTO TOOL v2.0 -- Made By Haribo                                  [-][o][x]  |
+-----------------------------------------------------------------------------------+
| [Token Input] [Connect]   Status: Connected as User#0001 (ID: 1234567890)        |
+-----------------------------------------+-----------------------------------------+
| Automation Controls                     | Live Activity Log                       |
| [X] Auto Hunt    [X] Auto Battle        | [14:02:10] [INFO] [HUNT] owo h sent     |
| [X] Auto Pray    [X] Auto Daily         | [14:02:15] [INFO] [BATTLE] owo b sent   |
| [ ] Auto Slot    [ ] Auto CoinFlip      | [14:02:22] [INFO] [PRAY] owo pray sent  |
| [X] Auto Gems    [X] Auto Lootbox       | [14:03:00] [STAT] Total Hunts: 142      |
|                                         |                                         |
| Multi-Channel Manager                   | Live Statistics                         |
| - Channel 1 (Delay: 3.0s - 6.0s)        | Running Time: 01:24:35                  |
| - Channel 2 (Delay: 4.0s - 7.5s)        | Hunts: 142 | Battles: 139 | Dailies: 1  |
+-----------------------------------------+-----------------------------------------+
| Webhook: https://discord.com/api/webhooks/...  [X] Enable Webhook Notifications   |
+-----------------------------------------------------------------------------------+
```

---

## 🚀 Installation

### 1. Prerequisites
- **Python 3.8+** installed on your system.

### 2. Setup
Clone or navigate to the folder:
```powershell
cd "C:\Users\Haribooo\Desktop\tool\owo tool"
```

Install the required library (`requests`):
```powershell
pip install -r requirements.txt
```

---

## 💻 Usage

### Quick Start (Windows)
Double-click [`run.bat`](file:///C:/Users/Haribooo/Desktop/tool/owo%20tool/run.bat) or run via terminal:
```powershell
python owo_tool.py
```

### Setup Steps:
1. **Discord Token:** Paste your Discord account token into the token field and click **Connect**.
2. **Channel IDs:** Add the ID(s) of the channel(s) where you want the bot to type commands.
3. **Configure Delays:** Adjust the minimum and maximum random delays (recommended: 3.5s - 7.0s).
4. **Select Features:** Toggle the modules you want active (Hunt, Battle, Pray, Daily, etc.).
5. **Webhook Notifications (Optional):** Paste a Discord Webhook URL and toggle **Enable** to receive alerts on your phone or private server.
6. **Start:** Click **Start Automation**.

---

## 📂 File Structure

```text
owo tool/
│
├── owo_tool.py           # Main application with Tkinter GUI & automation engine
├── run.bat               # Windows batch launcher
├── requirements.txt      # Dependencies (requests)
├── README.md             # Project documentation
│
└── logs/                 # Auto-generated daily log directory
    └── owo_YYYY-MM-DD.txt
```

---

## 🛡️ Safety & Anti-Ban Best Practices

1. **Avoid Extreme Delays:** Do not set delays under 2.5 seconds. Faster speeds trigger rate limits and captcha systems quickly.
2. **Use Multiple Channels:** Rotate between 2 or more channels to spread out message frequency.
3. **Keep Webhook Enabled:** Always configure a Discord Webhook so you are notified immediately when a captcha pops up.
4. **Don't Run 24/7 Unattended:** Run in realistic play intervals (1-2 hours at a time).

---

## ⚖️ Disclaimer

This tool is created for **educational and research purposes only**. 
Using automated scripts or self-bots on Discord accounts violates Discord's Terms of Service and may result in account termination. Use at your own discretion and risk.
