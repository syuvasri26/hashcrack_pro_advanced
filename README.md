#  HashCrack Pro v2.0
### Real-Time Password Hash Cracking Suite | Red Team Internship Project

![Python](https://img.shields.io/badge/Python-3.x-blue?style=flat-square&logo=python)
![Platform](https://img.shields.io/badge/Platform-Kali%20Linux-blue?style=flat-square&logo=linux)
![License](https://img.shields.io/badge/License-Educational%20Use%20Only-red?style=flat-square)
![Version](https://img.shields.io/badge/Version-2.0-brightgreen?style=flat-square)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square)

>  **Disclaimer:** This tool is built strictly for **educational and ethical purposes** as part of a Red Team internship project. Do NOT use on systems you do not own or have explicit permission to test.

---

##  About the Project

**HashCrack Pro v2.0** is a full-featured GUI desktop tool for cracking password hashes in real time.

It demonstrates how attackers crack passwords using wordlist and brute force techniques — helping security professionals understand why strong passwords and proper hashing matter.

This tool was developed as part of a **15-day Cybersecurity Internship** focusing on Red Team operations.

---

##  Tool Preview

```
╔══════════════════════════════════════════════════════════╗
║              HashCrack Pro v2.0 — ADVANCED               ║
║        Real-Time Password Hash Cracking Suite            ║
║                Red Team Internship Project               ║
╚══════════════════════════════════════════════════════════╝
```

---

##  Features

| Feature | Description |
|--------|-------------|
| 📖 Wordlist Attack | Crack hashes using rockyou.txt or any wordlist |
| 💥 Brute Force Attack | Try every combination with custom charset & length |
| 📋 Multi-Hash Cracking | Crack multiple hashes at once in a single pass |
| ⚙️ Hash Generator | Generate MD5/SHA1/SHA256+ hashes for testing |
| 🔍 Auto Hash Detection | Automatically detect hash type by length |
| 📊 Live Dashboard | Real-time speed (w/s), word count, elapsed time, ETA |
| 💾 Export TXT | Save results as a plain text report |
| 🌐 Export HTML | Beautiful dark-themed HTML report for presentations |
| 📊 Export CSV | Structured CSV for spreadsheet analysis |
| 🎨 Dark GUI | Professional cybersecurity-themed desktop interface |

---

##  Tech Stack

| Library | Purpose |
|---------|---------|
| `tkinter` | GUI — windows, buttons, input fields |
| `hashlib` | Hashing algorithms (MD5, SHA1, SHA256 etc.) |
| `threading` | Background cracking — keeps GUI smooth |
| `itertools` | Brute force combination generation |
| `csv` | CSV export |
| `datetime` | Timestamps in reports |
| `os` | File handling |

>  No external packages needed — all built-in Python libraries!

---

##  Installation

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/HashCrack-Pro.git
cd HashCrack-Pro
```

### 2. Run the Tool
```bash
python3 hashcrack_pro_advanced.py
```

### 3. Setup rockyou.txt (Kali Linux)
```bash
sudo gunzip /usr/share/wordlists/rockyou.txt.gz
```

---

##  Quick Test

### Step 1 — Generate test hashes in terminal
```bash
# MD5
echo -n "password123" | md5sum
# Output: 482c811da5d5b4bc6d497ffa98491e38

# SHA256
echo -n "hello123" | sha256sum

# SHA1
echo -n "admin" | sha1sum
```

### Step 2 — Run the tool
```bash
python3 hashcrack_pro_advanced.py
```

### Step 3 — Crack it
1. Paste the hash into the tool
2. Click **🔍 Detect Type**
3. Click **⚡ rockyou.txt**
4. Click **⚡ START CRACKING**
5. Watch it crack in real time! ✅

---

## Tab Guide

### 📖 Tab 1 — Wordlist Attack
- Paste hash → Detect type → Load wordlist → Start cracking
- Best for: most common passwords

### 💥 Tab 2 — Brute Force Attack
- Paste hash → Set min/max length → Choose charset → Start
- Best for: short unknown passwords (1–5 chars)
- Charset options: lowercase, digits, lowercase+digits, all printable

### 📋 Tab 3 — Multi-Hash Cracking
- Paste multiple hashes (one per line) → Load wordlist → Start
- Cracks all hashes in a single wordlist pass — very efficient!

### ⚙️ Tab 4 — Hash Generator
- Type any text → Select algorithm → Generate Hash or Generate All
- Copy generated hashes directly to Multi-Hash tab for testing

---

##  Live Dashboard

While cracking, the top dashboard shows live stats:

| Stat | Description |
|------|-------------|
| ⚡ Speed | Words per second being tried |
| 🔢 Tried | Total words attempted so far |
| ⏱ Elapsed | Time taken so far |
| 🎯 ETA | Estimated time remaining |
| ✅ Cracked | Number of hashes cracked |

---

##  Export Formats

| Format | Best For |
|--------|---------|
| 💾 TXT | Quick readable summary |
| 🌐 HTML | Presentations & portfolio (opens in browser) |
| 📊 CSV | Excel / spreadsheet analysis |

---

##  Supported Hash Types

| Algorithm | Hash Length | Example Use |
|-----------|------------|-------------|
| MD5 | 32 characters | Legacy systems |
| SHA1 | 40 characters | Git commits, old auth |
| SHA224 | 56 characters | Lightweight SHA2 |
| SHA256 | 64 characters | Modern web apps |
| SHA384 | 96 characters | TLS certificates |
| SHA512 | 128 characters | High-security systems |

---

##  Project Structure

```
HashCrack-Pro/
│
├── hashcrack_pro_advanced.py   ← Main tool (v2.0) — Advanced full features
├── hashcrack_pro.py            ← Basic tool (v1.0)
├── README.md                   ← Project documentation
├── requirements.txt            ← Dependencies (all built-in)
│
├── screenshots/
│   └── tool_screenshot.png     ← GUI screenshot
│
└── wordlists/
    └── sample_wordlist.txt     ← Sample wordlist for testing
```

---

##  How It Works

```
User enters hash
      ↓
Tool auto-detects hash type (MD5 / SHA1 / SHA256 ...)
      ↓
Load wordlist (rockyou.txt — 14 million passwords)
      ↓
Background thread starts cracking
      ↓
┌─────────────────────────────────┐
│  Take word from wordlist        │
│  Hash it using same algorithm   │
│  Compare with target hash       │
│  Match? → Show password ✅      │
│  No match? → Try next word      │
└─────────────────────────────────┘
      ↓
Export Report (TXT / HTML / CSV)
```

---

##  Defence Recommendations (Blue Team)

| Attack | Defence |
|--------|---------|
| Wordlist Attack | Use passwords not found in common wordlists |
| Brute Force | Use long passwords (12+ characters) |
| Hash Cracking | Use bcrypt or Argon2 with salt instead of MD5/SHA1 |
| All attacks | Enable Multi-Factor Authentication (MFA) |

---

##  Ethical Use

This tool is for **educational purposes only**.

- ✅ Use only on systems you own
- ✅ Use in lab environments (VMs, CTFs)
- ✅ Use for learning and awareness
- ❌ Never use on real systems without permission
- ❌ Never use for malicious purposes

---

##  Author

**Your Name**
- 🎓 Cybersecurity Internship — Red Team (2024)
- 🐙 GitHub: [@YOUR_USERNAME](https://github.com/YOUR_USERNAME)
- 💼 LinkedIn: [Your LinkedIn](https://linkedin.com/in/yourprofile)

---

##  License

This project is for **educational use only**.
Use responsibly and ethically.

---

##  Support

If you found this useful, please give it a ⭐ star — it helps a lot!
