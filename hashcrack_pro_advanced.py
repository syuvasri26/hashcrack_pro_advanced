#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════╗
║              HashCrack Pro v2.0 — ADVANCED               ║
║        Real-Time Password Hash Cracking Suite            ║
║                Red Team Internship Project               ║
╚══════════════════════════════════════════════════════════╝

Features:
  • Wordlist Attack
  • Brute Force Attack
  • Multiple Hash Cracking
  • Hash Generator
  • Live Dashboard (speed, progress, ETA)
  • Export: TXT + HTML + CSV reports
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import hashlib
import threading
import time
import os
import csv
import datetime
import itertools
import string


# ══════════════════════════════════════════════════════════
#  CONSTANTS & HELPERS
# ══════════════════════════════════════════════════════════

HASH_LENGTHS = {
    32:  "md5",
    40:  "sha1",
    56:  "sha224",
    64:  "sha256",
    96:  "sha384",
    128: "sha512",
}

COLORS = {
    "bg":        "#0b0d12",
    "panel":     "#13161f",
    "border":    "#1e2230",
    "red":       "#e63946",
    "blue":      "#457b9d",
    "teal":      "#2a9d8f",
    "yellow":    "#e9c46a",
    "text":      "#cdd6f4",
    "subtext":   "#6c7086",
    "success":   "#a6e3a1",
    "error":     "#f38ba8",
    "warn":      "#fab387",
    "highlight": "#1e2230",
}

FONTS = {
    "title":  ("Courier New", 20, "bold"),
    "head":   ("Courier New", 12, "bold"),
    "normal": ("Courier New", 10),
    "small":  ("Courier New", 9),
    "mono":   ("Courier New", 11),
}


def detect_hash_type(h):
    h = h.strip()
    return HASH_LENGTHS.get(len(h), "unknown")


def compute_hash(word, algo):
    try:
        h = hashlib.new(algo)
        h.update(word.encode("utf-8", errors="ignore"))
        return h.hexdigest()
    except Exception:
        return None


def make_label(parent, text, fg=None, font=None, bg=None, **kw):
    return tk.Label(
        parent, text=text,
        fg=fg or COLORS["text"],
        bg=bg or COLORS["bg"],
        font=font or FONTS["normal"],
        **kw
    )


def make_button(parent, text, command, bg=None, fg=None, **kw):
    return tk.Button(
        parent, text=text, command=command,
        bg=bg or COLORS["blue"],
        fg=fg or COLORS["bg"],
        font=FONTS["small"],
        relief="flat", cursor="hand2",
        activebackground=COLORS["red"],
        activeforeground=COLORS["bg"],
        padx=10, pady=5,
        **kw
    )


# ══════════════════════════════════════════════════════════
#  MAIN APPLICATION
# ══════════════════════════════════════════════════════════

