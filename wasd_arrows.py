"""
AlwaysFnActive — WASD Arrow Key Remapper
by GlaceYT
"""

import keyboard
import threading
import sys
import os
import ctypes
import time
import webbrowser
import tkinter as tk

try:
    import pystray
    from PIL import Image, ImageDraw, ImageFont
    HAS_TRAY = True
except ImportError:
    HAS_TRAY = False


# ── Config ──

APP_NAME    = "AlwaysFnActive"
APP_VERSION = "v4.1"
APP_TAGLINE = "WASD Arrow Key Remapper"
TOGGLE_KEY  = "f9"
QUIT_HOTKEY = "ctrl+alt+q"

KEY_MAP = {
    "w": "up",
    "a": "left",
    "s": "down",
    "d": "right",
}

LINKS = {
    "website": "https://glaceyt.com",
    "youtube": "https://www.youtube.com/@GlaceYT",
    "discord": "https://discord.gg/xQF9f9yUEM",
    "email":   "shivaindiangamer@gmail.com",
}


# ── Colors ──

C = {
    "bg_base":          "#0b0b10",
    "bg_sidebar":       "#101018",
    "bg_card":          "#161622",
    "border_subtle":    "#1f1f32",
    "text_white":       "#f0f0f8",
    "text_primary":     "#d4d4e0",
    "text_secondary":   "#8888a4",
    "text_tertiary":    "#5c5c78",
    "emerald":          "#10b981",
    "emerald_soft":     "#0d3320",
    "emerald_border":   "#059669",
    "red":              "#ef4444",
    "red_soft":         "#450a0a",
    "red_border":       "#dc2626",
    "indigo":           "#6366f1",
    "indigo_soft":      "#312e81",
    "violet":           "#8b5cf6",
    "blue":             "#3b82f6",
    "amber":            "#f59e0b",
    "amber_soft":       "#451a03",
    "keycap_bg":        "#20203a",
    "keycap_text":      "#e0e0f0",
    "arrow_glow":       "#a78bfa",
    "btn_primary":      "#6366f1",
    "btn_primary_hover":"#4f46e5",
    "btn_danger":       "#dc2626",
    "btn_danger_hover": "#b91c1c",
    "white":            "#ffffff",
    "link_blue":        "#60a5fa",
    "link_hover":       "#93c5fd",
    "youtube_red":      "#ff0000",
    "discord_blurple":  "#5865f2",
}


# ── State ──

class AppState:
    def __init__(self):
        self.arrow_mode = True
        self.running = True
        self.tray_icon = None

state = AppState()


def resource_path(relative):
    """Get path to resource — works in dev and PyInstaller bundle."""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), relative)


# ── Key Remapping ──

def activate_arrow_mode():
    for wasd, arrow in KEY_MAP.items():
        try:
            keyboard.remap_key(wasd, arrow)
        except Exception:
            pass


def deactivate_arrow_mode():
    for wasd in KEY_MAP:
        try:
            keyboard.unremap_key(wasd)
        except Exception:
            pass


def release_stuck_keys():
    for key in ["ctrl", "shift", "alt",
                "left ctrl", "right ctrl",
                "left shift", "right shift",
                "left alt", "right alt",
                "up", "down", "left", "right",
                "w", "a", "s", "d"]:
        try:
            keyboard.release(key)
        except Exception:
            pass


# ── Tray Icon ──

