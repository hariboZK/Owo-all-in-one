#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ════════════════════════════════════════════════
#   OWO AUTO TOOL v2.0  -  Made By Haribo
# ════════════════════════════════════════════════
# Auto Hunt | Battle | Pray | Daily | Sell | Slot
# CoinFlip | Cookie | HuntBot | Gems | Lootbox
# Multi-Channel | Webhook | Captcha Detect | Logging
# ════════════════════════════════════════════════

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import threading
import requests
import time
import random
import json
import os
import sys
import re
from datetime import datetime, date
from collections import defaultdict

# ─── Renkler (Discord tema) ──────────────────────
BG      = "#0a0a0a"
BG2     = "#111111"
BG3     = "#1e1e2e"
ACCENT  = "#7289da"   # Discord blue
TEXT    = "#dcddde"
SUBTEXT = "#72767d"
GREEN   = "#43b581"
YELLOW  = "#faa61a"
RED     = "#f04747"
BLUE    = "#00b0f4"
PURPLE  = "#b9bffe"
ORANGE  = "#ffa500"
PINK    = "#ff69b4"
DARK    = "#2c2f33"

# ─── Discord API ────────────────────────────────
API_BASE = "https://discord.com/api/v9"
OWO_BOT_ID = "408785106942164992"

# ─── Stats (global) ─────────────────────────────
STATS = defaultdict(int)
SESSION_START = datetime.now()


# ════════════════════════════════════════════════
# DISCORD CLIENT
# ════════════════════════════════════════════════
class DiscordClient:
    def __init__(self, token: str):
        self.token = token
        self.headers = {
            "Authorization": token,
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "X-Super-Properties": "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRGlzY29yZCIsImRldmljZSI6IiIsInN5c3RlbV9sb2NhbGUiOiJlbi1VUyIsImJyb3dzZXJfdXNlcl9hZ2VudCI6Ik1vemlsbGEvNS4wIiwiYnJvd3Nlcl92ZXJzaW9uIjoiMjcuNy4xIiwib3NfdmVyc2lvbiI6IjEwIn0=",
        }
        self.me = None

    def get_me(self):
        try:
            r = requests.get(f"{API_BASE}/users/@me", headers=self.headers, timeout=8)
            if r.status_code == 200:
                self.me = r.json()
                return self.me
        except Exception as e:
            return None

    def send_message(self, channel_id: str, content: str) -> dict:
        try:
            payload = {"content": content}
            r = requests.post(
                f"{API_BASE}/channels/{channel_id}/messages",
                headers=self.headers,
                json=payload,
                timeout=8,
            )
            return r.json() if r.status_code in [200, 201] else {"error": r.status_code, "raw": r.text}
        except Exception as e:
            return {"error": str(e)}

    def get_messages(self, channel_id: str, limit: int = 10) -> list:
        try:
            params = {"limit": limit}
            r = requests.get(
                f"{API_BASE}/channels/{channel_id}/messages",
                headers=self.headers,
                params=params,
                timeout=8,
            )
            if r.status_code == 200:
                return r.json()
        except Exception:
            pass
        return []

    def get_channel_info(self, channel_id: str) -> dict:
        try:
            r = requests.get(f"{API_BASE}/channels/{channel_id}", headers=self.headers, timeout=6)
            if r.status_code == 200:
                return r.json()
        except:
            pass
        return {}


# ════════════════════════════════════════════════
# WEBHOOK NOTIFIER
# ════════════════════════════════════════════════
class WebhookNotifier:
    def __init__(self, url: str = ""):
        self.url = url
        self.enabled = False

    def send(self, title: str, description: str, color: int = 0x7289da, fields: list = None):
        if not self.enabled or not self.url:
            return
        try:
            embed = {
                "title": title,
                "description": description,
                "color": color,
                "timestamp": datetime.utcnow().isoformat(),
                "footer": {"text": "OWO Tool v2.0 | Made By Haribo"},
            }
            if fields:
                embed["fields"] = fields
            payload = {"embeds": [embed], "username": "OWO Tool | Haribo"}
            requests.post(self.url, json=payload, timeout=6)
        except Exception:
            pass

    def notify_captcha(self, channel_id: str):
        self.send(
            "⚠️ CAPTCHA TESPİT EDİLDİ",
            f"Channel `{channel_id}` içinde captcha algılandı!\nBot **duraklatıldı** — manuel çöz.",
            color=0xff0000,
        )

    def notify_daily(self, amount: str, channel_id: str):
        self.send(
            "💰 Daily Toplandı",
            f"Channel `{channel_id}`\nMiktar: **{amount}**",
            color=0x43b581,
        )

    def notify_huntbot(self, msg: str, channel_id: str):
        self.send(
            "🤖 HuntBot",
            f"Channel `{channel_id}`\n{msg}",
            color=0x7289da,
        )

    def notify_funds_low(self, balance: str):
        self.send(
            "💸 Bakiye Düşük",
            f"Mevcut bakiye: **{balance}**",
            color=0xfaa61a,
        )


# ════════════════════════════════════════════════
# LOGGER
# ════════════════════════════════════════════════
class Logger:
    def __init__(self, log_dir: str = "logs"):
        self.log_dir = log_dir
        os.makedirs(log_dir, exist_ok=True)
        self._callbacks = []
        self.today_file = os.path.join(log_dir, f"owo_{date.today().isoformat()}.txt")

    def add_callback(self, fn):
        self._callbacks.append(fn)

    def log(self, category: str, message: str, level: str = "INFO"):
        ts = datetime.now().strftime("%H:%M:%S")
        line = f"[{ts}] [{level}] [{category}] {message}"
        try:
            with open(self.today_file, "a", encoding="utf-8") as f:
                f.write(line + "\n")
        except Exception:
            pass
        for cb in self._callbacks:
            try:
                cb(category, message, level, ts)
            except Exception:
                pass

    def log_stat(self, key: str, value):
        STATS[key] = value
        self.log("STAT", f"{key} = {value}")


# ════════════════════════════════════════════════
# CAPTCHA DETECTOR
# ════════════════════════════════════════════════
CAPTCHA_KEYWORDS = [
    "captcha", "verify", "human", "robot", "i'm not a robot",
    "please verify", "suspicious", "automated", "banned", "suspended",
    "click the button", "prove you", "are you a bot",
]

def detect_captcha(message_content: str) -> bool:
    content_lower = message_content.lower()
    return any(kw in content_lower for kw in CAPTCHA_KEYWORDS)


# ════════════════════════════════════════════════
# CHANNEL CONFIG
# ════════════════════════════════════════════════
class ChannelConfig:
    def __init__(self):
        self.channels = []  # list of dicts

    def add(self, channel_id: str, delay_min: float = 3.0, delay_max: float = 6.0):
        self.channels.append({
            "id": channel_id.strip(),
            "delay_min": delay_min,
            "delay_max": delay_max,
            "enabled": True,
            "captcha_paused": False,
        })

    def remove(self, channel_id: str):
        self.channels = [c for c in self.channels if c["id"] != channel_id]

    def get_delay(self, channel_id: str) -> float:
        for c in self.channels:
            if c["id"] == channel_id:
                return random.uniform(c["delay_min"], c["delay_max"])
        return random.uniform(3, 6)