class HashCrackPro(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("HashCrack Pro v2.0  |  Advanced Red Team Suite")
        self.geometry("960x780")
        self.minsize(900, 700)
        self.configure(bg=COLORS["bg"])

        # ── Shared state ──
        self.is_running     = False
        self.crack_thread   = None
        self.results        = []          # [{hash, password, algo, method, time, tries}]
        self.wordlist_path  = tk.StringVar(value="")
        self.stats          = {"tries": 0, "speed": 0, "elapsed": 0, "eta": "—"}

        self._style_ttk()
        self._build_ui()
        self._log("HashCrack Pro v2.0 ready. Select a tab and start cracking! 🔐", "info")

    # ── TTK Styling ──────────────────────────────────────

    def _style_ttk(self):
        s = ttk.Style(self)
        s.theme_use("clam")
        s.configure("TNotebook",
                    background=COLORS["bg"],
                    borderwidth=0)
        s.configure("TNotebook.Tab",
                    background=COLORS["panel"],
                    foreground=COLORS["subtext"],
                    font=FONTS["small"],
                    padding=[14, 6])
        s.map("TNotebook.Tab",
              background=[("selected", COLORS["red"])],
              foreground=[("selected", COLORS["bg"])])
        s.configure("TProgressbar",
                    troughcolor=COLORS["border"],
                    background=COLORS["red"],
                    thickness=6)
        s.configure("TCombobox",
                    fieldbackground=COLORS["panel"],
                    background=COLORS["panel"],
                    foreground=COLORS["text"],
                    selectbackground=COLORS["red"])

    # ── UI Layout ─────────────────────────────────────────

    def _build_ui(self):
        # Header
        hdr = tk.Frame(self, bg=COLORS["bg"])
        hdr.pack(fill="x", padx=20, pady=(14, 0))

        tk.Label(hdr, text="🔐 HashCrack Pro",
                 font=FONTS["title"], fg=COLORS["red"],
                 bg=COLORS["bg"]).pack(side="left")

        tk.Label(hdr, text="Advanced Red Team Password Cracking Suite  v2.0",
                 font=FONTS["small"], fg=COLORS["subtext"],
                 bg=COLORS["bg"]).pack(side="left", padx=16, pady=6)

        tk.Frame(self, bg=COLORS["red"], height=2).pack(fill="x", padx=20, pady=8)

        # Dashboard bar
        self._build_dashboard()

        # Tabs
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=20, pady=6)

        self.tab_wordlist  = tk.Frame(self.notebook, bg=COLORS["bg"])
        self.tab_brute     = tk.Frame(self.notebook, bg=COLORS["bg"])
        self.tab_multi     = tk.Frame(self.notebook, bg=COLORS["bg"])
        self.tab_generator = tk.Frame(self.notebook, bg=COLORS["bg"])

        self.notebook.add(self.tab_wordlist,  text="  📖 Wordlist Attack  ")
        self.notebook.add(self.tab_brute,     text="  💥 Brute Force  ")
        self.notebook.add(self.tab_multi,     text="  📋 Multi-Hash  ")
        self.notebook.add(self.tab_generator, text="  ⚙️  Hash Generator  ")

        self._build_wordlist_tab()
        self._build_brute_tab()
        self._build_multi_tab()
        self._build_generator_tab()

        # Log + Export
        self._build_log()

    # ── Dashboard ─────────────────────────────────────────

    def _build_dashboard(self):
        dash = tk.Frame(self, bg=COLORS["panel"], pady=8)
        dash.pack(fill="x", padx=20, pady=4)

        cards = [
            ("⚡ SPEED",   "speed_lbl",   "0 w/s"),
            ("🔢 TRIED",   "tries_lbl",   "0"),
            ("⏱ ELAPSED", "elapsed_lbl", "0s"),
            ("🎯 ETA",     "eta_lbl",     "—"),
            ("✅ CRACKED", "cracked_lbl", "0"),
        ]

        for title, attr, default in cards:
            card = tk.Frame(dash, bg=COLORS["border"], padx=16, pady=6)
            card.pack(side="left", padx=8, pady=4)
            tk.Label(card, text=title, font=FONTS["small"],
                     fg=COLORS["subtext"], bg=COLORS["border"]).pack()
            lbl = tk.Label(card, text=default, font=FONTS["head"],
                           fg=COLORS["red"], bg=COLORS["border"])
            lbl.pack()
            setattr(self, attr, lbl)

        # Progress bar
        pb_frame = tk.Frame(dash, bg=COLORS["panel"])
        pb_frame.pack(side="left", fill="x", expand=True, padx=16)
        tk.Label(pb_frame, text="Progress", font=FONTS["small"],
                 fg=COLORS["subtext"], bg=COLORS["panel"]).pack(anchor="w")
        self.progress = ttk.Progressbar(pb_frame, mode="indeterminate", length=300)
        self.progress.pack(fill="x", pady=4)
        self.status_lbl = tk.Label(pb_frame, text="Idle",
                                   font=FONTS["small"], fg=COLORS["teal"],
                                   bg=COLORS["panel"])
        self.status_lbl.pack(anchor="w")

    # ── Tab 1: Wordlist ───────────────────────────────────

    def _build_wordlist_tab(self):
        p = self.tab_wordlist

        # Hash input
        row1 = self._panel(p, "🎯  Target Hash")
        self.wl_hash = self._entry(row1, width=60)
        self.wl_hash.grid(row=0, column=0, padx=8, pady=8, sticky="ew")
        make_button(row1, "🔍 Detect", self._wl_detect).grid(row=0, column=1, padx=4)
        self.wl_detect_lbl = tk.Label(row1, text="", font=FONTS["small"],
                                      fg=COLORS["teal"], bg=COLORS["panel"])
        self.wl_detect_lbl.grid(row=0, column=2, padx=8)

        tk.Label(row1, text="Algorithm:", font=FONTS["small"],
                 fg=COLORS["subtext"], bg=COLORS["panel"]).grid(row=1, column=0, sticky="w", padx=8)
        self.wl_algo = ttk.Combobox(row1, values=["Auto Detect","md5","sha1","sha224","sha256","sha384","sha512"],
                                    state="readonly", width=18)
        self.wl_algo.set("Auto Detect")
        self.wl_algo.grid(row=1, column=0, sticky="e", padx=8, pady=6)
        row1.columnconfigure(0, weight=1)

        # Wordlist
        row2 = self._panel(p, "📂  Wordlist File")
        self.wl_path_lbl = tk.Label(row2, textvariable=self.wordlist_path,
                                    font=FONTS["small"], fg=COLORS["text"],
                                    bg=COLORS["panel"], anchor="w", width=55)
        self.wl_path_lbl.grid(row=0, column=0, padx=8, pady=8, sticky="ew")
        make_button(row2, "📂 Browse", self._browse_wordlist).grid(row=0, column=1, padx=4)
        make_button(row2, "⚡ rockyou.txt", self._use_rockyou,
                    bg=COLORS["teal"]).grid(row=0, column=2, padx=4)
        row2.columnconfigure(0, weight=1)

        # Buttons
        self._ctrl_buttons(p, self._start_wordlist, self._stop)

    # ── Tab 2: Brute Force ────────────────────────────────

    def _build_brute_tab(self):
        p = self.tab_brute

        row1 = self._panel(p, "🎯  Target Hash")
        self.bf_hash = self._entry(row1, width=60)
        self.bf_hash.grid(row=0, column=0, padx=8, pady=8, sticky="ew")
        make_button(row1, "🔍 Detect", self._bf_detect).grid(row=0, column=1, padx=4)
        self.bf_detect_lbl = tk.Label(row1, text="", font=FONTS["small"],
                                      fg=COLORS["teal"], bg=COLORS["panel"])
        self.bf_detect_lbl.grid(row=0, column=2, padx=8)

        tk.Label(row1, text="Algorithm:", font=FONTS["small"],
                 fg=COLORS["subtext"], bg=COLORS["panel"]).grid(row=1, column=0, sticky="w", padx=8)
        self.bf_algo = ttk.Combobox(row1, values=["Auto Detect","md5","sha1","sha224","sha256","sha384","sha512"],
                                    state="readonly", width=18)
        self.bf_algo.set("Auto Detect")
        self.bf_algo.grid(row=1, column=0, sticky="e", padx=8, pady=6)
        row1.columnconfigure(0, weight=1)

        # Brute force config
        row2 = self._panel(p, "⚙️  Brute Force Settings")
        configs = [
            ("Min Length:", "bf_min", "1", 6),
            ("Max Length:", "bf_max", "4", 6),
        ]
        for i, (lbl, attr, default, w) in enumerate(configs):
            tk.Label(row2, text=lbl, font=FONTS["small"],
                     fg=COLORS["subtext"], bg=COLORS["panel"]).grid(row=0, column=i*2, padx=8, pady=8, sticky="w")
            e = self._entry(row2, width=w)
            e.insert(0, default)
            e.grid(row=0, column=i*2+1, padx=4)
            setattr(self, attr, e)

        tk.Label(row2, text="Charset:", font=FONTS["small"],
                 fg=COLORS["subtext"], bg=COLORS["panel"]).grid(row=0, column=4, padx=8, sticky="w")
        self.bf_charset = ttk.Combobox(row2, width=22, state="readonly",
            values=["Lowercase (a-z)", "Uppercase (A-Z)", "Digits (0-9)",
                    "Lower + Digits", "Lower + Upper + Digits", "All Printable"])
        self.bf_charset.set("Lower + Digits")
        self.bf_charset.grid(row=0, column=5, padx=8)

        self._ctrl_buttons(p, self._start_brute, self._stop)

    # ── Tab 3: Multi-Hash ─────────────────────────────────

    def _build_multi_tab(self):
        p = self.tab_multi

        row1 = self._panel(p, "📋  Multiple Hashes  (one per line)")
        self.multi_text = tk.Text(row1, height=6, font=FONTS["mono"],
                                  bg=COLORS["border"], fg=COLORS["text"],
                                  insertbackground=COLORS["red"],
                                  relief="flat", bd=4)
        self.multi_text.pack(fill="both", expand=True, padx=8, pady=8)
        self.multi_text.insert("end", "# Paste hashes here, one per line\n")

        row2 = self._panel(p, "📂  Wordlist")
        tk.Label(row2, textvariable=self.wordlist_path,
                 font=FONTS["small"], fg=COLORS["text"],
                 bg=COLORS["panel"], anchor="w").pack(side="left", padx=8, fill="x", expand=True)
        make_button(row2, "📂 Browse", self._browse_wordlist).pack(side="left", padx=4)
        make_button(row2, "⚡ rockyou.txt", self._use_rockyou,
                    bg=COLORS["teal"]).pack(side="left", padx=4)

        self._ctrl_buttons(p, self._start_multi, self._stop)

    # ── Tab 4: Hash Generator ─────────────────────────────

    def _build_generator_tab(self):
        p = self.tab_generator

        row1 = self._panel(p, "⚙️  Hash Generator")

        tk.Label(row1, text="Plain Text:", font=FONTS["small"],
                 fg=COLORS["subtext"], bg=COLORS["panel"]).grid(row=0, column=0, padx=8, pady=8, sticky="w")
        self.gen_input = self._entry(row1, width=50)
        self.gen_input.grid(row=0, column=1, padx=8, pady=8, sticky="ew")

        tk.Label(row1, text="Algorithm:", font=FONTS["small"],
                 fg=COLORS["subtext"], bg=COLORS["panel"]).grid(row=1, column=0, padx=8, sticky="w")
        self.gen_algo = ttk.Combobox(row1, values=["md5","sha1","sha224","sha256","sha384","sha512"],
                                     state="readonly", width=18)
        self.gen_algo.set("md5")
        self.gen_algo.grid(row=1, column=1, padx=8, pady=6, sticky="w")

        make_button(row1, "⚡ Generate Hash", self._generate_hash,
                    bg=COLORS["teal"]).grid(row=1, column=2, padx=8)
        make_button(row1, "🔄 Generate All", self._generate_all,
                    bg=COLORS["blue"]).grid(row=1, column=3, padx=4)
        row1.columnconfigure(1, weight=1)

        # Results
        row2 = self._panel(p, "📊  Generated Hashes")
        self.gen_result = scrolledtext.ScrolledText(
            row2, height=12, font=FONTS["mono"],
            bg=COLORS["border"], fg=COLORS["success"],
            insertbackground=COLORS["red"], relief="flat", bd=4)
        self.gen_result.pack(fill="both", expand=True, padx=8, pady=8)

        make_button(row2, "📋 Copy to Multi-Hash Tab", self._copy_to_multi,
                    bg=COLORS["yellow"], fg=COLORS["bg"]).pack(pady=6)

    # ── Log Panel ─────────────────────────────────────────

    def _build_log(self):
        bottom = tk.Frame(self, bg=COLORS["bg"])
        bottom.pack(fill="both", expand=True, padx=20, pady=(0, 8))

        log_frame = self._panel(bottom, "📡  Live Output Log")

        self.log_box = scrolledtext.ScrolledText(
            log_frame, height=8,
            font=FONTS["small"],
            bg="#080a0f", fg=COLORS["subtext"],
            insertbackground=COLORS["red"],
            relief="flat", bd=4, state="disabled"
        )
        self.log_box.pack(fill="both", expand=True, padx=8, pady=4)

        for tag, color in [("success", COLORS["success"]), ("error", COLORS["error"]),
                           ("info", COLORS["blue"]), ("warn", COLORS["warn"]),
                           ("crack", COLORS["red"])]:
            self.log_box.tag_config(tag, foreground=color)

        # Export buttons
        exp = tk.Frame(log_frame, bg=COLORS["panel"])
        exp.pack(fill="x", padx=8, pady=6)
        make_button(exp, "💾 Export TXT",  self._export_txt,  bg=COLORS["blue"]).pack(side="left", padx=4)
        make_button(exp, "🌐 Export HTML", self._export_html, bg=COLORS["teal"]).pack(side="left", padx=4)
        make_button(exp, "📊 Export CSV",  self._export_csv,  bg=COLORS["yellow"], fg=COLORS["bg"]).pack(side="left", padx=4)
        make_button(exp, "🗑 Clear Log",   self._clear_log,   bg=COLORS["border"], fg=COLORS["text"]).pack(side="right", padx=4)

        tk.Label(exp, text="⚠ For ethical & educational use only",
                 font=FONTS["small"], fg=COLORS["subtext"],
                 bg=COLORS["panel"]).pack(side="right", padx=12)

    # ── UI Helpers ────────────────────────────────────────

    def _panel(self, parent, title):
        lf = tk.LabelFrame(parent, text=f"  {title}  ",
                           font=FONTS["small"], fg=COLORS["red"],
                           bg=COLORS["panel"], bd=1, relief="groove",
                           labelanchor="nw")
        lf.pack(fill="x", padx=8, pady=6)
        return lf

    def _entry(self, parent, width=40):
        e = tk.Entry(parent, font=FONTS["mono"], width=width,
                     bg=COLORS["border"], fg=COLORS["text"],
                     insertbackground=COLORS["red"],
                     relief="flat", bd=6)
        return e

    def _ctrl_buttons(self, parent, start_cmd, stop_cmd):
        f = tk.Frame(parent, bg=COLORS["bg"])
        f.pack(pady=8)
        make_button(f, "⚡  START CRACKING", start_cmd,
                    bg=COLORS["red"], fg=COLORS["bg"]).pack(side="left", padx=8)
        make_button(f, "⛔  STOP", stop_cmd,
                    bg=COLORS["border"], fg=COLORS["text"]).pack(side="left", padx=8)

    # ── Logging ───────────────────────────────────────────

    def _log(self, msg, tag="info"):
        ts = datetime.datetime.now().strftime("%H:%M:%S")
        self.log_box.configure(state="normal")
        self.log_box.insert("end", f"[{ts}] {msg}\n", tag)
        self.log_box.see("end")
        self.log_box.configure(state="disabled")

    def _update_dashboard(self):
        self.speed_lbl.config(text=f"{self.stats['speed']:,} w/s")
        self.tries_lbl.config(text=f"{self.stats['tries']:,}")
        self.elapsed_lbl.config(text=f"{self.stats['elapsed']:.1f}s")
        self.eta_lbl.config(text=str(self.stats['eta']))
        self.cracked_lbl.config(text=str(len(self.results)))

    def _set_status(self, msg, color=None):
        self.status_lbl.config(text=msg, fg=color or COLORS["teal"])

    # ── Wordlist Actions ──────────────────────────────────

    def _browse_wordlist(self):
        path = filedialog.askopenfilename(
            title="Select Wordlist",
            filetypes=[("Text", "*.txt"), ("All", "*.*")]
        )
        if path:
            self.wordlist_path.set(path)
            count = sum(1 for _ in open(path, errors="ignore"))
            self._log(f"Wordlist loaded: {os.path.basename(path)} ({count:,} words)", "info")

    def _use_rockyou(self):
        for c in ["/usr/share/wordlists/rockyou.txt", os.path.expanduser("~/rockyou.txt")]:
            if os.path.exists(c):
                self.wordlist_path.set(c)
                self._log(f"rockyou.txt loaded from {c}", "info")
                return
        self._log("rockyou.txt not found. Run: sudo gunzip /usr/share/wordlists/rockyou.txt.gz", "warn")
        messagebox.showinfo("Not Found", "rockyou.txt not found.\nKali: sudo gunzip /usr/share/wordlists/rockyou.txt.gz")

    # ── Detect Hash ───────────────────────────────────────

    def _detect(self, entry_widget, label_widget, algo_widget):
        h = entry_widget.get().strip()
        if not h:
            messagebox.showwarning("Missing", "Enter a hash first.")
            return None
        t = detect_hash_type(h)
        if t == "unknown":
            label_widget.config(text="⚠ Unknown", fg=COLORS["warn"])
            self._log(f"Unknown hash length ({len(h)} chars): {h[:20]}...", "warn")
            return None
        label_widget.config(text=f"✔ {t.upper()}", fg=COLORS["teal"])
        algo_widget.set(t)
        self._log(f"Hash detected as {t.upper()}", "info")
        return t

    def _wl_detect(self): self._detect(self.wl_hash, self.wl_detect_lbl, self.wl_algo)
    def _bf_detect(self): self._detect(self.bf_hash, self.bf_detect_lbl, self.bf_algo)

    # ── STOP ──────────────────────────────────────────────

    def _stop(self):
        self.is_running = False
        self._log("Stopped by user.", "warn")
        self._set_status("Stopped", COLORS["warn"])
        self.progress.stop()

    # ══════════════════════════════════════════════════════
    #  ATTACK 1 — WORDLIST
    # ══════════════════════════════════════════════════════

    def _start_wordlist(self):
        h = self.wl_hash.get().strip()
        wl = self.wordlist_path.get()
        algo = self.wl_algo.get()

        if not h: return messagebox.showwarning("Missing", "Enter a hash.")
        if not wl or not os.path.exists(wl): return messagebox.showwarning("Missing", "Select a wordlist file.")

        if algo == "Auto Detect":
            algo = detect_hash_type(h)
            if algo == "unknown": return messagebox.showerror("Unknown", "Cannot detect hash type. Select manually.")
            self.wl_algo.set(algo)

        self._begin_attack()
        self._log(f"{'='*50}", "info")
        self._log(f"WORDLIST ATTACK STARTED", "crack")
        self._log(f"Hash: {h}  |  Algorithm: {algo.upper()}", "info")
        self._log(f"Wordlist: {os.path.basename(wl)}", "info")

        self.crack_thread = threading.Thread(
            target=self._wordlist_worker, args=([h], wl, algo), daemon=True)
        self.crack_thread.start()

    def _wordlist_worker(self, hashes, wordlist, algo):
        start = time.time()
        count = 0
        remaining = set(hashes)

        try:
            total = sum(1 for _ in open(wordlist, errors="ignore"))
            with open(wordlist, errors="ignore") as f:
                for line in f:
                    if not self.is_running: break
                    word = line.rstrip("\n")
                    count += 1
                    computed = compute_hash(word, algo)

                    if computed in remaining:
                        remaining.discard(computed)
                        elapsed = time.time() - start
                        result = {"hash": computed, "password": word, "algo": algo,
                                  "method": "Wordlist", "time": f"{elapsed:.2f}s", "tries": count}
                        self.results.append(result)
                        self.after(0, self._on_found, word, computed, algo, count, elapsed)
                        if not remaining: break

                    if count % 5000 == 0:
                        elapsed = time.time() - start
                        speed = int(count / elapsed) if elapsed > 0 else 0
                        eta = int((total - count) / speed) if speed > 0 else 0
                        self.stats = {"tries": count, "speed": speed,
                                      "elapsed": elapsed, "eta": f"{eta}s"}
                        self.after(0, self._update_dashboard)

        except Exception as e:
            self.after(0, self._log, f"Error: {e}", "error")

        if remaining and self.is_running:
            elapsed = time.time() - start
            self.after(0, self._on_not_found, count, elapsed)
        self.after(0, self._end_attack)

    # ══════════════════════════════════════════════════════
    #  ATTACK 2 — BRUTE FORCE
    # ══════════════════════════════════════════════════════

    def _start_brute(self):
        h = self.bf_hash.get().strip()
        algo = self.bf_algo.get()

        if not h: return messagebox.showwarning("Missing", "Enter a hash.")
        try:
            min_l = int(self.bf_min.get())
            max_l = int(self.bf_max.get())
        except ValueError:
            return messagebox.showerror("Error", "Min/Max length must be numbers.")

        if algo == "Auto Detect":
            algo = detect_hash_type(h)
            if algo == "unknown": return messagebox.showerror("Unknown", "Cannot detect hash type.")
            self.bf_algo.set(algo)

        charsets = {
            "Lowercase (a-z)":           string.ascii_lowercase,
            "Uppercase (A-Z)":           string.ascii_uppercase,
            "Digits (0-9)":              string.digits,
            "Lower + Digits":            string.ascii_lowercase + string.digits,
            "Lower + Upper + Digits":    string.ascii_letters + string.digits,
            "All Printable":             string.printable.strip(),
        }
        charset = charsets.get(self.bf_charset.get(), string.ascii_lowercase + string.digits)

        self._begin_attack()
        self._log(f"{'='*50}", "info")
        self._log("BRUTE FORCE ATTACK STARTED", "crack")
        self._log(f"Hash: {h}  |  Algo: {algo.upper()}  |  Len: {min_l}-{max_l}  |  Charset: {len(charset)} chars", "info")

        self.crack_thread = threading.Thread(
            target=self._brute_worker, args=(h, algo, min_l, max_l, charset), daemon=True)
        self.crack_thread.start()

    def _brute_worker(self, target_hash, algo, min_l, max_l, charset):
        start = time.time()
        count = 0

        try:
            for length in range(min_l, max_l + 1):
                if not self.is_running: break
                self.after(0, self._log, f"Trying length {length}...", "info")
                for combo in itertools.product(charset, repeat=length):
                    if not self.is_running: break
                    word = "".join(combo)
                    count += 1
                    computed = compute_hash(word, algo)

                    if computed == target_hash:
                        elapsed = time.time() - start
                        result = {"hash": target_hash, "password": word, "algo": algo,
                                  "method": "Brute Force", "time": f"{elapsed:.2f}s", "tries": count}
                        self.results.append(result)
                        self.after(0, self._on_found, word, target_hash, algo, count, elapsed)
                        self.after(0, self._end_attack)
                        return

                    if count % 10000 == 0:
                        elapsed = time.time() - start
                        speed = int(count / elapsed) if elapsed > 0 else 0
                        self.stats = {"tries": count, "speed": speed, "elapsed": elapsed, "eta": "—"}
                        self.after(0, self._update_dashboard)

        except Exception as e:
            self.after(0, self._log, f"Error: {e}", "error")

        elapsed = time.time() - start
        self.after(0, self._on_not_found, count, elapsed)
        self.after(0, self._end_attack)

    # ══════════════════════════════════════════════════════
    #  ATTACK 3 — MULTI-HASH
    # ══════════════════════════════════════════════════════

    def _start_multi(self):
        raw = self.multi_text.get("1.0", "end")
        hashes = [l.strip() for l in raw.splitlines()
                  if l.strip() and not l.strip().startswith("#")]

        if not hashes: return messagebox.showwarning("Missing", "Enter at least one hash.")
        wl = self.wordlist_path.get()
        if not wl or not os.path.exists(wl): return messagebox.showwarning("Missing", "Select a wordlist file.")

        self._begin_attack()
        self._log(f"{'='*50}", "info")
        self._log(f"MULTI-HASH ATTACK STARTED  ({len(hashes)} hashes)", "crack")

        self.crack_thread = threading.Thread(
            target=self._multi_worker, args=(hashes, wl), daemon=True)
        self.crack_thread.start()

    def _multi_worker(self, hashes, wordlist):
        start = time.time()
        count = 0

        # Group hashes by algo
        groups = {}
        for h in hashes:
            algo = detect_hash_type(h)
            if algo == "unknown":
                self.after(0, self._log, f"Skipping unknown hash: {h[:20]}...", "warn")
                continue
            groups.setdefault(algo, set()).add(h)
            self.after(0, self._log, f"Hash {h[:16]}... detected as {algo.upper()}", "info")

        remaining = {algo: set(hs) for algo, hs in groups.items()}
        all_remaining = set(h for hs in remaining.values() for h in hs)

        try:
            with open(wordlist, errors="ignore") as f:
                for line in f:
                    if not self.is_running or not all_remaining: break
                    word = line.rstrip("\n")
                    count += 1

                    for algo, rem in list(remaining.items()):
                        if not rem: continue
                        computed = compute_hash(word, algo)
                        if computed in rem:
                            rem.discard(computed)
                            all_remaining.discard(computed)
                            elapsed = time.time() - start
                            result = {"hash": computed, "password": word, "algo": algo,
                                      "method": "Multi-Hash", "time": f"{elapsed:.2f}s", "tries": count}
                            self.results.append(result)
                            self.after(0, self._on_found, word, computed, algo, count, elapsed)

                    if count % 5000 == 0:
                        elapsed = time.time() - start
                        speed = int(count / elapsed) if elapsed > 0 else 0
                        self.stats = {"tries": count, "speed": speed, "elapsed": elapsed, "eta": "—"}
                        self.after(0, self._update_dashboard)

        except Exception as e:
            self.after(0, self._log, f"Error: {e}", "error")

        if all_remaining and self.is_running:
            elapsed = time.time() - start
            self.after(0, self._log, f"{len(all_remaining)} hash(es) not found in wordlist.", "warn")
        self.after(0, self._end_attack)

    # ══════════════════════════════════════════════════════
    #  HASH GENERATOR
    # ══════════════════════════════════════════════════════

    def _generate_hash(self):
        text = self.gen_input.get().strip()
        algo = self.gen_algo.get()
        if not text: return messagebox.showwarning("Missing", "Enter text to hash.")
        h = compute_hash(text, algo)
        self.gen_result.delete("1.0", "end")
        self.gen_result.insert("end", f"Input    : {text}\n")
        self.gen_result.insert("end", f"Algorithm: {algo.upper()}\n")
        self.gen_result.insert("end", f"Hash     : {h}\n")

    def _generate_all(self):
        text = self.gen_input.get().strip()
        if not text: return messagebox.showwarning("Missing", "Enter text to hash.")
        self.gen_result.delete("1.0", "end")
        self.gen_result.insert("end", f"Input: {text}\n{'─'*55}\n")
        for algo in ["md5","sha1","sha224","sha256","sha384","sha512"]:
            h = compute_hash(text, algo)
            self.gen_result.insert("end", f"{algo.upper():<10}: {h}\n")

    def _copy_to_multi(self):
        content = self.gen_result.get("1.0", "end")
        hashes = []
        for line in content.splitlines():
            if ":" in line:
                parts = line.split(":")
                if len(parts) >= 2:
                    h = parts[-1].strip()
                    if len(h) in HASH_LENGTHS:
                        hashes.append(h)
        if hashes:
            self.notebook.select(self.tab_multi)
            self.multi_text.delete("1.0", "end")
            self.multi_text.insert("end", "\n".join(hashes))
            self._log(f"Copied {len(hashes)} hash(es) to Multi-Hash tab.", "info")
        else:
            messagebox.showinfo("None found", "No valid hashes found to copy.")

    # ══════════════════════════════════════════════════════
    #  ATTACK LIFECYCLE
    # ══════════════════════════════════════════════════════

    def _begin_attack(self):
        self.is_running = True
        self.progress.start(10)
        self._set_status("Cracking...", COLORS["red"])

    def _end_attack(self):
        self.is_running = False
        self.progress.stop()
        self._set_status("Done", COLORS["teal"])
        self._update_dashboard()

    def _on_found(self, word, h, algo, count, elapsed):
        self._log(f"{'★'*50}", "crack")
        self._log(f"✅  PASSWORD CRACKED!", "success")
        self._log(f"    Password  : {word}", "success")
        self._log(f"    Hash      : {h}", "success")
        self._log(f"    Algorithm : {algo.upper()}", "success")
        self._log(f"    Tried     : {count:,} words  in  {elapsed:.2f}s", "success")
        self._log(f"{'★'*50}", "crack")
        self._set_status(f"✅ CRACKED: {word}", COLORS["success"])

    def _on_not_found(self, count, elapsed):
        self._log(f"❌ Not found after {count:,} words ({elapsed:.2f}s)", "error")
        self._log("Try a larger wordlist or increase brute force length.", "warn")
        self._set_status("Not found", COLORS["error"])

    # ══════════════════════════════════════════════════════
    #  EXPORTS
    # ══════════════════════════════════════════════════════

    def _no_results(self):
        if not self.results:
            messagebox.showinfo("No Results", "No cracked passwords to export yet.")
            return True
        return False

    def _export_txt(self):
        if self._no_results(): return
        path = filedialog.asksaveasfilename(defaultextension=".txt",
               filetypes=[("Text","*.txt")], initialfile="hashcrack_report.txt")
        if not path: return
        with open(path, "w") as f:
            f.write("=" * 60 + "\n")
            f.write("       HashCrack Pro v2.0 — Crack Report\n")
            f.write(f"  Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 60 + "\n\n")
            for i, r in enumerate(self.results, 1):
                f.write(f"[{i}]\n")
                for k, v in r.items():
                    f.write(f"  {k:<12}: {v}\n")
                f.write("\n")
            f.write("=" * 60 + "\n  For educational and ethical use only.\n" + "=" * 60 + "\n")
        self._log(f"TXT report saved: {path}", "success")

    def _export_csv(self):
        if self._no_results(): return
        path = filedialog.asksaveasfilename(defaultextension=".csv",
               filetypes=[("CSV","*.csv")], initialfile="hashcrack_report.csv")
        if not path: return
        with open(path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["hash","password","algo","method","time","tries"])
            writer.writeheader()
            writer.writerows(self.results)
        self._log(f"CSV report saved: {path}", "success")

    def _export_html(self):
        if self._no_results(): return
        path = filedialog.asksaveasfilename(defaultextension=".html",
               filetypes=[("HTML","*.html")], initialfile="hashcrack_report.html")
        if not path: return
        rows = ""
        for i, r in enumerate(self.results, 1):
            rows += f"""
            <tr>
              <td>{i}</td>
              <td class="hash">{r['hash']}</td>
              <td class="password">{r['password']}</td>
              <td>{r['algo'].upper()}</td>
              <td>{r['method']}</td>
              <td>{r['time']}</td>
              <td>{r['tries']:,}</td>
            </tr>"""

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>HashCrack Pro Report</title>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: 'Courier New', monospace; background: #0b0d12; color: #cdd6f4; padding: 30px; }}
  h1 {{ color: #e63946; font-size: 2rem; margin-bottom: 6px; }}
  .sub {{ color: #6c7086; font-size: 0.85rem; margin-bottom: 30px; }}
  .badge {{ display: inline-block; background: #e63946; color: #0b0d12;
            padding: 4px 12px; border-radius: 4px; font-size: 0.8rem; margin-right: 8px; }}
  table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
  th {{ background: #e63946; color: #0b0d12; padding: 12px 16px; text-align: left; font-size: 0.85rem; }}
  td {{ padding: 10px 16px; border-bottom: 1px solid #1e2230; font-size: 0.85rem; }}
  tr:hover td {{ background: #13161f; }}
  .hash {{ color: #457b9d; font-size: 0.75rem; word-break: break-all; max-width: 200px; }}
  .password {{ color: #a6e3a1; font-weight: bold; }}
  footer {{ margin-top: 30px; color: #6c7086; font-size: 0.75rem; }}
</style>
</head>
<body>
  <h1>🔐 HashCrack Pro v2.0</h1>
  <p class="sub">Red Team Password Cracking Report &nbsp;|&nbsp; Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
  <span class="badge">Total Cracked: {len(self.results)}</span>
  <table>
    <thead>
      <tr><th>#</th><th>Hash</th><th>Password</th><th>Algorithm</th><th>Method</th><th>Time</th><th>Tries</th></tr>
    </thead>
    <tbody>{rows}</tbody>
  </table>
  <footer>⚠ For educational and ethical use only.</footer>
</body>
</html>"""
        with open(path, "w") as f:
            f.write(html)
        self._log(f"HTML report saved: {path}", "success")

    def _clear_log(self):
        self.log_box.configure(state="normal")
        self.log_box.delete("1.0", "end")
        self.log_box.configure(state="disabled")


# ══════════════════════════════════════════════════════════
#  ENTRY POINT
# ══════════════════════════════════════════════════════════

if __name__ == "__main__":
    app = HashCrackPro()
    app.mainloop()