def create_tray_image(is_arrow):
    size = 64
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    if is_arrow:
        d.rounded_rectangle([2, 2, 62, 62], 12, fill=(99, 102, 241))
        cx, cy, t = 32, 32, 8
        d.polygon([(cx, cy-18), (cx-t, cy-7), (cx+t, cy-7)], fill=(255,255,255))
        d.polygon([(cx, cy+18), (cx-t, cy+7), (cx+t, cy+7)], fill=(255,255,255))
        d.polygon([(cx-18, cy), (cx-7, cy-t), (cx-7, cy+t)], fill=(255,255,255))
        d.polygon([(cx+18, cy), (cx+7, cy-t), (cx+7, cy+t)], fill=(255,255,255))
        d.ellipse([cx-3, cy-3, cx+3, cy+3], fill=(167, 139, 250))
    else:
        d.rounded_rectangle([2, 2, 62, 62], 12, fill=(239, 68, 68))
        try:
            f = ImageFont.truetype("arial.ttf", 30)
        except Exception:
            f = ImageFont.load_default()
        d.text((32, 32), "W", fill=(255,255,255), font=f, anchor="mm")
    return img


# ── GUI ──

class AlwaysFnActiveGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(f"{APP_NAME} \u2014 {APP_TAGLINE}")
        self.root.configure(bg=C["bg_base"])
        self.root.resizable(False, False)

        w, h = 1280, 720
        sx = (self.root.winfo_screenwidth() - w) // 2
        sy = (self.root.winfo_screenheight() - h) // 2
        self.root.geometry(f"{w}x{h}+{sx}+{sy}")

        ico = resource_path("icon.ico")
        if os.path.exists(ico):
            try:
                self.root.iconbitmap(default=ico)
            except Exception:
                pass

        self._pulse_state = 0
        self._pulse_growing = True
        self._lock = threading.Lock()

        self._build_ui()
        activate_arrow_mode()

        keyboard.on_press_key(TOGGLE_KEY,
                              lambda e: self.root.after(0, self.toggle_mode),
                              suppress=False)
        keyboard.add_hotkey(QUIT_HOTKEY,
                            lambda: self.root.after(0, self.quit_app),
                            suppress=False)

        if HAS_TRAY:
            self._setup_tray()

        self._animate_pulse()
        self.root.protocol("WM_DELETE_WINDOW", self.quit_app)

    def _build_ui(self):
        main = tk.Frame(self.root, bg=C["bg_base"])
        main.pack(fill="both", expand=True)

        sb = tk.Frame(main, bg=C["bg_sidebar"], width=320)
        sb.pack(side="left", fill="y")
        sb.pack_propagate(False)
        self._sidebar(sb)

        tk.Frame(main, bg=C["border_subtle"], width=1).pack(side="left", fill="y")

        ct = tk.Frame(main, bg=C["bg_base"])
        ct.pack(side="left", fill="both", expand=True)
        self._content(ct)

    def _sidebar(self, p):
        brand = tk.Frame(p, bg=C["bg_sidebar"], padx=28, pady=28)
        brand.pack(fill="x")

        s = 56
        ic = tk.Canvas(brand, width=s, height=s,
                       bg=C["bg_sidebar"], highlightthickness=0)
        ic.pack(anchor="w")
        ic.create_rectangle(2, 2, s-2, s-2,
                            fill=C["indigo"], outline=C["violet"], width=2)
        cx, cy, t = s//2, s//2, 7
        ic.create_polygon(cx, cy-16, cx-t, cy-8, cx+t, cy-8,
                          fill="#fff", outline="")
        ic.create_polygon(cx, cy+16, cx-t, cy+8, cx+t, cy+8,
                          fill="#fff", outline="")
        ic.create_polygon(cx-16, cy, cx-8, cy-t, cx-8, cy+t,
                          fill="#fff", outline="")
        ic.create_polygon(cx+16, cy, cx+8, cy-t, cx+8, cy+t,
                          fill="#fff", outline="")
        ic.create_oval(cx-3, cy-3, cx+3, cy+3,
                       fill=C["arrow_glow"], outline="")

        tk.Label(brand, text=APP_NAME,
                 font=("Segoe UI Semibold", 18),
                 fg=C["text_white"], bg=C["bg_sidebar"],
                 anchor="w").pack(fill="x", pady=(14, 0))
        tk.Label(brand, text=APP_TAGLINE,
                 font=("Segoe UI", 10),
                 fg=C["text_secondary"], bg=C["bg_sidebar"],
                 anchor="w").pack(fill="x", pady=(2, 0))
        tk.Label(brand, text=APP_VERSION,
                 font=("Consolas", 9),
                 fg=C["text_tertiary"], bg=C["bg_sidebar"],
                 anchor="w").pack(fill="x", pady=(4, 0))

        sf = tk.Frame(p, bg=C["bg_sidebar"], padx=28)
        sf.pack(fill="x")
        tk.Frame(sf, bg=C["border_subtle"], height=1).pack(fill="x", pady=8)

        sc = tk.Frame(p, bg=C["bg_sidebar"], padx=28, pady=8)
        sc.pack(fill="x")
        tk.Label(sc, text="STATUS", font=("Segoe UI Semibold", 8),
                 fg=C["text_tertiary"], bg=C["bg_sidebar"],
                 anchor="w").pack(fill="x", pady=(0, 10))

        self.scard = tk.Frame(sc, bg=C["emerald_soft"], padx=16, pady=14,
                              highlightbackground=C["emerald_border"],
                              highlightthickness=1)
        self.scard.pack(fill="x")

        sr = tk.Frame(self.scard, bg=C["emerald_soft"])
        sr.pack(fill="x")

        self.dot = tk.Canvas(sr, width=12, height=12,
                             bg=C["emerald_soft"], highlightthickness=0)
        self.dot.pack(side="left", padx=(0, 10))
        self.dot_o = self.dot.create_oval(0, 0, 12, 12,
                                          fill=C["emerald"], outline="")
        self.dot_i = self.dot.create_oval(3, 3, 9, 9,
                                          fill="#fff", outline="")

        self.slbl = tk.Label(sr, text="ARROW MODE",
                             font=("Segoe UI Semibold", 11),
                             fg=C["emerald"], bg=C["emerald_soft"])
        self.slbl.pack(side="left")

        self.sdesc = tk.Label(self.scard,
                              text="W A S D  \u2192  \u2191 \u2190 \u2193 \u2192",
                              font=("Consolas", 10),
                              fg=C["text_secondary"],
                              bg=C["emerald_soft"], anchor="w")
        self.sdesc.pack(fill="x", pady=(8, 0))

        tc = tk.Frame(p, bg=C["bg_sidebar"], padx=28, pady=12)
        tc.pack(fill="x")
        self.tbtn = tk.Label(tc, text="\u23f8   Switch to Type Mode",
                             font=("Segoe UI Semibold", 11),
                             fg="#fff", bg=C["btn_primary"],
                             pady=14, padx=16, cursor="hand2",
                             anchor="center")
        self.tbtn.pack(fill="x")
        self.tbtn.bind("<Button-1>", lambda e: self.toggle_mode())
        self.tbtn.bind("<Enter>", lambda e: self.tbtn.config(
            bg=C["btn_primary_hover"] if state.arrow_mode
            else C["btn_danger_hover"]))
        self.tbtn.bind("<Leave>", lambda e: self.tbtn.config(
            bg=C["btn_primary"] if state.arrow_mode
            else C["btn_danger"]))

        hk = tk.Frame(p, bg=C["bg_sidebar"], padx=28, pady=4)
        hk.pack(fill="x")
        tk.Label(hk, text="SHORTCUTS", font=("Segoe UI Semibold", 8),
                 fg=C["text_tertiary"], bg=C["bg_sidebar"],
                 anchor="w").pack(fill="x", pady=(0, 10))
        for k, d in [("F9", "Toggle Arrow / Type Mode"),
                     ("Ctrl+Alt+Q", "Quit Application")]:
            r = tk.Frame(hk, bg=C["bg_sidebar"])
            r.pack(fill="x", pady=3)
            tk.Label(r, text=f" {k} ", font=("Consolas", 9),
                     fg=C["blue"], bg=C["keycap_bg"],
                     padx=6, pady=2).pack(side="left")
            tk.Label(r, text=f"  {d}", font=("Segoe UI", 9),
                     fg=C["text_secondary"],
                     bg=C["bg_sidebar"]).pack(side="left")

        tk.Frame(p, bg=C["bg_sidebar"]).pack(fill="both", expand=True)

        ft = tk.Frame(p, bg=C["bg_sidebar"], padx=28, pady=20)
        ft.pack(fill="x", side="bottom")
        tk.Frame(ft, bg=C["border_subtle"], height=1).pack(fill="x", pady=(0, 14))
        tk.Label(ft, text="CONNECT", font=("Segoe UI Semibold", 8),
                 fg=C["text_tertiary"], bg=C["bg_sidebar"],
                 anchor="w").pack(fill="x", pady=(0, 10))

        for txt, url, clr in [
            ("\U0001f310  Website",  LINKS["website"],  C["link_blue"]),
            ("\u25b6  YouTube",      LINKS["youtube"],  C["youtube_red"]),
            ("\U0001f4ac  Discord",  LINKS["discord"],  C["discord_blurple"]),
            ("\U0001f4e7  " + LINKS["email"],
             "mailto:" + LINKS["email"], C["text_secondary"]),
        ]:
            lb = tk.Label(ft, text=txt, font=("Segoe UI", 9),
                          fg=clr, bg=C["bg_sidebar"],
                          cursor="hand2", anchor="w")
            lb.pack(fill="x", pady=2)
            lb.bind("<Button-1>", lambda e, u=url: webbrowser.open(u))
            lb.bind("<Enter>", lambda e, l=lb: l.config(fg=C["link_hover"]))
            lb.bind("<Leave>", lambda e, l=lb, c=clr: l.config(fg=c))

    def _content(self, p):
        hdr = tk.Frame(p, bg=C["bg_base"], padx=40, pady=28)
        hdr.pack(fill="x")
        tk.Label(hdr, text="Key Mappings",
                 font=("Segoe UI Semibold", 22),
                 fg=C["text_white"], bg=C["bg_base"],
                 anchor="w").pack(fill="x")
        tk.Label(hdr,
                 text="Your WASD keys are remapped to arrow keys when Arrow Mode is active.",
                 font=("Segoe UI", 11),
                 fg=C["text_secondary"], bg=C["bg_base"],
                 anchor="w").pack(fill="x", pady=(6, 0))

        g = tk.Frame(p, bg=C["bg_base"], padx=40)
        g.pack(fill="x", pady=(0, 20))

        data = [("W", "\u2191", "Up Arrow", "Navigate upward"),
                ("A", "\u2190", "Left Arrow", "Navigate left"),
                ("S", "\u2193", "Down Arrow", "Navigate downward"),
                ("D", "\u2192", "Right Arrow", "Navigate right")]

        r1 = tk.Frame(g, bg=C["bg_base"])
        r1.pack(fill="x", pady=(0, 12))
        for i in range(2):
            self._kcard(r1, *data[i], i)

        r2 = tk.Frame(g, bg=C["bg_base"])
        r2.pack(fill="x")
        for i in range(2, 4):
            self._kcard(r2, *data[i], i-2)

        sp = tk.Frame(p, bg=C["bg_base"], padx=40)
        sp.pack(fill="x", pady=(10, 0))
        tk.Frame(sp, bg=C["border_subtle"], height=1).pack(fill="x")

        hw = tk.Frame(p, bg=C["bg_base"], padx=40, pady=24)
        hw.pack(fill="x")
        tk.Label(hw, text="How It Works",
                 font=("Segoe UI Semibold", 16),
                 fg=C["text_white"], bg=C["bg_base"],
                 anchor="w").pack(fill="x", pady=(0, 14))

        for n, t, d in [
            ("1", "Global Key Remap",
             "Intercepts WASD key events and translates them to "
             "arrow keys at the system level."),
            ("2", "Works Everywhere",
             "Arrow Mode works in browsers, games, text editors, "
             "and terminals."),
            ("3", "Instant Toggle with F9",
             "Press F9 anytime to switch between Arrow Mode and Type "
             "Mode. All modifier keys are released during the switch."),
        ]:
            sr = tk.Frame(hw, bg=C["bg_base"])
            sr.pack(fill="x", pady=6)
            tk.Label(sr, text=f" {n} ",
                     font=("Consolas", 10, "bold"),
                     fg=C["indigo"], bg=C["indigo_soft"],
                     padx=6, pady=2).pack(side="left", padx=(0, 14),
                                          anchor="n")
            tf = tk.Frame(sr, bg=C["bg_base"])
            tf.pack(side="left", fill="x", expand=True)
            tk.Label(tf, text=t,
                     font=("Segoe UI Semibold", 10),
                     fg=C["text_primary"], bg=C["bg_base"],
                     anchor="w").pack(fill="x")
            tk.Label(tf, text=d,
                     font=("Segoe UI", 9),
                     fg=C["text_tertiary"], bg=C["bg_base"],
                     anchor="w", wraplength=580,
                     justify="left").pack(fill="x", pady=(2, 0))

        tk.Frame(p, bg=C["bg_base"]).pack(fill="both", expand=True)

        bb = tk.Frame(p, bg=C["bg_sidebar"], padx=40, pady=14)
        bb.pack(fill="x", side="bottom")
        tk.Label(bb,
                 text=f"\u00a9 2025 GlaceYT  \u00b7  {APP_NAME} {APP_VERSION}"
                      "  \u00b7  Made with \u2764 for mini keyboard users",
                 font=("Segoe UI", 9), fg=C["text_tertiary"],
                 bg=C["bg_sidebar"]).pack(side="left")
        qb = tk.Label(bb, text="  \u2715  Quit  ",
                      font=("Segoe UI Semibold", 9),
                      fg=C["text_secondary"], bg=C["bg_sidebar"],
                      cursor="hand2")
        qb.pack(side="right")
        qb.bind("<Button-1>", lambda e: self.quit_app())
        qb.bind("<Enter>", lambda e: qb.config(fg=C["red"]))
        qb.bind("<Leave>", lambda e: qb.config(fg=C["text_secondary"]))

    def _kcard(self, parent, key, arrow, name, desc, idx):
        px = (0, 6) if idx == 0 else (6, 0)
        outer = tk.Frame(parent, bg=C["border_subtle"])
        outer.pack(side="left", fill="both", expand=True, padx=px)
        card = tk.Frame(outer, bg=C["bg_card"], padx=24, pady=20)
        card.pack(fill="both", expand=True, padx=1, pady=1)
        top = tk.Frame(card, bg=C["bg_card"])
        top.pack(fill="x")
        tk.Label(top, text=f"  {key}  ",
                 font=("Consolas", 22, "bold"),
                 fg=C["keycap_text"], bg=C["keycap_bg"],
                 padx=8, pady=4).pack(side="left")
        tk.Label(top, text="  \u2192  ",
                 font=("Segoe UI", 16),
                 fg=C["text_tertiary"], bg=C["bg_card"]).pack(side="left")
        tk.Label(top, text=f"  {arrow}  ",
                 font=("Segoe UI", 22),
                 fg=C["arrow_glow"], bg=C["keycap_bg"],
                 padx=8, pady=4).pack(side="left")
        tk.Label(card, text=name,
                 font=("Segoe UI Semibold", 11),
                 fg=C["text_primary"], bg=C["bg_card"],
                 anchor="w").pack(fill="x", pady=(12, 0))
        tk.Label(card, text=desc,
                 font=("Segoe UI", 9),
                 fg=C["text_tertiary"], bg=C["bg_card"],
                 anchor="w").pack(fill="x", pady=(2, 0))

    def _animate_pulse(self):
        if not state.running:
            return
        if state.arrow_mode:
            if self._pulse_growing:
                self._pulse_state += 1
                if self._pulse_state >= 3:
                    self._pulse_growing = False
            else:
                self._pulse_state -= 1
                if self._pulse_state <= 0:
                    self._pulse_growing = True
            o = self._pulse_state
            self.dot.coords(self.dot_i, 3-o, 3-o, 9+o, 9+o)
        self.root.after(400, self._animate_pulse)

    def toggle_mode(self):
        with self._lock:
            release_stuck_keys()
            time.sleep(0.02)
            if state.arrow_mode:
                deactivate_arrow_mode()
                state.arrow_mode = False
            else:
                state.arrow_mode = True
                activate_arrow_mode()
            release_stuck_keys()
            self._update_ui()
            if HAS_TRAY and state.tray_icon:
                try:
                    state.tray_icon.icon = create_tray_image(state.arrow_mode)
                    m = "Arrow" if state.arrow_mode else "Type"
                    state.tray_icon.title = f"{APP_NAME} \u2014 {m} Mode"
                except Exception:
                    pass

    def _update_ui(self):
        if state.arrow_mode:
            bg = C["emerald_soft"]
            self.scard.config(bg=bg, highlightbackground=C["emerald_border"])
            self.dot.config(bg=bg)
            self.dot.itemconfig(self.dot_o, fill=C["emerald"])
            self.dot.itemconfig(self.dot_i, fill="#fff")
            self.slbl.config(text="ARROW MODE", fg=C["emerald"], bg=bg)
            self.sdesc.config(
                text="W A S D  \u2192  \u2191 \u2190 \u2193 \u2192", bg=bg)
            self.tbtn.config(text="\u23f8   Switch to Type Mode",
                             bg=C["btn_primary"])
            for w in self.scard.winfo_children():
                try: w.config(bg=bg)
                except: pass
        else:
            bg = C["red_soft"]
            self.scard.config(bg=bg, highlightbackground=C["red_border"])
            self.dot.config(bg=bg)
            self.dot.itemconfig(self.dot_o, fill=C["red"])
            self.dot.itemconfig(self.dot_i, fill="#fff")
            self.slbl.config(text="TYPE MODE", fg=C["red"], bg=bg)
            self.sdesc.config(text="W A S D  typing normally", bg=bg)
            self.tbtn.config(text="\u25b6   Switch to Arrow Mode",
                             bg=C["btn_danger"])
            for w in self.scard.winfo_children():
                try: w.config(bg=bg)
                except: pass

    def _setup_tray(self):
        img = create_tray_image(True)
        def on_show(i, it):
            self.root.after(0, self._show)
        def on_toggle(i, it):
            self.root.after(0, self.toggle_mode)
        def on_quit(i, it):
            self.root.after(0, self.quit_app)
        menu = pystray.Menu(
            pystray.MenuItem("Show Window", on_show, default=True),
            pystray.MenuItem("Toggle Mode", on_toggle),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Quit", on_quit),
        )
        state.tray_icon = pystray.Icon(
            APP_NAME.lower(), img,
            f"{APP_NAME} \u2014 Arrow Mode", menu)
        threading.Thread(target=state.tray_icon.run, daemon=True).start()

    def _show(self):
        self.root.deiconify()
        self.root.lift()
        self.root.focus_force()

    def quit_app(self):
        state.running = False
        deactivate_arrow_mode()
        release_stuck_keys()
        try:
            keyboard.unhook_all()
        except Exception:
            pass
        if HAS_TRAY and state.tray_icon:
            try:
                state.tray_icon.stop()
            except Exception:
                pass
        self.root.destroy()
        os._exit(0)

    def run(self):
        self.root.mainloop()


def main():
    app = AlwaysFnActiveGUI()
    app.run()

if __name__ == "__main__":
    main()
