# 🔐 HashCrack Pro v2.0 — Advanced Edition
### Real-Time Password Hash Cracking Suite | Red Team Internship Project

![Python](https://img.shields.io/badge/Python-3.x-blue?style=flat-square&logo=python)
![Platform](https://img.shields.io/badge/Platform-Kali%20Linux-blue?style=flat-square&logo=linux)
![License](https://img.shields.io/badge/License-Educational%20Use%20Only-red?style=flat-square)
![Version](https://img.shields.io/badge/Version-2.0-brightgreen?style=flat-square)

> ⚠️ **Disclaimer:** Strictly for **educational and ethical use** as part of a Red Team internship. Only use on systems you own or have permission to test.

---

## 📌 About

**HashCrack Pro v2.0** is a full-featured GUI desktop tool for cracking password hashes.
Built in Python as a **Red Team Internship Project** to demonstrate real-world password attack techniques.

---

## ✨ Features

| Feature | Description |
|--------|-------------|
| 📖 Wordlist Attack | Crack hashes using password wordlists (rockyou.txt etc.) |
| 💥 Brute Force Attack | Try every possible combination with custom charset & length |
| 📋 Multi-Hash Cracking | Crack multiple hashes at once from a single wordlist pass |
| ⚙️ Hash Generator | Generate MD5/SHA1/SHA256+ hashes for testing |
| 🔍 Auto Hash Detection | Auto-detect hash type by length |
| 📊 Live Dashboard | Real-time speed, count, elapsed time, ETA |
| 💾 Export TXT | Save results as plain text report |
| 🌐 Export HTML | Beautiful dark-themed HTML report |
| 📊 Export CSV | Structured CSV for spreadsheet analysis |
| 🎨 Dark GUI | Professional cybersecurity-themed interface |

---

## 🛠️ Tech Stack

- **Language:** Python 3.x
- **GUI:** Tkinter (built-in)
- **Hashing:** hashlib (built-in)
- **Brute Force:** itertools (built-in)
- **Threading:** threading (built-in)
- **Export:** csv, datetime, os (all built-in)

> No external packages needed!

---

## 📦 Installation & Run

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/HashCrack-Pro.git
cd HashCrack-Pro

# 2. Run the tool
python3 hashcrack_pro_advanced.py
```

---

## 🧪 Quick Test

```bash
# Generate a test MD5 hash
echo -n "password123" | md5sum
# Output: 482c811da5d5b4bc6d497ffa98491e38

# Generate SHA256
echo -n "hello" | sha256sum

# Setup rockyou.txt (Kali Linux)
sudo gunzip /usr/share/wordlists/rockyou.txt.gz
```

---

## 🗂️ Tab Guide

### 📖 Tab 1 — Wordlist Attack
1. Paste your hash
2. Click **Detect Type**
3. Load wordlist or click **rockyou.txt**
4. Click **START CRACKING**

### 💥 Tab 2 — Brute Force
1. Paste your hash
2. Set **Min/Max length** and **Charset**
3. Click **START CRACKING**
> Best for short passwords (1-5 chars)

### 📋 Tab 3 — Multi-Hash
1. Paste multiple hashes (one per line)
2. Load wordlist
3. Cracks all hashes in one pass!

### ⚙️ Tab 4 — Hash Generator
1. Type any text
2. Select algorithm
3. Click **Generate Hash** or **Generate All**
4. Copy hashes to Multi-Hash tab for testing

---

## 📊 Export Formats

| Format | Best For |
|--------|---------|
| 💾 TXT | Simple readable report |
| 🌐 HTML | Presentation / portfolio |
| 📊 CSV | Data analysis / Excel |

---

## 🔐 Supported Hash Types

| Hash | Characters |
|------|-----------|
| MD5 | 32 |
| SHA1 | 40 |
| SHA224 | 56 |
| SHA256 | 64 |
| SHA384 | 96 |
| SHA512 | 128 |

---

## 📁 Project Structure

```
HashCrack-Pro/
├── hashcrack_pro_advanced.py  ← Main tool (v2.0)
├── hashcrack_pro.py           ← Basic tool (v1.0)
├── README.md                  ← Documentation
├── requirements.txt           ← Dependencies (all built-in)
├── screenshots/
│   └── tool_screenshot.png
└── wordlists/
    └── sample_wordlist.txt
```

---

## 🛡️ Defence Tips (Blue Team)

| Attack | Defence |
|--------|---------|
| Wordlist Attack | Use unique passwords not in common lists |
| Brute Force | Use long passwords (12+ chars) |
| Hash Cracking | Use bcrypt/Argon2 with salt |
| All attacks | Enable Multi-Factor Authentication (MFA) |

---

## 👨‍💻 Author

**Your Name** — Cybersecurity Internship | Red Team
- GitHub: [@YOUR_USERNAME](https://github.com/YOUR_USERNAME)
- LinkedIn: [Your LinkedIn](https://linkedin.com)

---

## ⭐ Support

If you found this useful, please **star** ⭐ the repo!

```
⭐ Star  🍴 Fork  📢 Share
```
