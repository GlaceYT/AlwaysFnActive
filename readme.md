<div align="center">
  <img src="https://i.ibb.co/GfTxbJfC/7-edited.png" alt="Banner" width="100%"/>
</div>

<div align="center">

# AlwaysFnActive

### WASD Arrow Key Remapper for Mini Keyboards

[![GitHub release](https://img.shields.io/github/v/release/GlaceYT/AlwaysFnActive?style=for-the-badge&color=6366f1)](https://github.com/GlaceYT/AlwaysFnActive/releases)
[![License](https://img.shields.io/github/license/GlaceYT/AlwaysFnActive?style=for-the-badge&color=10b981)](LICENSE)
[![Downloads](https://img.shields.io/github/downloads/GlaceYT/AlwaysFnActive/total?style=for-the-badge&color=8b5cf6)](https://github.com/GlaceYT/AlwaysFnActive/releases)
[![Stars](https://img.shields.io/github/stars/GlaceYT/AlwaysFnActive?style=for-the-badge&color=f59e0b)](https://github.com/GlaceYT/AlwaysFnActive/stargazers)

**Remap your WASD keys to Arrow Keys with a single click.**
Built for 60%/65% keyboards that lack dedicated arrow keys.

[Download](https://github.com/GlaceYT/AlwaysFnActive/releases) · [Report Bug](https://github.com/GlaceYT/AlwaysFnActive/issues) · [Discord](https://discord.gg/xQF9f9yUEM)

</div>

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| **WASD → Arrow Keys** | W↑ A← S↓ D→ — instant remapping |
| **Toggle with F9** | Switch between Arrow Mode and Type Mode anytime |
| **No Admin Required** | Works without elevated privileges |
| **System Tray** | Runs quietly in the background |
| **Stuck Key Prevention** | All modifiers are safely released on every toggle |
| **Dark UI** | Clean, modern 1280×720 interface |
| **Portable** | Single `.exe` — no installation needed |

---

## 📥 Installation

### Option 1: Download the EXE (Recommended)

1. Go to the [Releases](https://github.com/GlaceYT/AlwaysFnActive/releases) page
2. Download `AlwaysFnActive.exe`
3. Double-click to run — that's it!

### Option 2: Run from Source

```bash
git clone https://github.com/GlaceYT/AlwaysFnActive.git
cd AlwaysFnActive
pip install -r requirements.txt
python wasd_arrows.py
```

### Option 3: Build the EXE Yourself

```bash
pip install -r requirements.txt
python build.py
# Output: dist/AlwaysFnActive.exe
```

---

## 🎮 Usage

| Action | How |
|--------|-----|
| **Start** | Run `AlwaysFnActive.exe` — starts in Arrow Mode |
| **Toggle** | Press `F9` or click the toggle button |
| **Quit** | Press `Ctrl+Alt+Q` or click Quit |
| **Tray** | Minimize to system tray — right-click for options |

### Key Mappings (Arrow Mode ON)

```
W  →  ↑  Up Arrow
A  →  ←  Left Arrow
S  →  ↓  Down Arrow
D  →  →  Right Arrow
```

When Arrow Mode is **OFF**, WASD types normally.

---

## 🖥️ Screenshot

<div align="center">
  <img src="https://i.ibb.co/GfTxbJfC/7-edited.png" alt="AlwaysFnActive Screenshot" width="80%"/>
</div>

---

## 🔧 Requirements (for running from source)

- Python 3.8+
- Windows 10/11

```
keyboard
pystray
Pillow
```

---

## 📂 Project Structure

```
AlwaysFnActive/
├── wasd_arrows.py      # Main application
├── build.py            # PyInstaller build script
├── generate_icon.py    # Icon generator
├── icon.ico            # Application icon
├── requirements.txt    # Python dependencies
├── readme.md           # This file
└── dist/
    └── AlwaysFnActive.exe
```

---

## ❓ FAQ

**Q: Does this work in games?**
A: Yes. Arrow Mode works in any application — browsers, games, editors, terminals.

**Q: Do I need admin privileges?**
A: No. AlwaysFnActive works without admin.

**Q: My Ctrl/Shift/Alt key got stuck after toggling.**
A: This is handled automatically — all modifiers are released on every toggle. If it still happens, press and release the stuck key manually.

**Q: Can I change the toggle key from F9?**
A: Edit `TOGGLE_KEY` in `wasd_arrows.py` and rebuild.

**Q: Can I remap to different keys?**
A: Edit the `KEY_MAP` dictionary in `wasd_arrows.py` and rebuild.

---

## 🤝 Connect

[![Website](https://img.shields.io/badge/Website-glaceyt.com-60a5fa?style=for-the-badge)](https://glaceyt.com)
[![YouTube](https://img.shields.io/badge/YouTube-GlaceYT-ff0000?style=for-the-badge&logo=youtube)](https://www.youtube.com/@GlaceYT)
[![Discord](https://img.shields.io/badge/Discord-Join_Server-5865f2?style=for-the-badge&logo=discord)](https://discord.gg/xQF9f9yUEM)

---

<div align="center">

Made with ❤️ by [GlaceYT](https://github.com/GlaceYT) for mini keyboard users

⭐ Star this repo if you found it useful!

</div>