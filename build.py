"""Build script for AlwaysFnActive."""

import subprocess
import sys
import os

def build():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    main_script = os.path.join(script_dir, "wasd_arrows.py")
    icon_path = os.path.join(script_dir, "icon.ico")

    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--windowed",
        "--name", "AlwaysFnActive",
        "--clean",
        "--noconfirm",
    ]

    if os.path.exists(icon_path):
        cmd.extend(["--icon", icon_path])
        # Bundle icon.ico inside the exe so it can be found at runtime
        cmd.extend(["--add-data", f"{icon_path};."])

    cmd.extend([
        "--hidden-import", "keyboard",
        "--hidden-import", "pystray",
        "--hidden-import", "PIL",
        "--hidden-import", "pystray._win32",
    ])

    cmd.append(main_script)

    print(f"\n  Building...\n")
    subprocess.run(cmd, cwd=script_dir)
    print(f"\n  Done! Check dist/AlwaysFnActive.exe")

if __name__ == "__main__":
    build()