# ════════════════════════════════════════════════
# MAIN OWO TOOL GUI
# ════════════════════════════════════════════════
class OwoTool(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("OWO AUTO TOOL v2.0  --  Made By Haribo")
        self.geometry("1100x760")
        self.minsize(900, 620)
        self.configure(bg=BG)

        self.client: DiscordClient = None
        self.webhook = WebhookNotifier()
        self.logger = Logger()
        self.logger.add_callback(self._on_log)
        self.ch_cfg = ChannelConfig()

        self._running = False
        self._pause_all = False
        self._threads = []

        # Feature toggles
        self.feat_hunt       = tk.BooleanVar(value=True)
        self.feat_battle     = tk.BooleanVar(value=True)
        self.feat_pray       = tk.BooleanVar(value=True)
        self.feat_daily      = tk.BooleanVar(value=True)
        self.feat_sell       = tk.BooleanVar(value=True)
        self.feat_slot       = tk.BooleanVar(value=False)
        self.feat_coinflip   = tk.BooleanVar(value=False)
        self.feat_cookie     = tk.BooleanVar(value=True)
        self.feat_huntbot    = tk.BooleanVar(value=True)
        self.feat_gems       = tk.BooleanVar(value=True)
        self.feat_lootbox    = tk.BooleanVar(value=True)
        self.feat_owo_cmd    = tk.BooleanVar(value=True)
        self.feat_captcha_wh = tk.BooleanVar(value=True)
        self.feat_anti_detect= tk.BooleanVar(value=True)

        self._style()
        self._header()
        self._build_notebook()
        self._status_bar()

    def _style(self):
        s = ttk.Style(self)
        s.theme_use("clam")
        s.configure("TNotebook", background=BG, borderwidth=0)
        s.configure("TNotebook.Tab", background=BG3, foreground=TEXT,
                    padding=[16, 9], font=("Consolas", 10, "bold"))
        s.map("TNotebook.Tab",
              background=[("selected", ACCENT)],
              foreground=[("selected", "#ffffff")])
        s.configure("TCheckbutton", background=BG, foreground=TEXT,
                    font=("Consolas", 10), focuscolor="")
        s.map("TCheckbutton", background=[("active", BG)])

    def _header(self):
        h = tk.Frame(self, bg=BG2, height=56)
        h.pack(fill="x")
        h.pack_propagate(False)
        left = tk.Frame(h, bg=BG2)
        left.pack(side="left", padx=16, pady=8)
        tk.Label(left, text="☁  OWO AUTO TOOL", bg=BG2, fg=ACCENT,
                 font=("Consolas", 18, "bold")).pack(side="left")
        tk.Label(left, text=" v2.0", bg=BG2, fg=SUBTEXT,
                 font=("Consolas", 13)).pack(side="left", pady=4)
        right = tk.Frame(h, bg=BG2)
        right.pack(side="right", padx=16)
        tk.Label(right, text="Made By Haribo", bg=BG2, fg=SUBTEXT,
                 font=("Consolas", 10)).pack()
        tk.Frame(self, bg=ACCENT, height=2).pack(fill="x")

    def _build_notebook(self):
        nb = ttk.Notebook(self)
        nb.pack(fill="both", expand=True, padx=4, pady=4)
        self._tab_config(nb)
        self._tab_features(nb)
        self._tab_channels(nb)
        self._tab_stats(nb)
        self._tab_log(nb)
        self._tab_captcha(nb)
        self._tab_about(nb)

    def _status_bar(self):
        bar = tk.Frame(self, bg=BG3, height=28)
        bar.pack(fill="x", side="bottom")
        bar.pack_propagate(False)
        self.status_var = tk.StringVar(value="⚫  Hazır — Token gir ve Bağlan'a bas")
        self.status_lbl = tk.Label(bar, textvariable=self.status_var,
                                   bg=BG3, fg=SUBTEXT, font=("Consolas", 9), anchor="w")
        self.status_lbl.pack(side="left", padx=10)
        self.stat_var2 = tk.StringVar(value="")
        tk.Label(bar, textvariable=self.stat_var2,
                 bg=BG3, fg=GREEN, font=("Consolas", 9)).pack(side="right", padx=10)

    def _btn(self, parent, text, cmd, color=ACCENT, width=18, **kw):
        return tk.Button(parent, text=text, command=cmd,
                         bg=color, fg="#ffffff",
                         activebackground=color, activeforeground="#ffffff",
                         relief="flat", bd=0,
                         font=("Consolas", 9, "bold"),
                         cursor="hand2", width=width, pady=6, **kw)

    def _entry(self, parent, width=28, default="", show="", **kw):
        e = tk.Entry(parent, width=width, bg=BG3, fg=TEXT,
                     insertbackground=TEXT, relief="flat", bd=4,
                     font=("Consolas", 10), show=show, **kw)
        if default:
            e.insert(0, default)
        return e

    def _lf(self, parent, text, color=ACCENT):
        return tk.LabelFrame(parent, text=f"  {text}  ",
                             bg=BG, fg=color,
                             font=("Consolas", 9, "bold"),
                             bd=1, relief="groove")

    def _logbox(self, parent, height=10, fg=GREEN):
        return scrolledtext.ScrolledText(
            parent, height=height, bg=BG3, fg=fg,
            font=("Consolas", 9), state="disabled",
            relief="flat", bd=0, wrap="word"
        )

    def _log_write(self, widget, msg, color=None):
        widget.configure(state="normal")
        ts = datetime.now().strftime("%H:%M:%S")
        widget.insert("end", f"[{ts}] {msg}\n")
        widget.see("end")
        widget.configure(state="disabled")

    def set_status(self, msg: str, color: str = SUBTEXT):
        self.status_var.set(msg)
        self.status_lbl.configure(fg=color)

    def _on_log(self, category: str, message: str, level: str, ts: str):
        if hasattr(self, "log_widget"):
            color_map = {"ERROR": RED, "WARN": YELLOW, "INFO": GREEN, "STAT": BLUE}
            clr = color_map.get(level, GREEN)
            self.log_widget.configure(state="normal")
            self.log_widget.insert("end", f"[{ts}] ", "ts")
            self.log_widget.insert("end", f"[{level}] ", level)
            self.log_widget.insert("end", f"[{category}] ", "cat")
            self.log_widget.insert("end", f"{message}\n")
            self.log_widget.see("end")
            self.log_widget.configure(state="disabled")
        if hasattr(self, "stat_var2"):
            hunts = STATS["hunt_count"]
            battles = STATS["battle_count"]
            dailies = STATS["daily_count"]
            self.stat_var2.set(f"Hunt:{hunts}  Battle:{battles}  Daily:{dailies}")


    # ─── TAB: CONFIG ───────────────────────────────────────────────────────
    def _tab_config(self, nb):
        f = tk.Frame(nb, bg=BG)
        nb.add(f, text="  ⚙ CONFIG  ")

        # Token
        tf = self._lf(f, "Discord User Token (Selfbot)", RED)
        tf.pack(fill="x", padx=16, pady=(12, 5))
        tr = tk.Frame(tf, bg=BG)
        tr.pack(fill="x", padx=8, pady=6)
        tk.Label(tr, text="Token:", bg=BG, fg=SUBTEXT, font=("Consolas", 10)).pack(side="left", padx=4)
        self.token_entry = self._entry(tr, width=52, show="•")
        self.token_entry.pack(side="left", padx=6)
        self.show_token_var = tk.BooleanVar(value=False)
        tk.Checkbutton(tr, text="Göster", variable=self.show_token_var,
                       command=self._toggle_token_show,
                       bg=BG, fg=SUBTEXT, selectcolor=BG3,
                       activebackground=BG, font=("Consolas", 9)).pack(side="left", padx=4)
        self._btn(tr, "🔌 Bağlan & Doğrula", self._connect, color=GREEN, width=20).pack(side="left", padx=8)
        self.conn_status = tk.StringVar(value="⚫  Bağlı değil")
        tk.Label(tf, textvariable=self.conn_status, bg=BG, fg=SUBTEXT,
                 font=("Consolas", 10, "bold")).pack(anchor="w", padx=12, pady=(0, 6))
        tk.Label(tf, text="⚠ Selfbot Discord ToS'a aykırıdır. Riski sende.",
                 bg=BG, fg=RED, font=("Consolas", 8)).pack(anchor="w", padx=12, pady=(0, 5))

        # Webhook
        wf = self._lf(f, "Webhook Notifier", PURPLE)
        wf.pack(fill="x", padx=16, pady=5)
        wr = tk.Frame(wf, bg=BG)
        wr.pack(fill="x", padx=8, pady=6)
        tk.Label(wr, text="Webhook URL:", bg=BG, fg=SUBTEXT, font=("Consolas", 10)).pack(side="left", padx=4)
        self.webhook_entry = self._entry(wr, width=52)
        self.webhook_entry.pack(side="left", padx=6)
        self._btn(wr, "Test Gönder", self._test_webhook, color="#5865f2", width=12).pack(side="left", padx=6)
        self.wh_enable = tk.BooleanVar(value=True)
        tk.Checkbutton(wf, text="Webhook aktif", variable=self.wh_enable,
                       command=self._toggle_webhook,
                       bg=BG, fg=TEXT, selectcolor=BG3, activebackground=BG,
                       font=("Consolas", 10)).pack(anchor="w", padx=12, pady=(0, 5))

        # Prefix
        pf = self._lf(f, "OWO Prefix / Komut Ayarları", YELLOW)
        pf.pack(fill="x", padx=16, pady=5)
        pr = tk.Frame(pf, bg=BG)
        pr.pack(fill="x", padx=8, pady=6)
        tk.Label(pr, text="Prefix:", bg=BG, fg=SUBTEXT, font=("Consolas", 10)).pack(side="left", padx=4)
        self.prefix_entry = self._entry(pr, width=8, default="owo ")
        self.prefix_entry.pack(side="left", padx=4)
        tk.Label(pr, text="Battle Target (@user):", bg=BG, fg=SUBTEXT, font=("Consolas", 10)).pack(side="left", padx=12)
        self.battle_target = self._entry(pr, width=18, default="")
        self.battle_target.pack(side="left", padx=4)
        tk.Label(pr, text="Cookie Target:", bg=BG, fg=SUBTEXT, font=("Consolas", 10)).pack(side="left", padx=12)
        self.cookie_target = self._entry(pr, width=18, default="")
        self.cookie_target.pack(side="left", padx=4)

        pr2 = tk.Frame(pf, bg=BG)
        pr2.pack(fill="x", padx=8, pady=4)
        tk.Label(pr2, text="Sell Target:", bg=BG, fg=SUBTEXT, font=("Consolas", 10)).pack(side="left", padx=4)
        self.sell_target = self._entry(pr2, width=14, default="all")
        self.sell_target.pack(side="left", padx=4)
        tk.Label(pr2, text="Slot Bet:", bg=BG, fg=SUBTEXT, font=("Consolas", 10)).pack(side="left", padx=12)
        self.slot_bet = self._entry(pr2, width=8, default="100")
        self.slot_bet.pack(side="left", padx=4)
        tk.Label(pr2, text="CoinFlip Bet:", bg=BG, fg=SUBTEXT, font=("Consolas", 10)).pack(side="left", padx=12)
        self.cf_bet = self._entry(pr2, width=8, default="100")
        self.cf_bet.pack(side="left", padx=4)
        tk.Label(pr2, text="CF Side:", bg=BG, fg=SUBTEXT, font=("Consolas", 10)).pack(side="left", padx=12)
        self.cf_side = ttk.Combobox(pr2, values=["heads", "tails"], state="readonly", width=8, font=("Consolas", 9))
        self.cf_side.current(0)
        self.cf_side.pack(side="left", padx=4)

        # Gem / Lootbox
        gf = self._lf(f, "Gem & Lootbox Ayarları", BLUE)
        gf.pack(fill="x", padx=16, pady=5)
        gr = tk.Frame(gf, bg=BG)
        gr.pack(fill="x", padx=8, pady=6)
        tk.Label(gr, text="Gem Tipi:", bg=BG, fg=SUBTEXT, font=("Consolas", 10)).pack(side="left", padx=4)
        self.gem_type = ttk.Combobox(gr, values=["all", "lootbox gem", "luck gem", "experience gem", "fabled gem"], state="readonly", width=16, font=("Consolas", 9))
        self.gem_type.current(0)
        self.gem_type.pack(side="left", padx=4)
        tk.Label(gr, text="Lootbox Tipi:", bg=BG, fg=SUBTEXT, font=("Consolas", 10)).pack(side="left", padx=12)
        self.lb_type = ttk.Combobox(gr, values=["all", "lootbox", "epic lootbox", "fabled lootbox", "common lootbox"], state="readonly", width=16, font=("Consolas", 9))
        self.lb_type.current(0)
        self.lb_type.pack(side="left", padx=4)

        # Control
        ctrl = tk.Frame(f, bg=BG)
        ctrl.pack(pady=14)
        self._btn(ctrl, "▶  BOTU BAŞLAT", self._start_bot, color=GREEN, width=22).pack(side="left", padx=10)
        self._btn(ctrl, "⏹  DURDUR", self._stop_bot, color=RED, width=16).pack(side="left", padx=6)
        self._btn(ctrl, "⏸  DURAKLAT", self._pause_bot, color=YELLOW, width=14).pack(side="left", padx=6)
        self._btn(ctrl, "Config Kaydet", self._save_config, color="#333", width=14).pack(side="left", padx=6)
        self._btn(ctrl, "Config Yükle", self._load_config, color="#333", width=14).pack(side="left", padx=6)

    # ─── TAB: FEATURES ─────────────────────────────────────────────────────
    def _tab_features(self, nb):
        f = tk.Frame(nb, bg=BG)
        nb.add(f, text="  🎮 FEATURES  ")

        tk.Label(f, text="OTO FONKSİYONLAR  —  Her birini ayrı ayrı aç/kapat",
                 bg=BG, fg=ACCENT, font=("Consolas", 13, "bold")).pack(pady=(14, 6))

        container = tk.Frame(f, bg=BG)
        container.pack(fill="both", expand=True, padx=20)

        left = tk.Frame(container, bg=BG)
        left.pack(side="left", fill="y", padx=10)
        right = tk.Frame(container, bg=BG)
        right.pack(side="left", fill="y", padx=10)

        features_left = [
            ("🏹  Auto Hunt",        self.feat_hunt,       "owo hunt  |  Hayvan avlar"),
            ("⚔️  Auto Battle",      self.feat_battle,     "owo battle  |  Savaşır"),
            ("🙏  Auto Pray",        self.feat_pray,       "owo pray  |  Dua eder"),
            ("📅  Auto Daily",       self.feat_daily,      "owo daily  |  Günlük ödül alır"),
            ("💰  Auto Sell",        self.feat_sell,       "owo sell  |  Hayvanları satar"),
            ("🎰  Auto Slot",        self.feat_slot,       "owo slots  |  Slot oynar"),
        ]
        features_right = [
            ("🪙  Auto CoinFlip",   self.feat_coinflip,   "owo coinflip  |  Para atar"),
            ("🍪  Auto Cookie",     self.feat_cookie,     "owo cookie  |  Cookie verir"),
            ("🤖  Auto HuntBot",    self.feat_huntbot,    "owo huntbot  |  HuntBot satın alır/başlatır"),
            ("💎  Auto Use Gems",   self.feat_gems,       "owo gem use  |  Gem kullanır"),
            ("📦  Auto Lootbox",    self.feat_lootbox,    "owo lootbox open  |  Kutu açar"),
            ("🔰  Anti-Detection",  self.feat_anti_detect,"Random delay & typo simulation"),
        ]

        def make_row(parent, text, var, desc):
            row = tk.Frame(parent, bg=BG2, pady=2)
            row.pack(fill="x", pady=3)
            tk.Checkbutton(row, text=text, variable=var,
                           bg=BG2, fg=TEXT, selectcolor=BG3,
                           activebackground=BG2,
                           font=("Consolas", 11, "bold"),
                           width=24, anchor="w").pack(side="left", padx=8)
            tk.Label(row, text=desc, bg=BG2, fg=SUBTEXT, font=("Consolas", 8)).pack(side="left", padx=4)

        for text, var, desc in features_left:
            make_row(left, text, var, desc)
        for text, var, desc in features_right:
            make_row(right, text, var, desc)

        # Delay sliders
        df = self._lf(f, "Global Gecikme Ayarları (saniye)", YELLOW)
        df.pack(fill="x", padx=20, pady=12)
        dr = tk.Frame(df, bg=BG)
        dr.pack(fill="x", padx=8, pady=6)

        for col, (lbl, attr, dmin, dmax, ddef) in enumerate([
            ("Hunt Aralığı (s):", "hunt_delay", 1, 30, 6),
            ("Battle Aralığı:", "battle_delay", 1, 60, 20),
            ("Pray Aralığı:", "pray_delay", 1, 60, 30),
            ("Sell Aralığı:", "sell_delay", 60, 3600, 600),
        ]):
            tk.Label(dr, text=lbl, bg=BG, fg=SUBTEXT, font=("Consolas", 9)).grid(row=0, column=col*2, padx=6, sticky="w")
            var = tk.IntVar(value=ddef)
            setattr(self, attr, var)
            sc = tk.Scale(dr, variable=var, from_=dmin, to=dmax,
                          orient="horizontal", bg=BG, fg=TEXT,
                          troughcolor=BG3, highlightthickness=0,
                          font=("Consolas", 8), length=100)
            sc.grid(row=0, column=col*2+1, padx=4)

    # ─── TAB: CHANNELS ─────────────────────────────────────────────────────
    def _tab_channels(self, nb):
        f = tk.Frame(nb, bg=BG)
        nb.add(f, text="  📡 CHANNELS  ")

        tk.Label(f, text="ÇOKLU KANAL DESTEĞİ",
                 bg=BG, fg=ACCENT, font=("Consolas", 13, "bold")).pack(pady=(14, 4))
        tk.Label(f, text="Her kanala farklı gecikme ve özellik ayarı yapabilirsin",
                 bg=BG, fg=SUBTEXT, font=("Consolas", 9)).pack(pady=(0, 8))

        # Add channel
        af = self._lf(f, "Kanal Ekle", GREEN)
        af.pack(fill="x", padx=16, pady=4)
        ar = tk.Frame(af, bg=BG)
        ar.pack(fill="x", padx=8, pady=6)
        tk.Label(ar, text="Channel ID:", bg=BG, fg=SUBTEXT, font=("Consolas", 10)).pack(side="left", padx=4)
        self.new_ch_id = self._entry(ar, width=22)
        self.new_ch_id.pack(side="left", padx=4)
        tk.Label(ar, text="Min Delay:", bg=BG, fg=SUBTEXT, font=("Consolas", 10)).pack(side="left", padx=10)
        self.new_ch_min = self._entry(ar, width=6, default="3")
        self.new_ch_min.pack(side="left", padx=4)
        tk.Label(ar, text="Max Delay:", bg=BG, fg=SUBTEXT, font=("Consolas", 10)).pack(side="left", padx=10)
        self.new_ch_max = self._entry(ar, width=6, default="7")
        self.new_ch_max.pack(side="left", padx=4)
        self._btn(ar, "➕ Ekle", self._add_channel, color=GREEN, width=10).pack(side="left", padx=10)
        self._btn(ar, "Kaldır", self._remove_channel, color=RED, width=10).pack(side="left", padx=4)

        # Channel list
        lf2 = self._lf(f, "Aktif Kanallar", SUBTEXT)
        lf2.pack(fill="both", expand=True, padx=16, pady=4)
        cols = ("ID", "Min Delay", "Max Delay", "Durum", "Hunt", "Battle", "Daily")
        self.ch_tree = ttk.Treeview(lf2, columns=cols, show="headings", height=10)
        for c in cols:
            self.ch_tree.heading(c, text=c)
            self.ch_tree.column(c, width=110)
        style = ttk.Style()
        style.configure("Treeview", background=BG3, foreground=TEXT,
                        fieldbackground=BG3, font=("Consolas", 9))
        style.configure("Treeview.Heading", background=BG2, foreground=ACCENT,
                        font=("Consolas", 9, "bold"))
        sb = ttk.Scrollbar(lf2, orient="vertical", command=self.ch_tree.yview)
        self.ch_tree.configure(yscrollcommand=sb.set)
        self.ch_tree.pack(side="left", fill="both", expand=True, padx=4, pady=4)
        sb.pack(side="right", fill="y")

    def _add_channel(self):
        cid = self.new_ch_id.get().strip()
        if not cid:
            return
        try:
            dmin = float(self.new_ch_min.get())
            dmax = float(self.new_ch_max.get())
        except ValueError:
            dmin, dmax = 3.0, 7.0
        self.ch_cfg.add(cid, dmin, dmax)
        self.ch_tree.insert("", "end", values=(cid, dmin, dmax, "✅ Aktif", 0, 0, 0))
        self.new_ch_id.delete(0, "end")
        self.logger.log("CHANNEL", f"Kanal eklendi: {cid} ({dmin}-{dmax}s)")

    def _remove_channel(self):
        sel = self.ch_tree.selection()
        if not sel:
            return
        for item in sel:
            cid = self.ch_tree.item(item, "values")[0]
            self.ch_cfg.remove(cid)
            self.ch_tree.delete(item)
            self.logger.log("CHANNEL", f"Kanal kaldırıldı: {cid}")


    # ─── TAB: STATS ────────────────────────────────────────────────────────
    def _tab_stats(self, nb):
        f = tk.Frame(nb, bg=BG)
        nb.add(f, text="  📊 STATS  ")

        tk.Label(f, text="CANLI İSTATİSTİKLER", bg=BG, fg=GREEN,
                 font=("Consolas", 14, "bold")).pack(pady=(14, 4))

        grid = tk.Frame(f, bg=BG)
        grid.pack(fill="x", padx=20)

        stat_defs = [
            ("🏹 Hunt Sayısı",    "s_hunt",    GREEN),
            ("⚔️ Battle Sayısı",  "s_battle",  ACCENT),
            ("🙏 Pray Sayısı",    "s_pray",    BLUE),
            ("📅 Daily Sayısı",   "s_daily",   YELLOW),
            ("💰 Sell Sayısı",    "s_sell",    ORANGE),
            ("🎰 Slot Sayısı",    "s_slot",    PURPLE),
            ("🪙 CoinFlip Kazanç","s_cf_win",  GREEN),
            ("🪙 CoinFlip Kaybı", "s_cf_loss", RED),
            ("🍪 Cookie Sayısı",  "s_cookie",  PINK),
            ("🤖 HuntBot Sayısı", "s_huntbot", BLUE),
            ("💎 Gem Kullanımı",  "s_gems",    PURPLE),
            ("📦 Lootbox Sayısı", "s_lootbox", YELLOW),
            ("⚠️ Captcha Sayısı", "s_captcha", RED),
            ("🚨 Hata Sayısı",    "s_errors",  RED),
            ("⏱ Süre",           "s_uptime",  SUBTEXT),
            ("💸 Tahmini Kazanç", "s_earnings",GREEN),
        ]

        self._stat_vars = {}
        for i, (label, key, color) in enumerate(stat_defs):
            row, col = divmod(i, 4)
            card = tk.Frame(grid, bg=BG3, relief="flat", bd=0)
            card.grid(row=row, column=col, padx=8, pady=6, sticky="nsew")
            tk.Label(card, text=label, bg=BG3, fg=SUBTEXT,
                     font=("Consolas", 9)).pack(anchor="w", padx=10, pady=(6, 0))
            var = tk.StringVar(value="0")
            self._stat_vars[key] = var
            tk.Label(card, textvariable=var, bg=BG3, fg=color,
                     font=("Consolas", 20, "bold")).pack(anchor="w", padx=10, pady=(0, 8))

        for c in range(4):
            grid.columnconfigure(c, weight=1)

        br = tk.Frame(f, bg=BG)
        br.pack(pady=10)
        self._btn(br, "🔄 Sıfırla", self._reset_stats, color="#333", width=14).pack(side="left", padx=6)
        self._btn(br, "💾 Export CSV", self._export_stats, color=ACCENT, width=14).pack(side="left", padx=6)

        # Start update loop
        self._update_stats_loop()

    def _update_stats_loop(self):
        if not hasattr(self, "_stat_vars"):
            self.after(2000, self._update_stats_loop)
            return
        mapping = {
            "s_hunt":    STATS["hunt_count"],
            "s_battle":  STATS["battle_count"],
            "s_pray":    STATS["pray_count"],
            "s_daily":   STATS["daily_count"],
            "s_sell":    STATS["sell_count"],
            "s_slot":    STATS["slot_count"],
            "s_cf_win":  STATS["cf_wins"],
            "s_cf_loss": STATS["cf_losses"],
            "s_cookie":  STATS["cookie_count"],
            "s_huntbot": STATS["huntbot_count"],
            "s_gems":    STATS["gem_count"],
            "s_lootbox": STATS["lootbox_count"],
            "s_captcha": STATS["captcha_count"],
            "s_errors":  STATS["error_count"],
        }
        elapsed = int((datetime.now() - SESSION_START).total_seconds())
        h2, m2, s2 = elapsed // 3600, (elapsed % 3600) // 60, elapsed % 60
        mapping["s_uptime"] = f"{h2:02d}:{m2:02d}:{s2:02d}"
        mapping["s_earnings"] = f"~{STATS['hunt_count'] * 350 + STATS['daily_count'] * 1000} OwO$"
        for k, v in mapping.items():
            if k in self._stat_vars:
                self._stat_vars[k].set(str(v))
        self.after(1500, self._update_stats_loop)

    def _reset_stats(self):
        STATS.clear()
        self.logger.log("STATS", "İstatistikler sıfırlandı")

    def _export_stats(self):
        try:
            import csv
            fn = f"stats_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            with open(fn, "w", newline="", encoding="utf-8") as csvf:
                w = csv.writer(csvf)
                w.writerow(["Stat", "Value"])
                for k, v in STATS.items():
                    w.writerow([k, v])
            self.logger.log("EXPORT", f"Stats CSV kaydedildi: {fn}", "INFO")
        except Exception as e:
            self.logger.log("EXPORT", f"Hata: {e}", "ERROR")

    # ─── TAB: LOG ──────────────────────────────────────────────────────────
    def _tab_log(self, nb):
        f = tk.Frame(nb, bg=BG)
        nb.add(f, text="  📋 LOG  ")

        hdr = tk.Frame(f, bg=BG)
        hdr.pack(fill="x", padx=10, pady=6)
        tk.Label(hdr, text="CANLI LOG AKIŞI", bg=BG, fg=GREEN,
                 font=("Consolas", 12, "bold")).pack(side="left")
        self._btn(hdr, "Temizle", self._clear_log, color="#222", width=10).pack(side="right", padx=4)
        self._btn(hdr, "💾 Dosyaya Yaz", self._save_log, color="#333", width=14).pack(side="right", padx=4)

        # Filter
        flt = tk.Frame(f, bg=BG3)
        flt.pack(fill="x", padx=10, pady=2)
        tk.Label(flt, text="Filtre:", bg=BG3, fg=SUBTEXT, font=("Consolas", 9)).pack(side="left", padx=6)
        self.log_filter = self._entry(flt, width=20)
        self.log_filter.pack(side="left", padx=4)
        self.log_filter.bind("<Return>", self._apply_log_filter)
        self._btn(flt, "Filtrele", self._apply_log_filter, color=ACCENT, width=10).pack(side="left", padx=4)
        self.log_level_var = ttk.Combobox(flt, values=["ALL", "INFO", "WARN", "ERROR", "STAT"],
                                          state="readonly", width=8, font=("Consolas", 9))
        self.log_level_var.current(0)
        self.log_level_var.pack(side="left", padx=8)

        self.log_widget = scrolledtext.ScrolledText(
            f, bg=BG3, fg=GREEN, font=("Consolas", 9),
            state="disabled", relief="flat", bd=0, wrap="word"
        )
        self.log_widget.pack(fill="both", expand=True, padx=10, pady=4)
        # Tag colors
        self.log_widget.tag_config("ts",   foreground=SUBTEXT)
        self.log_widget.tag_config("INFO",  foreground=GREEN)
        self.log_widget.tag_config("WARN",  foreground=YELLOW)
        self.log_widget.tag_config("ERROR", foreground=RED)
        self.log_widget.tag_config("STAT",  foreground=BLUE)
        self.log_widget.tag_config("cat",   foreground=ACCENT)

    def _clear_log(self):
        self.log_widget.configure(state="normal")
        self.log_widget.delete("1.0", "end")
        self.log_widget.configure(state="disabled")

    def _apply_log_filter(self, event=None):
        pass  # Full implementation can filter log_widget content

    def _save_log(self):
        try:
            fn = f"log_session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            content = self.log_widget.get("1.0", "end")
            with open(fn, "w", encoding="utf-8") as fh:
                fh.write(content)
            self.logger.log("LOG", f"Log kaydedildi: {fn}")
        except Exception as e:
            self.logger.log("LOG", f"Hata: {e}", "ERROR")

    # ─── TAB: CAPTCHA ──────────────────────────────────────────────────────
    def _tab_captcha(self, nb):
        f = tk.Frame(nb, bg=BG)
        nb.add(f, text="  🔐 CAPTCHA  ")

        tk.Label(f, text="CAPTCHA YÖNETIMI", bg=BG, fg=RED,
                 font=("Consolas", 14, "bold")).pack(pady=(14, 4))
        tk.Label(f, text="OWO Bot captcha gönderdiğinde otomatik duraklatır ve seni bildirir.",
                 bg=BG, fg=SUBTEXT, font=("Consolas", 9)).pack(pady=(0, 10))

        # Status
        sf = self._lf(f, "Captcha Durumu", RED)
        sf.pack(fill="x", padx=16, pady=4)
        sr = tk.Frame(sf, bg=BG)
        sr.pack(fill="x", padx=8, pady=8)
        self.captcha_status_var = tk.StringVar(value="✅  Captcha yok — Bot çalışıyor")
        tk.Label(sr, textvariable=self.captcha_status_var, bg=BG, fg=GREEN,
                 font=("Consolas", 12, "bold")).pack(side="left", padx=6)
        self._btn(sr, "Manuel Devam Et", self._resume_after_captcha, color=GREEN, width=18).pack(side="right", padx=8)

        # Settings
        stf = self._lf(f, "Captcha Algılama Ayarları", YELLOW)
        stf.pack(fill="x", padx=16, pady=4)
        opts = [
            ("Captcha algılandığında botu duraklat", "captcha_pause", True),
            ("Captcha webhook bildirimi gönder", "captcha_webhook", True),
            ("Otomatik tüm kanallarda duraklat", "captcha_pause_all", True),
            ("Captcha log'a kaydet", "captcha_log", True),
        ]
        self.captcha_opts = {}
        for text, key, default in opts:
            var = tk.BooleanVar(value=default)
            self.captcha_opts[key] = var
            tk.Checkbutton(stf, text=text, variable=var,
                           bg=BG, fg=TEXT, selectcolor=BG3,
                           activebackground=BG, font=("Consolas", 10)).pack(anchor="w", padx=12, pady=3)

        # Keyword list
        kf = self._lf(f, "Captcha Anahtar Kelimeleri", SUBTEXT)
        kf.pack(fill="x", padx=16, pady=4)
        kw_frame = tk.Frame(kf, bg=BG)
        kw_frame.pack(fill="x", padx=8, pady=6)
        self.kw_listbox = tk.Listbox(kw_frame, bg=BG3, fg=YELLOW, font=("Consolas", 9), height=5, selectmode="single")
        for kw in CAPTCHA_KEYWORDS:
            self.kw_listbox.insert("end", kw)
        self.kw_listbox.pack(side="left", fill="x", expand=True, padx=4)
        kw_btns = tk.Frame(kw_frame, bg=BG)
        kw_btns.pack(side="right", padx=6)
        self.new_kw = self._entry(kw_btns, width=16)
        self.new_kw.pack(pady=4)
        self._btn(kw_btns, "➕ Ekle", self._add_kw, color=GREEN, width=12).pack(pady=2)
        self._btn(kw_btns, "🗑 Sil", self._remove_kw, color=RED, width=12).pack(pady=2)

        # Captcha log
        tk.Label(f, text="Captcha Geçmişi:", bg=BG, fg=SUBTEXT, font=("Consolas", 9)).pack(anchor="w", padx=16, pady=(8, 2))
        self.captcha_log = self._logbox(f, height=6, fg=RED)
        self.captcha_log.pack(fill="both", expand=True, padx=16, pady=(0, 12))

    def _resume_after_captcha(self):
        self._pause_all = False
        self.captcha_status_var.set("✅  Manuel devam — Bot yeniden başladı")
        self.logger.log("CAPTCHA", "Manuel devam — bot yeniden başlatıldı", "WARN")
        self._log_write(self.captcha_log, "[RESUMED] Kullanıcı manuel devam etti")

    def _add_kw(self):
        kw = self.new_kw.get().strip()
        if kw:
            CAPTCHA_KEYWORDS.append(kw)
            self.kw_listbox.insert("end", kw)
            self.new_kw.delete(0, "end")

    def _remove_kw(self):
        sel = self.kw_listbox.curselection()
        if sel:
            kw = self.kw_listbox.get(sel[0])
            if kw in CAPTCHA_KEYWORDS:
                CAPTCHA_KEYWORDS.remove(kw)
            self.kw_listbox.delete(sel[0])

    # ─── TAB: ABOUT ────────────────────────────────────────────────────────
    def _tab_about(self, nb):
        f = tk.Frame(nb, bg=BG)
        nb.add(f, text="  ℹ ABOUT  ")
        tk.Label(f, text="\n\n☁  OWO AUTO TOOL  ☁", bg=BG, fg=ACCENT,
                 font=("Consolas", 22, "bold")).pack()
        tk.Label(f, text="v2.0", bg=BG, fg=SUBTEXT, font=("Consolas", 14)).pack()
        tk.Label(f, text="\nMade By Haribo\n", bg=BG, fg=TEXT, font=("Consolas", 12, "bold")).pack()
        feats = [
            "✅  Auto Hunt, Battle, Pray, Daily, Sell",
            "✅  Auto Slot & CoinFlip (ayarlanabilir bahis)",
            "✅  Auto Cookie, HuntBot, Gems, Lootbox",
            "✅  Multi-Channel Support (özel gecikme)",
            "✅  Discord Webhook Notifier",
            "✅  Captcha Algılama & Duraklatma",
            "✅  Detaylı Logging (dosyaya yazar)",
            "✅  Anti-Detection (random delay)",
            "✅  Canlı Stats Dashboard",
            "✅  Config Kaydet / Yükle",
        ]
        for feat in feats:
            tk.Label(f, text=feat, bg=BG, fg=TEXT, font=("Consolas", 10)).pack(pady=1)
        tk.Label(f, text="\n⚠  UYARI: Discord ToS ihlali — Kendi riskinle kullan.",
                 bg=BG, fg=RED, font=("Consolas", 9)).pack()


    # ════════════════════════════════════════════════
    # CONNECT & BOT CONTROL
    # ════════════════════════════════════════════════
    def _toggle_token_show(self):
        show = "" if self.show_token_var.get() else "•"
        self.token_entry.configure(show=show)

    def _connect(self):
        token = self.token_entry.get().strip()
        if not token:
            self.conn_status.set("❌  Token boş!")
            return
        self.set_status("🔄  Bağlanıyor...", YELLOW)
        def w():
            self.client = DiscordClient(token)
            me = self.client.get_me()
            if me:
                uname = f"{me.get('username','?')}#{me.get('discriminator','0')}"
                uid   = me.get('id','?')
                self.conn_status.set(f"✅  Bağlandı: {uname}  (ID: {uid})")
                self.set_status(f"✅  {uname} olarak bağlandı", GREEN)
                self.logger.log("AUTH", f"Token doğrulandı: {uname} ({uid})", "INFO")
            else:
                self.conn_status.set("❌  Token geçersiz veya ban yendi!")
                self.set_status("❌  Bağlantı başarısız", RED)
                self.client = None
        threading.Thread(target=w, daemon=True).start()

    def _toggle_webhook(self):
        self.webhook.enabled = self.wh_enable.get()

    def _test_webhook(self):
        url = self.webhook_entry.get().strip()
        if not url:
            return
        self.webhook.url = url
        self.webhook.enabled = True
        self.webhook.send("🔔 Test Bildirimi", "OWO Tool webhook bağlantısı başarılı! ✅", 0x43b581)
        self.logger.log("WEBHOOK", "Test bildirimi gönderildi")

    def _start_bot(self):
        if not self.client:
            messagebox.showerror("Hata", "Önce token ile bağlan!")
            return
        if not self.ch_cfg.channels:
            messagebox.showerror("Hata", "En az bir kanal ekle!")
            return
        if self._running:
            messagebox.showinfo("Bilgi", "Bot zaten çalışıyor!")
            return

        self._running = True
        self._pause_all = False
        self.webhook.url    = self.webhook_entry.get().strip()
        self.webhook.enabled = self.wh_enable.get()
        self.set_status("▶  Bot çalışıyor...", GREEN)
        self.logger.log("BOT", "Bot başlatıldı", "INFO")

        for ch in self.ch_cfg.channels:
            t = threading.Thread(
                target=self._channel_worker,
                args=(ch,),
                daemon=True,
            )
            t.start()
            self._threads.append(t)

    def _stop_bot(self):
        self._running = False
        self._threads.clear()
        self.set_status("⏹  Bot durduruldu", RED)
        self.logger.log("BOT", "Bot durduruldu", "WARN")

    def _pause_bot(self):
        self._pause_all = not self._pause_all
        if self._pause_all:
            self.set_status("⏸  Bot duraklatıldı", YELLOW)
            self.logger.log("BOT", "Bot duraklatıldı", "WARN")
        else:
            self.set_status("▶  Bot devam ediyor", GREEN)
            self.logger.log("BOT", "Bot devam ediyor", "INFO")

    # ════════════════════════════════════════════════
    # CHANNEL WORKER (ana döngü)
    # ════════════════════════════════════════════════
    def _channel_worker(self, ch: dict):
        channel_id  = ch["id"]
        hunt_cycle  = 0
        battle_cycle = 0
        pray_cycle  = 0
        sell_cycle  = 0
        daily_done  = False
        huntbot_cycle = 0

        self.logger.log("WORKER", f"[{channel_id}] Worker başladı")

        while self._running:
            if self._pause_all or ch.get("captcha_paused"):
                time.sleep(1)
                continue

            try:
                # ─── DAILY (günlük bir kez) ──────────────────
                if self.feat_daily.get() and not daily_done:
                    self._do_daily(channel_id)
                    daily_done = True
                    STATS["daily_count"] += 1

                # ─── HUNT ────────────────────────────────────
                if self.feat_hunt.get():
                    self._do_hunt(channel_id)
                    hunt_cycle += 1
                    STATS["hunt_count"] += 1
                    delay = self._random_delay(ch, self.hunt_delay.get())
                    time.sleep(delay)
                    if not self._running:
                        break

                # ─── BATTLE ──────────────────────────────────
                if self.feat_battle.get() and hunt_cycle % 3 == 0:
                    self._do_battle(channel_id)
                    battle_cycle += 1
                    STATS["battle_count"] += 1
                    time.sleep(self._random_delay(ch, self.battle_delay.get()))

                # ─── PRAY ────────────────────────────────────
                if self.feat_pray.get() and hunt_cycle % 5 == 0:
                    self._do_pray(channel_id)
                    pray_cycle += 1
                    STATS["pray_count"] += 1
                    time.sleep(self._random_delay(ch, self.pray_delay.get()))

                # ─── COOKIE ──────────────────────────────────
                if self.feat_cookie.get() and hunt_cycle % 7 == 0:
                    self._do_cookie(channel_id)
                    STATS["cookie_count"] += 1
                    time.sleep(self._random_delay(ch, 5))

                # ─── SELL ────────────────────────────────────
                if self.feat_sell.get() and hunt_cycle % 20 == 0:
                    self._do_sell(channel_id)
                    sell_cycle += 1
                    STATS["sell_count"] += 1
                    time.sleep(self._random_delay(ch, self.sell_delay.get()))

                # ─── HUNTBOT ─────────────────────────────────
                if self.feat_huntbot.get() and hunt_cycle % 30 == 0:
                    self._do_huntbot(channel_id)
                    huntbot_cycle += 1
                    STATS["huntbot_count"] += 1
                    time.sleep(self._random_delay(ch, 8))

                # ─── SLOT ────────────────────────────────────
                if self.feat_slot.get() and hunt_cycle % 15 == 0:
                    self._do_slot(channel_id)
                    STATS["slot_count"] += 1
                    time.sleep(self._random_delay(ch, 4))

                # ─── COINFLIP ─────────────────────────────────
                if self.feat_coinflip.get() and hunt_cycle % 12 == 0:
                    self._do_coinflip(channel_id)
                    time.sleep(self._random_delay(ch, 3))

                # ─── GEMS ─────────────────────────────────────
                if self.feat_gems.get() and hunt_cycle % 50 == 0:
                    self._do_gems(channel_id)
                    STATS["gem_count"] += 1
                    time.sleep(self._random_delay(ch, 3))

                # ─── LOOTBOX ─────────────────────────────────
                if self.feat_lootbox.get() and hunt_cycle % 40 == 0:
                    self._do_lootbox(channel_id)
                    STATS["lootbox_count"] += 1
                    time.sleep(self._random_delay(ch, 3))

                # ─── Captcha kontrolü ─────────────────────────
                if hunt_cycle % 5 == 0:
                    self._check_captcha(channel_id, ch)

                # ─── Daily reset check ────────────────────────
                if hunt_cycle % 100 == 0:
                    daily_done = False  # Gece yarısında resetle (basit yaklaşım)

            except Exception as e:
                STATS["error_count"] += 1
                self.logger.log("WORKER", f"[{channel_id}] Hata: {e}", "ERROR")
                time.sleep(5)

    # ════════════════════════════════════════════════
    # OWO KOMUTLARI
    # ════════════════════════════════════════════════
    def _prefix(self) -> str:
        return self.prefix_entry.get().strip() if hasattr(self, "prefix_entry") else "owo "

    def _random_delay(self, ch: dict, base: float) -> float:
        if self.feat_anti_detect.get():
            jitter = random.uniform(-0.8, 1.5)
            return max(1.0, base + jitter)
        return base

    def _send(self, channel_id: str, cmd: str):
        if not self.client:
            return
        p = self._prefix()
        msg = p + cmd
        result = self.client.send_message(channel_id, msg)
        if "error" in result:
            self.logger.log("SEND", f"[{channel_id}] Hata: {result}", "ERROR")
            STATS["error_count"] += 1
        else:
            self.logger.log("CMD", f"[{channel_id}] → {msg}")
        return result

    def _do_hunt(self, channel_id: str):
        self._send(channel_id, "hunt")

    def _do_battle(self, channel_id: str):
        target = self.battle_target.get().strip()
        cmd = f"battle {target}" if target else "battle"
        self._send(channel_id, cmd)

    def _do_pray(self, channel_id: str):
        self._send(channel_id, "pray")

    def _do_daily(self, channel_id: str):
        result = self._send(channel_id, "daily")
        self.logger.log("DAILY", f"[{channel_id}] Daily toplandı", "INFO")
        self.webhook.notify_daily("?", channel_id)
        time.sleep(3)

    def _do_sell(self, channel_id: str):
        target = self.sell_target.get().strip() if hasattr(self, "sell_target") else "all"
        self._send(channel_id, f"sell {target}")
        self.logger.log("SELL", f"[{channel_id}] Sell: {target}")
        time.sleep(2)

    def _do_slot(self, channel_id: str):
        bet = self.slot_bet.get().strip() if hasattr(self, "slot_bet") else "100"
        self._send(channel_id, f"slots {bet}")

    def _do_coinflip(self, channel_id: str):
        bet  = self.cf_bet.get().strip()  if hasattr(self, "cf_bet")  else "100"
        side = self.cf_side.get()          if hasattr(self, "cf_side") else "heads"
        result = self._send(channel_id, f"coinflip {side} {bet}")
        time.sleep(2)
        # Kazanç/kayıp tespiti için mesajları kontrol et
        msgs = self.client.get_messages(channel_id, 3) if self.client else []
        for m in msgs:
            content = m.get("content", "").lower()
            if "won" in content or "kazandın" in content:
                STATS["cf_wins"] += 1
            elif "lost" in content or "kaybettın" in content:
                STATS["cf_losses"] += 1

    def _do_cookie(self, channel_id: str):
        target = self.cookie_target.get().strip() if hasattr(self, "cookie_target") else ""
        if target:
            self._send(channel_id, f"cookie {target}")
        else:
            self._send(channel_id, "cookie")

    def _do_huntbot(self, channel_id: str):
        self._send(channel_id, "huntbot")
        self.logger.log("HUNTBOT", f"[{channel_id}] HuntBot komutu gönderildi")
        self.webhook.notify_huntbot("owo huntbot komutu gönderildi", channel_id)
        time.sleep(3)

    def _do_gems(self, channel_id: str):
        gem = self.gem_type.get() if hasattr(self, "gem_type") else "all"
        self._send(channel_id, f"gem use {gem}")

    def _do_lootbox(self, channel_id: str):
        lb = self.lb_type.get() if hasattr(self, "lb_type") else "all"
        self._send(channel_id, f"lootbox open {lb}")

    # ════════════════════════════════════════════════
    # CAPTCHA CHECK
    # ════════════════════════════════════════════════
    def _check_captcha(self, channel_id: str, ch: dict):
        if not self.client:
            return
        msgs = self.client.get_messages(channel_id, 5)
        for m in msgs:
            author_id  = m.get("author", {}).get("id", "")
            content    = m.get("content", "")
            if author_id == OWO_BOT_ID and detect_captcha(content):
                self._handle_captcha(channel_id, ch, content)
                return

    def _handle_captcha(self, channel_id: str, ch: dict, content: str):
        STATS["captcha_count"] += 1
        self.logger.log("CAPTCHA", f"[{channel_id}] CAPTCHA TESPİT EDİLDİ!", "ERROR")
        ch["captcha_paused"] = True

        if hasattr(self, "captcha_status_var"):
            self.captcha_status_var.set(f"⚠️  CAPTCHA! [{channel_id}] — Manuel çöz ve 'Devam Et'e bas")

        if hasattr(self, "captcha_log"):
            self._log_write(self.captcha_log,
                            f"[CAPTCHA] [{channel_id}]: {content[:80]}...")

        if self.feat_captcha_wh.get():
            self.webhook.notify_captcha(channel_id)

        if self.captcha_opts.get("captcha_pause_all", tk.BooleanVar(value=True)).get():
            self._pause_all = True
            self.set_status("⚠️  CAPTCHA! Bot duraklatıldı — CAPTCHA sekmesine git!", RED)

    # ════════════════════════════════════════════════
    # CONFIG SAVE / LOAD
    # ════════════════════════════════════════════════
    def _save_config(self):
        cfg = {
            "token": self.token_entry.get(),
            "webhook": self.webhook_entry.get(),
            "prefix": self.prefix_entry.get(),
            "battle_target": self.battle_target.get(),
            "cookie_target": self.cookie_target.get(),
            "sell_target": self.sell_target.get(),
            "slot_bet": self.slot_bet.get(),
            "cf_bet": self.cf_bet.get(),
            "cf_side": self.cf_side.get(),
            "gem_type": self.gem_type.get(),
            "lb_type": self.lb_type.get(),
            "features": {
                "hunt":        self.feat_hunt.get(),
                "battle":      self.feat_battle.get(),
                "pray":        self.feat_pray.get(),
                "daily":       self.feat_daily.get(),
                "sell":        self.feat_sell.get(),
                "slot":        self.feat_slot.get(),
                "coinflip":    self.feat_coinflip.get(),
                "cookie":      self.feat_cookie.get(),
                "huntbot":     self.feat_huntbot.get(),
                "gems":        self.feat_gems.get(),
                "lootbox":     self.feat_lootbox.get(),
                "anti_detect": self.feat_anti_detect.get(),
            },
            "channels": self.ch_cfg.channels,
            "hunt_delay":   self.hunt_delay.get(),
            "battle_delay": self.battle_delay.get(),
            "pray_delay":   self.pray_delay.get(),
            "sell_delay":   self.sell_delay.get(),
        }
        fn = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON", "*.json")],
            initialfile="owo_config.json",
        )
        if fn:
            with open(fn, "w", encoding="utf-8") as f:
                json.dump(cfg, f, indent=2, ensure_ascii=False)
            self.logger.log("CONFIG", f"Config kaydedildi: {fn}")

    def _load_config(self):
        fn = filedialog.askopenfilename(filetypes=[("JSON", "*.json")])
        if not fn or not os.path.exists(fn):
            return
        with open(fn, encoding="utf-8") as f:
            cfg = json.load(f)

        def se(widget, value):
            widget.delete(0, "end")
            widget.insert(0, value)

        se(self.token_entry,  cfg.get("token", ""))
        se(self.webhook_entry, cfg.get("webhook", ""))
        se(self.prefix_entry, cfg.get("prefix", "owo "))
        se(self.battle_target, cfg.get("battle_target", ""))
        se(self.cookie_target, cfg.get("cookie_target", ""))
        se(self.sell_target,  cfg.get("sell_target", "all"))
        se(self.slot_bet,     cfg.get("slot_bet", "100"))
        se(self.cf_bet,       cfg.get("cf_bet", "100"))

        feats = cfg.get("features", {})
        self.feat_hunt.set(feats.get("hunt", True))
        self.feat_battle.set(feats.get("battle", True))
        self.feat_pray.set(feats.get("pray", True))
        self.feat_daily.set(feats.get("daily", True))
        self.feat_sell.set(feats.get("sell", True))
        self.feat_slot.set(feats.get("slot", False))
        self.feat_coinflip.set(feats.get("coinflip", False))
        self.feat_cookie.set(feats.get("cookie", True))
        self.feat_huntbot.set(feats.get("huntbot", True))
        self.feat_gems.set(feats.get("gems", True))
        self.feat_lootbox.set(feats.get("lootbox", True))
        self.feat_anti_detect.set(feats.get("anti_detect", True))

        self.hunt_delay.set(cfg.get("hunt_delay", 6))
        self.battle_delay.set(cfg.get("battle_delay", 20))
        self.pray_delay.set(cfg.get("pray_delay", 30))
        self.sell_delay.set(cfg.get("sell_delay", 600))

        for ch in cfg.get("channels", []):
            self.ch_cfg.add(ch["id"], ch.get("delay_min", 3), ch.get("delay_max", 7))
            self.ch_tree.insert("", "end", values=(ch["id"], ch.get("delay_min", 3), ch.get("delay_max", 7), "✅ Aktif", 0, 0, 0))

        self.logger.log("CONFIG", f"Config yüklendi: {fn}")



# ════════════════════════════════════════════════
if __name__ == "__main__":
    app = OwoTool()
    app.mainloop()
